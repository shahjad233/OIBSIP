from pathlib import Path
import subprocess, sys

ROOT = Path(__file__).resolve().parent
REQ = ROOT / "requirements.txt"
NOTEBOOK = ROOT / "Car_Price_Prediction.ipynb"

def run(args):
    subprocess.check_call(list(map(str, args)), cwd=ROOT)

def check():
    modules = ["numpy", "pandas", "matplotlib", "seaborn", "sklearn", "jupyter", "joblib"]
    failed = []
    for module in modules:
        try:
            __import__(module)
            print("[OK]", module)
        except Exception as exc:
            print("[MISSING]", module, "-", exc)
            failed.append(module)
    for path in [NOTEBOOK, ROOT/"data"/"sample_car_data.csv"]:
        print("[OK]" if path.exists() else "[MISSING]", path.name)
    if failed:
        print("Run: python setup.py install")
        return 1
    print("Environment check passed.")
    return 0

def help_text():
    print("Commands:\\n  python setup.py install\\n  python setup.py check\\n  python setup.py notebook")

if __name__ == "__main__":
    cmd = sys.argv[1].lower() if len(sys.argv)>1 else "help"
    if cmd == "install":
        run([sys.executable,"-m","pip","install","--upgrade","pip"])
        run([sys.executable,"-m","pip","install","-r",REQ])
    elif cmd == "check":
        sys.exit(check())
    elif cmd == "notebook":
        run([sys.executable,"-m","jupyter","notebook",NOTEBOOK])
    else:
        help_text()
