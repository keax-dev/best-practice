# Tema: ejecutar demostraciones Python independientes sin iniciar servidores.
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).parent
    examples = []
    for directory, subdirectories, files in root.walk():
        subdirectories[:] = [name for name in subdirectories if name not in {"node_modules", "target", ".venv"}]
        for name in ("before.py", "after.py", "example.py"):
            if name in files:
                examples.append(directory / name)
    order = {"before.py": 0, "after.py": 1, "example.py": 2}
    examples.sort(key=lambda path: (str(path.parent), order[path.name]))
    for path in examples:
        result = subprocess.run([sys.executable, "-B", str(path)], capture_output=True, encoding="utf-8", timeout=15)
        if result.returncode:
            print(f"FAILED: {path.relative_to(root)}")
            print(result.stdout, result.stderr)
            return result.returncode
        print(f"OK: {path.relative_to(root)}")
    print(f"Python demonstrations passed: {len(examples)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
