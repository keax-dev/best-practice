# Tema: comprobar archivos y enlaces locales sin ejecutar comandos de despliegue.
import ast
import json
import re
from pathlib import Path


def main() -> None:
    root = Path(__file__).parent
    catalog = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
    for item in catalog:
        directory = root / item["category"] / item["slug"]
        assert (directory / "definition.md").is_file(), directory
        for name in item["files"]:
            assert (directory / name).is_file(), (directory, name)
    for path in root.rglob("*.py"):
        if not any(part in {"node_modules", "target"} for part in path.parts):
            ast.parse(path.read_text(encoding="utf-8"))
    for path in root.rglob("*.md"):
        if any(part in {"node_modules", "target"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        for link in re.findall(r"\]\(([^)]+)\)", text):
            if "://" in link or link.startswith("#"):
                continue
            target = (path.parent / link.split("#")[0]).resolve()
            assert target.exists(), (path, link)
    print(f"Catalog, Python syntax and local links checked: {len(catalog)} lessons")


if __name__ == "__main__":
    main()
