# Tema: comprobar cuatro procesos reales y todo el recorrido HTTP.
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
    for port in (5000, 5001, 5002, 5003):
        with socket.socket() as probe:
            try:
                probe.bind(("127.0.0.1", port))
            except OSError:
                pytest.fail(
                    f"Port {port} is busy; stop your local exercise before this test"
                )
    key_directory = tmp_path / "keys"
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/setup_local.py"),
            "--directory",
            str(key_directory),
        ],
        check=True,
    )
    processes = {}
    handles = []
    folders = {
        "auth": ("onb-msa-sp-auth", 5003),
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
        "AUTH_SERVICE_URL": "http://127.0.0.1:5003",
        "AUTH_TIMEOUT": "3",
        "JWT_PRIVATE_KEY_FILE": str(key_directory / "jwt-private.pem"),
        "JWT_PUBLIC_KEY_FILE": str(key_directory / "jwt-public.pem"),
        "INTERNAL_API_KEY": (key_directory / "internal-api.key").read_text(),
        "ORDERS_SERVICE_KEY": (key_directory / "orders-service.key").read_text(),
        "JWT_ISSUER": "coe-auth",
        "JWT_AUDIENCE": "coe-backend",
        "JWT_ACCESS_TTL": "900",
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

    def login(username, password):
        response = requests.post(
            base + "/api/v1/auth/login",
            json={"username": username, "password": password},
            timeout=5,
        )
        assert response.status_code == 200
        session = requests.Session()
        session.headers["Authorization"] = "Bearer " + response.json()["access_token"]
        return session

    admin = login("admin", "Admin123!")
    customer = login("client", "Client123!")
    assert requests.get(base + "/api/v1/orders", timeout=5).status_code == 401
    assert (
        requests.post(
            base + "/api/v1/auth/login",
            json={"username": "client", "password": "wrong"},
            timeout=5,
        ).status_code
        == 401
    )
    for port, resource in [(5001, "orders"), (5002, "inventories")]:
        assert (
            requests.get(
                f"http://127.0.0.1:{port}/api/v1/{resource}",
                headers={
                    "Authorization": admin.headers["Authorization"],
                    "X-User-Id": "user-admin",
                    "X-User-Role": "ADMIN",
                },
                timeout=5,
            ).status_code
            == 401
        )

    def create(product_id, quantity, actor=admin):
        response = actor.post(
            base + "/api/v1/orders",
            json={"product_id": product_id, "quantity": quantity},
            timeout=15,
        )
        assert response.status_code == 201
        return response.json()

    order = create(1, 2)
    assert order["status"] == "CONFIRMADO"
    assert order["user_id"] == "user-admin"
    customer_order = create(2, 1, customer)
    assert customer_order["status"] == "CONFIRMADO"
    assert customer_order["user_id"] == "user-client"
    assert customer.get(base + "/api/v1/orders", timeout=5).json() == [customer_order]
    assert (
        customer.get(base + f"/api/v1/orders/{order['id']}", timeout=5).status_code
        == 404
    )
    assert (
        admin.get(
            base + f"/api/v1/orders/{customer_order['id']}", timeout=5
        ).status_code
        == 200
    )
    assert customer.get(base + "/api/v1/inventories", timeout=5).status_code == 403
    assert (
        customer.post(
            base + "/api/v1/inventories/deductions", json={}, timeout=5
        ).status_code
        == 403
    )
    assert (
        customer.post(
            base + "/api/v1/orders",
            json={"product_id": 2, "quantity": 1, "user_id": "user-admin"},
            timeout=5,
        ).status_code
        == 400
    )
    forged = customer.get(
        base + "/api/v1/orders",
        headers={
            "X-User-Id": "user-admin",
            "X-User-Role": "ADMIN",
            "X-Internal-Key": "fake",
        },
        timeout=5,
    )
    assert forged.json() == [customer_order]
    assert len(admin.get(base + "/api/v1/orders", timeout=5).json()) == 2
    assert admin.get(base + "/api/v1/inventories/1", timeout=5).json()["stock"] == 8
    assert admin.get(base + f"/api/v1/orders/{order['id']}", timeout=5).json() == order
    assert create(1, 99)["status"] == "RECHAZADO"
    assert create(999, 1)["reason"] == "Producto inexistente"
    assert admin.get(base + "/api/v1/inventories/1", timeout=5).json()["stock"] == 8
    before = admin.get(base + "/api/v1/orders", timeout=5).json()
    assert (
        admin.post(
            base + "/api/v1/orders", json={"product_id": 1, "quantity": True}, timeout=5
        ).status_code
        == 400
    )
    assert admin.get(base + "/api/v1/orders", timeout=5).json() == before
    assert admin.get(base + f"/api/v1/orders/{uuid4()}", timeout=5).status_code == 404

    # Repetir el descuento de un pedido confirmado no vuelve a consumir stock.
    deduction = {"order_id": order["id"], "product_id": 1, "quantity": 2}
    assert (
        admin.post(
            base + "/api/v1/inventories/deductions", json=deduction, timeout=5
        ).json()["remaining_stock"]
        == 8
    )
    conflict = admin.post(
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
    assert admin.get(base + "/api/v1/inventories/1", timeout=5).json()["stock"] == 0
    gateway_log = (logs / "gateway.log").read_text(encoding="utf-8")
    assert 'POST /api/v1/inventories/deductions HTTP/1.1" 200' in gateway_log
    assert 'POST /api/v1/orders HTTP/1.1" 201' in gateway_log
    for port in (5000, 5001, 5002, 5003):
        assert admin.get(f"http://127.0.0.1:{port}/docs", timeout=5).status_code == 200
        assert (
            admin.get(f"http://127.0.0.1:{port}/openapi.yaml", timeout=5).status_code
            == 200
        )

    processes["inventories"].terminate()
    processes["inventories"].wait(timeout=10)
    failed = create(2, 1)
    assert failed["status"] == "ERROR_VALIDACION"
    unavailable = admin.get(base + "/api/v1/inventories", timeout=5)
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
        timeout = admin.get(base + "/api/v1/inventories", timeout=5)
        assert timeout.status_code == 504
        assert timeout.json()["code"] == "UPSTREAM_TIMEOUT"
        assert (
            admin.get(base + f"/api/v1/orders/{timed_out['id']}", timeout=5).json()
            == timed_out
        )
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
