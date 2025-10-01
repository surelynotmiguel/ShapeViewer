import importlib
import subprocess
import sys

libs = ["pygame", "numpy", "psutil"]

def install():
    print("Checking and installing required libraries...")

    for lib in libs:
        try:
            importlib.import_module(lib)
            print(f"✅ {lib} is already installed.")
        except ImportError:
            print(f"⬇️ Installing {lib}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

    print("\nAll required libraries are installed.\n")
