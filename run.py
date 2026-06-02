from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    # 패키지를 pip install 하지 않아도 소스 체크아웃에서 바로 실행할 수 있게 src 경로를 추가한다.
    # run.py는 개발자가 더블클릭/터미널 실행할 때 쓰는 가장 단순한 진입점이다.
    sys.path.insert(0, str(SRC))

from universe.main import run


if __name__ == "__main__":
    run()
