# Tema: comprobar tres procesos reales y todo el recorrido HTTP.
import os
import socket
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from uuid import uuid4

import pytest
import requests

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def system(tmp_path):
    # No tocar procesos ajenos: la prueba exige que sus puertos estén libres.
    for port in (5000, 5001, 5002):
        with socket.socket() as probe:
            try:
                probe.bind(("127.0.0.1", port))
            except OSError:
                pytest.fail(
                    f"Port {port} is busy; stop your local exercise before this test"
                )
    processes = {}
    handles = []
    folders = {
        "gateway": ("api-gateway", 5000),
        "orders": ("onb-msa-sp-orders", 5001),
        "inventories": ("onb-msa-sp-inventories", 5002),
    }
    environment = {
        **os.environ,
        "ORDERS_SERVICE_URL": "http://127.0.0.1:5001",
        "INVENTORIES_SERVICE_URL": "http://127.0.0.1:5002",
        "API_GATEWAY_URL": "http://127.0.0.1:5000",
        "CONNECT_TIMEOUT": "1",
        "ORDERS_TIMEOUT": "10",
        "INVENTORIES_TIMEOUT": "2",
        "VALIDATION_TIMEOUT": "5",
        "PYTHONIOENCODING": "utf-8",
    }
    try:
        for name, (folder, port) in folders.items():
            handle = (tmp_path / f"{name}.log").open("w", encoding="utf-8")
            handles.append(handle)
            processes[name] = subprocess.Popen(
                [sys.executable, "-u", "app.py"],
                cwd=ROOT / folder,
                env=environment,
                stdout=handle,
                stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
            )
        deadline = time.monotonic() + 35
        for name, (_, port) in folders.items():
            while True:
                if processes[name].poll() is not None:
                    pytest.fail((tmp_path / f"{name}.log").read_text(encoding="utf-8"))
                try:
                    response = requests.get(
                        f"http://127.0.0.1:{port}/health", timeout=0.5
                    )
                    if response.status_code == 200:
                        break
                except requests.RequestException:
                    pass
                if time.monotonic() >= deadline:
                    pytest.fail(f"{name} did not start in time")
                time.sleep(0.1)
        yield processes, tmp_path
    finally:
        for process in processes.values():
            if process.poll() is None:
                process.terminate()
            process.wait(timeout=10)
        for handle in handles:
            handle.close()


def test_full_http_flow_and_failure_modes(system):
    processes, logs = system
    base = "http://127.0.0.1:5000"

    def create(product_id, quantity):
        response = requests.post(
            base + "/api/v1/orders",
            json={"product_id": product_id, "quantity": quantity},
            timeout=15,
        )
        assert response.status_code == 201
        return response.json()

    order = create(1, 2)
    assert order["status"] == "CONFIRMADO"
    assert requests.get(base + "/api/v1/inventories/1", timeout=5).json()["stock"] == 8
    assert (
        requests.get(base + f"/api/v1/orders/{order['id']}", timeout=5).json() == order
    )
    assert create(1, 99)["status"] == "RECHAZADO"
    assert create(999, 1)["reason"] == "Producto inexistente"
    assert requests.get(base + "/api/v1/inventories/1", timeout=5).json()["stock"] == 8
    before = requests.get(base + "/api/v1/orders", timeout=5).json()
    assert (
        requests.post(
            base + "/api/v1/orders", json={"product_id": 1, "quantity": True}, timeout=5
        ).status_code
        == 400
    )
    assert requests.get(base + "/api/v1/orders", timeout=5).json() == before
    assert (
        requests.get(base + f"/api/v1/orders/{uuid4()}", timeout=5).status_code == 404
    )

    # Repetir el descuento de un pedido confirmado no vuelve a consumir stock.
    deduction = {"order_id": order["id"], "product_id": 1, "quantity": 2}
    assert (
        requests.post(
            base + "/api/v1/inventories/deductions", json=deduction, timeout=5
        ).json()["remaining_stock"]
        == 8
    )
    conflict = requests.post(
        base + "/api/v1/inventories/deductions",
        json={**deduction, "quantity": 3},
        timeout=5,
    )
    assert conflict.status_code == 409
    assert conflict.json()["code"] == "IDEMPOTENCY_CONFLICT"

    with ThreadPoolExecutor(max_workers=12) as pool:
        orders = list(pool.map(lambda _: create(1, 1), range(12)))
    assert sum(item["status"] == "CONFIRMADO" for item in orders) == 8
    assert sum(item["status"] == "RECHAZADO" for item in orders) == 4
    assert requests.get(base + "/api/v1/inventories/1", timeout=5).json()["stock"] == 0
    gateway_log = (logs / "gateway.log").read_text(encoding="utf-8")
    assert 'POST /api/v1/inventories/deductions HTTP/1.1" 200' in gateway_log
    assert 'POST /api/v1/orders HTTP/1.1" 201' in gateway_log
    for port in (5000, 5001, 5002):
        assert (
            requests.get(f"http://127.0.0.1:{port}/docs", timeout=5).status_code == 200
        )
        assert (
            requests.get(f"http://127.0.0.1:{port}/openapi.yaml", timeout=5).status_code
            == 200
        )

    processes["inventories"].terminate()
    processes["inventories"].wait(timeout=10)
    failed = create(2, 1)
    assert failed["status"] == "ERROR_VALIDACION"
    unavailable = requests.get(base + "/api/v1/inventories", timeout=5)
    # Windows puede agotar la conexión antes de informar que el puerto está cerrado.
    assert (unavailable.status_code, unavailable.json()["code"]) in {
        (502, "SERVICE_UNAVAILABLE"),
        (504, "UPSTREAM_TIMEOUT"),
    }

    # Sustituto HTTP lento solo para comprobar el timeout real del gateway.
    class SlowInventory(BaseHTTPRequestHandler):
        def do_POST(self):
            self.rfile.read(int(self.headers.get("Content-Length", "0")))
            time.sleep(3)
            self.send_response(200)
            self.end_headers()

        def do_GET(self):
            time.sleep(3)
            self.send_response(200)
            self.end_headers()

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 5002), SlowInventory)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        started = time.monotonic()
        timed_out = create(2, 1)
        assert timed_out["status"] == "ERROR_VALIDACION"
        assert time.monotonic() - started < 10
        timeout = requests.get(base + "/api/v1/inventories", timeout=5)
        assert timeout.status_code == 504
        assert timeout.json()["code"] == "UPSTREAM_TIMEOUT"
        assert (
            requests.get(base + f"/api/v1/orders/{timed_out['id']}", timeout=5).json()
            == timed_out
        )
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
