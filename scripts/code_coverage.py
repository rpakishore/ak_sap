import tempfile
from pathlib import Path
import webbrowser
import subprocess
import shutil

# Run Pytest Coverage Report
code_coverage_path = Path(tempfile.gettempdir()) / "code_coverage_report"


cmd = [
    "uv",
    "run",
    "--group",
    "test",
    "pytest",
    "--cov=ak_sap",
    f"--cov-report=html:{code_coverage_path}",
]
print(" ".join(cmd))
subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()

webbrowser.open(f"file://{code_coverage_path}/index.html")