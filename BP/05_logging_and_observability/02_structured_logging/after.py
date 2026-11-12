# Tema: serializar explícitamente los campos extra evita perder el contexto.
import json
import logging
from datetime import UTC, datetime


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        event = {
            "application": "orders-demo",
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "order_id": getattr(record, "order_id", None),
        }
        return json.dumps(event)


def main() -> None:
    logger = logging.getLogger("structured-demo")
    logger.handlers.clear()
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.info("Order created", extra={"order_id": "order-1"})


if __name__ == "__main__":
    main()
