from __future__ import annotations

from pathlib import Path
import runpy
import sys


if __name__ == "__main__":
    src_path = Path(__file__).resolve().parent / "src"
    sys.path.insert(0, str(src_path))
    runpy.run_path(str(src_path / "main.py"), run_name="__main__")