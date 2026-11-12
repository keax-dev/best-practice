# Tema: comprobar límites de recursos, seguridad y fallos de integración sin red real.
import asyncio
import json
import logging
from unittest.mock import Mock

import pytest


@pytest.mark.parametrize("value", [True, False, 0, -1, "2", None, 1.5])
def test_invalid_quantity_is_not_accepted(load_example, value):
    module = load_example("01_python_standards/04_conditions_and_comparisons")
    assert module.is_valid_quantity(value) is False


@pytest.mark.parametrize("value", ["nan", "inf", "-1", "0", "coffee"])
def test_invalid_configuration_is_rejected(load_example, value):
    module = load_example("04_configuration_and_security/03_configuration_validation")
    with pytest.raises(ValueError):
        module.parse_timeout(value)


def test_secrets_do_not_appear_in_representation_or_event(load_example):
    credentials = load_example("04_configuration_and_security/04_secrets_management")
    assert "demo-secret" not in repr(credentials.load_credentials({"APP_ACCESS_TOKEN": "demo-secret"}))
    with pytest.raises(ValueError):
        credentials.load_credentials({})
    logs = load_example("05_logging_and_observability/04_sensitive_data_masking")
    event = logs.safe_event({"order_id": "order-1", "token": "demo-secret", "nested": {"password": "demo-password"}})
    assert event == {"event": "order_received", "order_id": "order-1"}


def test_structured_formatter_preserves_selected_context(load_example):
    module = load_example("05_logging_and_observability/02_structured_logging")
    record = logging.LogRecord("demo", logging.INFO, "example.py", 1, "Order created", (), None)
    record.order_id = "order-1"
    data = json.loads(module.JsonFormatter().format(record))
    assert data["order_id"] == "order-1"
    assert data["level"] == "INFO"
    assert data["timestamp"].endswith("+00:00")


def test_correlation_context_is_restored(load_example):
    module = load_example("05_logging_and_observability/03_correlation_ids")
    assert module.process("first") == ["first received", "first completed"]
    assert module.process("second") == ["second received", "second completed"]
    assert module.correlation_id.get() == "none"


def test_cache_evicts_and_expires_at_boundary(load_example):
    module = load_example("06_resources_and_performance/03_bounded_cache")
    now = [0.0]
    cache = module.BoundedCache(2, 5.0, lambda: now[0])
    cache.put("one", "A")
    cache.put("two", "B")
    cache.put("three", "C")
    assert cache.get("one") is None
    assert cache.get("three") == "C"
    now[0] = 5.0
    assert cache.get("three") is None


def test_resource_is_closed_after_error(load_example):
    module = load_example("06_resources_and_performance/01_context_managers")
    assert module.demonstrate() is True


@pytest.mark.parametrize("ttl", [0, -1, float("nan"), float("inf")])
def test_invalid_cache_expiration_is_rejected(load_example, ttl):
    module = load_example("06_resources_and_performance/03_bounded_cache")
    with pytest.raises(ValueError):
        module.BoundedCache(2, ttl, lambda: 0.0)


def test_liveness_does_not_depend_on_remote_availability(load_example):
    module = load_example("08_resilience/01_liveness_and_readiness")
    state = module.HealthState(True, True, False)
    assert module.liveness(state) is True
    assert module.readiness(state) is False


def test_cooperative_operation_times_out(load_example):
    module = load_example("08_resilience/02_timeouts")
    assert asyncio.run(module.fetch()) == "DEPENDENCY_TIMEOUT"


def test_retry_has_limited_attempts_and_exponential_backoff(load_example):
    module = load_example("08_resilience/03_safe_retries")
    operation = Mock(side_effect=[ConnectionError("one"), ConnectionError("two"), "OK"])
    delays = []
    assert module.retry_read(operation, sleep=delays.append, jitter=lambda: 0) == "OK"
    assert operation.call_count == 3
    assert delays == [0.01, 0.02]


def test_retry_does_not_repeat_business_errors(load_example):
    module = load_example("08_resilience/03_safe_retries")
    operation = Mock(side_effect=ValueError("Invalid input"))
    with pytest.raises(ValueError):
        module.retry_read(operation, sleep=lambda delay: None)
    assert operation.call_count == 1


def test_retry_stops_after_last_transient_failure(load_example):
    module = load_example("08_resilience/03_safe_retries")
    operation = Mock(side_effect=ConnectionError("Unavailable"))
    with pytest.raises(ConnectionError):
        module.retry_read(operation, attempts=2, sleep=lambda delay: None, jitter=lambda: 0)
    assert operation.call_count == 2


def test_fallback_marks_stale_information(load_example):
    module = load_example("08_resilience/04_fallbacks")
    result = module.get_catalog(Mock(side_effect=ConnectionError()), ("Coffee",))
    assert result.products == ("Coffee",)
    assert result.stale is True
    assert module.get_catalog(lambda: ("Tea",), ("Coffee",)).stale is False


def test_open_circuit_skips_call_and_can_recover(load_example):
    module = load_example("08_resilience/05_circuit_breaker")
    now = [0.0]
    circuit = module.CircuitBreaker(lambda: now[0], threshold=1, cooldown=5)
    operation = Mock(side_effect=ConnectionError())
    with pytest.raises(ConnectionError):
        circuit.call(operation)
    with pytest.raises(module.CircuitOpenError):
        circuit.call(operation)
    assert operation.call_count == 1
    now[0] = 5.0
    assert circuit.call(lambda: "OK") == "OK"
    assert circuit.state == "CLOSED"


def test_failed_half_open_probe_reopens_circuit(load_example):
    module = load_example("08_resilience/05_circuit_breaker")
    now = [0.0]
    circuit = module.CircuitBreaker(lambda: now[0], threshold=1, cooldown=5)
    failure = Mock(side_effect=ConnectionError())
    with pytest.raises(ConnectionError):
        circuit.call(failure)
    now[0] = 5.0
    with pytest.raises(ConnectionError):
        circuit.call(failure)
    assert circuit.state == "OPEN"
    with pytest.raises(module.CircuitOpenError):
        circuit.call(failure)
    assert failure.call_count == 2


def test_flag_changes_only_the_selected_behavior(load_example):
    module = load_example("08_resilience/06_feature_flags")
    flags = module.FeatureFlags()
    assert module.checkout_label(flags) == "Classic checkout"
    flags.new_checkout = True
    assert module.checkout_label(flags) == "New checkout"
