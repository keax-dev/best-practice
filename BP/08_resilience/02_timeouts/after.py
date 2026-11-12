# Tema: wait_for limita la espera de una operación que coopera con cancelación.
import asyncio


async def slow_operation() -> str:
    await asyncio.sleep(0.05)
    return "Catalog response"


async def fetch() -> str:
    try:
        return await asyncio.wait_for(slow_operation(), timeout=0.001)
    except TimeoutError:
        return "DEPENDENCY_TIMEOUT"


if __name__ == "__main__":
    print(asyncio.run(fetch()))
