import os
import json
from datetime import datetime

BASE_PATH = os.path.join(os.path.dirname(__file__), "..", "persistence")
BASE_PATH = os.path.abspath(BASE_PATH)


def save_dict(name, data):
    """Saves a dictionary to a JSON file."""
    path = os.path.join(BASE_PATH, f"{name}.json")
    os.makedirs(BASE_PATH, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, default=str, indent=2)

def load_dict(name):
    """Loads a dictionary from a JSON file.
    returns the data or an empty dict if the file does not exist."""
    path = os.path.join(BASE_PATH, f"{name}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}  # fallback falls Datei fehlt

# no persistence but global variable important for tracking the esp-connection over runtime
esp_conn_infos = {"ip_global": None, "ip_local": None, "last_seen": None, "connection_valid": False}