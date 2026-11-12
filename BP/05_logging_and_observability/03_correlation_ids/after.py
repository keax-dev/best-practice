# Tema: un contexto por operación mantiene el mismo identificador sin fugas.
from contextvars import ContextVar

correlation_id: ContextVar[str] = ContextVar("correlation_id", default="none")


def process(request_id: str) -> list[str]:
    token = correlation_id.set(request_id)
    try:
        return [f"{correlation_id.get()} received", f"{correlation_id.get()} completed"]
    finally:
        correlation_id.reset(token)


if __name__ == "__main__":
    print(*process("request-1"), sep="\n")
    print(f"After request: {correlation_id.get()}")
