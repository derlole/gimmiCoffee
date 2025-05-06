from flask import Flask
from flask_socketio import SocketIO
from routes.unsecure_routes import unsecure
from routes.esp_routes import esp
import threading
import time
import paho.mqtt.client as mqtt

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC_SUB = "coffee/status"
MQTT_TOPIC_SEND = "coffee/command"

app = Flask(__name__, static_url_path='/unsecure/static')
app.config['SECRET_KEY'] = 'super-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Blueprints registrieren
app.register_blueprint(unsecure)
app.register_blueprint(esp)

# MQTT Callback-Funktionen
def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Verbunden mit Code {rc}")
    client.subscribe(MQTT_TOPIC_SUB)
    print(f"[MQTT] Subscribed to topic: {MQTT_TOPIC_SUB}")

def on_message(client, userdata, msg):
    print(f"[MQTT] Nachricht empfangen: {msg.topic} -> {msg.payload.decode()}")
    # Optional an Clients senden
    socketio.emit('mqtt_message', {
        'topic': msg.topic,
        'message': msg.payload.decode()
    })

# MQTT-Thread starten
def mqtt_thread():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

# Dummy-Daten-Thread
# def send_data():
#     counter = 0
#     while True:
#         data = {
#             'test': 'Live-Daten',
#             'status': 'OK',
#             'counter': counter
#         }
#         socketio.emit('update_data', data)
#         counter += 1
#         time.sleep(2)

# Beide Threads starten
#threading.Thread(target=send_data, daemon=True).start()


#threading.Thread(target=mqtt_thread, daemon=True).start()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3060, allow_unsafe_werkzeug=True)
