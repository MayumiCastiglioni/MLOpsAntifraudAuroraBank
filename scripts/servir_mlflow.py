import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import subprocess
import config
subprocess.run([sys.executable,"-m","mlflow","server","--host","127.0.0.1","--port","5001","--backend-store-uri",config.URI_BANCO_MLFLOW,"--default-artifact-root",str(config.RAIZ/"mlruns")],check=True)
