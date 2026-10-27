"""Load only an explicitly selected, trusted forward-evaluation output."""

import importlib.util
import os
from pathlib import Path
import sys


def load_service():
    location = os.environ.get("SAFE_API_EVAL_PROJECT")
    if not location:
        raise RuntimeError("Set SAFE_API_EVAL_PROJECT to the trusted completed fixture")
    root = Path(location).resolve()
    source = root / "service.py"
    if not source.is_file():
        raise RuntimeError("Selected fixture must contain service.py")
    sys.path.insert(0, str(root))
    spec = importlib.util.spec_from_file_location("evaluated_service", source)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module
