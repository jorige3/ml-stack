import os
import subprocess

def _get_wsl_host_ip():
    try:
        result = subprocess.run(
            ["ip", "route", "show", "default"],
            capture_output=True, text=True, timeout=2
        )
        return result.stdout.split()[2]
    except Exception:
        return "127.0.0.1"

OLLAMA_URL = os.getenv("OLLAMA_URL", f"http://{_get_wsl_host_ip()}:11434")
