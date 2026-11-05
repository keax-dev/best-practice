# Tema: ejecutar cada suite en su proceso para no mezclar paquetes llamados api.
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    for folder in ["api-gateway", "onb-msa-sp-orders", "onb-msa-sp-inventories", "."]:
        print(f"\nChecking {folder}", flush=True)
        subprocess.run(
            [sys.executable, "-m", "pytest", "test", "-q"],
            cwd=ROOT / folder,
            check=True,
        )


if __name__ == "__main__":
    main()
