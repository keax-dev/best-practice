# Tema: cargar ejemplos numerados sin convertir las carpetas didácticas en paquetes.
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from uuid import uuid4

import pytest


@pytest.fixture
def load_example():
    modules = []
    inserted_paths = []

    def load(location, filename="after.py"):
        path = Path(location)
        if not path.is_absolute():
            path = Path(__file__).parent / path
        if path.is_file():
            path = path.parent
        path = path / filename
        name = f"lesson_{uuid4().hex}"
        spec = spec_from_file_location(name, path)
        module = module_from_spec(spec)
        sys.modules[name] = module
        modules.append(name)
        directory = str(path.parent)
        sys.path.insert(0, directory)
        inserted_paths.append(directory)
        spec.loader.exec_module(module)
        return module

    yield load
    for name in modules:
        sys.modules.pop(name, None)
    for directory in inserted_paths:
        sys.path.remove(directory)
