
from flask_socketio import SocketIO
from modules.persistence import esp_conn_infos,load_dict, save_dict
from datetime import datetime


socketio = SocketIO(cors_allowed_origins="*", async_mode='threading')

# function to change the datetime format to isoformat because json does not support datetime
def convert_datetimes(obj):
    """Convert datetime objects in a dict or list to a specific string format."""
    if isinstance(obj, dict):
        return {k: convert_datetimes(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_datetimes(i) for i in obj]
    elif isinstance(obj, datetime):
        return obj.strftime("%d.%m.%Y %H:%M")
    else:
        return obj


def resend_static_data():
    """Resend static data to the frontend via SocketIO."""
    water = load_dict("water")
    beans = load_dict("beans")
    machine = load_dict("machine")
    esp_info = convert_datetimes(esp_conn_infos)
    socketio.emit('static_data', {
        'water': water,
        'beans': beans,
        'machine': machine,
        'esp_conn_infos': esp_info
})
