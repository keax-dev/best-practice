# Tema: una espera sin límite depende por completo de la operación.
import asyncio

async def fetch() -> str:
    return "Catalog response"

if __name__ == "__main__":
    print(asyncio.run(fetch()))
