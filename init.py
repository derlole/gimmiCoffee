from modules.persistence import save_dict
from datetime import datetime, UTC

# Defaults
water = {
    "lastFilled": str(datetime.now(UTC)),
    "fill": 100,
    "coffeesOnFill": 0
}

beans = {
    "lastFilled": str(datetime.now(UTC)),
    "fill": 100,
    "coffeesOnFill": 0
}

machine = {
    "state": "idle",
    "connected": False,
    "ready": False,
    "peding_command": False,
    "error": False,
    "lastConnectionProof": str(datetime.now(UTC))
}

# In JSON-Dateien speichern
save_dict("water", water)
save_dict("beans", beans)
save_dict("machine", machine)
