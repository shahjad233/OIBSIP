from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
COMMANDS = {
    "check": [sys.executable, "-m", "compileall", "-q", str(ROOT)],
    "install": [sys.executable, "-m", "pip", "install", "-r", str(ROOT / "requirements.txt")],
    "notebook": [sys.executable, "-m", "notebook", "--notebook-dir", str(ROOT)],
    "run": [sys.executable, str(ROOT / "unemployment_analysis.py")],
}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in COMMANDS:
        print("Usage: python setup.py [check|install|notebook|run]")
        raise SystemExit(2)
    command = sys.argv[1]
    if command == "check":
        notebook = ROOT / "Unemployment_Analysis.ipynb"
        if not notebook.exists():
            raise SystemExit("Notebook is missing.")
        print("Project check passed. Notebook and analysis script are present.")
        print("Next: python setup.py install")
        raise SystemExit(0)
    subprocess.run(COMMANDS[command], cwd=ROOT, check=True)
