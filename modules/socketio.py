# extensions.py
from flask_socketio import SocketIO
from modules.persistence import esp_conn_infos,load_dict, save_dict

socketio = SocketIO(cors_allowed_origins="*", async_mode='threading')

def resend_static_data():
    water = load_dict("water")
    beans = load_dict("beans")
    machine = load_dict("machine")
    socketio.emit('static_data', {
        'water': water,
        'beans': beans,
        'machine': machine,
        'esp_conn_infos': esp_conn_infos
})
