from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    # Support running from a source checkout without installing the package first.
    sys.path.insert(0, str(SRC))

from universe.main import run


if __name__ == "__main__":
    run()
