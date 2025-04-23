from flask import Flask
from flask_socketio import SocketIO
from routes.unsecure_routes import unsecure
from routes.esp_routes import esp
import threading
import time


app = Flask(__name__, static_url_path='/unsecure/static')
app.config['SECRET_KEY'] = 'super-secret-key'  # beliebig ändern
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')


# Blueprint registrieren
app.register_blueprint(unsecure)
app.register_blueprint(esp)

# Simuliere regelmäßige Daten-Updates

def send_data():
    counter = 0
    while True:
        #print(f"Sending data: {counter}")
        data = {
            'test': 'Live-Daten',
            'status': 'OK',
            'counter': counter
        }
        socketio.emit('update_data', data)
        counter += 1
        time.sleep(2)  # alle 2 Sekunden neue Daten

# Hintergrund-Thread starten
thread = threading.Thread(target=send_data)
thread.daemon = True
thread.start()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3060, allow_unsafe_werkzeug=True)
