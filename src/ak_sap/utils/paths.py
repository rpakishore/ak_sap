from pathlib import Path

_this = Path(__file__)
dir_root: Path = _this.parent.parent
dir_src: Path = dir_root.parent
dir_test: Path = dir_src / "tests"
