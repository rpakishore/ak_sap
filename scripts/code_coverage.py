import subprocess
import tempfile
import webbrowser
from pathlib import Path

# Run Pytest Coverage Report
code_coverage_path = Path(tempfile.gettempdir()) / "code_coverage_report"


def run_cmd(cmd: list[str]):
    print(" ".join(cmd))
    subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).wait()


run_cmd(cmd=["uv", "run", "ruff", "format"])
run_cmd(cmd=["uv", "run", "ruff", "check", "--select", "I", "-e", "--fix"])
run_cmd(cmd=["uv", "run", "ruff", "check", "--fix", ">&1"])

run_cmd(
    cmd=[
        "uv",
        "run",
        "--group",
        "test",
        "pytest",
        "--cov=template_python",
        f"--cov-report=html:{code_coverage_path}",
    ]
)
webbrowser.open(f"file://{code_coverage_path}/index.html")

run_cmd(cmd=["uv", "run", "--group", "test", "pytest"])
