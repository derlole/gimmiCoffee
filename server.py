
from flask import Flask
from flask_socketio import SocketIO, emit
import threading
import time
from routes.unsecure_routes import unsecure

app = Flask(__name__, static_url_path='/unsecure/static')
# socketio = SocketIO(app, cors_allowed_origins="*")

# data = {
#     "test": 1,
#     "status": "online",
#     "counter": 0
# }

# def monitor_changes():
#     while True:
#         time.sleep(5)  # alle 5 Sekunden neue Daten senden
#         data["test"] += 1
#         data["counter"] += 5
#         data["status"] = "busy" if data["counter"] % 2 == 0 else "idle"

#         print("Neue Daten gesendet:", data)
#         socketio.emit('update_data', data)


# Blueprint registrieren
app.register_blueprint(unsecure)

if __name__ == '__main__':
    # threading.Thread(target=monitor_changes).start()
    app.run(host='0.0.0.0', port=3060)
