
# from flask import Flask
# from flask_socketio import SocketIO, emit
# import threading
# import time


# app = Flask(__name__, static_url_path='/unsecure/static')
# # socketio = SocketIO(app, cors_allowed_origins="*")

# # data = {
# #     "test": 1,
# #     "status": "online",
# #     "counter": 0
# # }

# # def monitor_changes():
# #     while True:
# #         time.sleep(5)  # alle 5 Sekunden neue Daten senden
# #         data["test"] += 1
# #         data["counter"] += 5
# #         data["status"] = "busy" if data["counter"] % 2 == 0 else "idle"

# #         print("Neue Daten gesendet:", data)
# #         socketio.emit('update_data', data)


# # Blueprint registrieren
# app.register_blueprint(unsecure)

# if __name__ == '__main__':
#     # threading.Thread(target=monitor_changes).start()
#     app.run(host='0.0.0.0', port=3060)

import eventlet
eventlet.monkey_patch()  # Das sollte ganz oben sein, um sicherzustellen, dass eventlet alles patcht

from flask import Flask, render_template
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
from routes.unsecure_routes import unsecure

app = Flask(__name__, static_url_path='/unsecure/static')
socketio = SocketIO(app, cors_allowed_origins="*")

# MQTT Setup
mqtt_client = mqtt.Client(protocol=mqtt.MQTTv5)

# Funktion für den Empfang von MQTT-Nachrichten
def on_mqtt_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"[MQTT] {msg.topic}: {payload}")
    # Sende die erhaltenen MQTT-Daten über WebSocket an alle verbundenen Clients
    socketio.emit("esp_update", {"topic": msg.topic, "payload": payload})

mqtt_client.on_message = on_mqtt_message
mqtt_client.connect("localhost", 1883)  # MQTT-Broker-Adresse
mqtt_client.subscribe("lires/esp1/status")  # MQTT-Topic, das abonniert werden soll
mqtt_client.loop_start()  # Starten des MQTT-Client-Loops in einem separaten Thread

# Socket.IO → MQTT: Empfangene Daten von Socket.IO an MQTT senden
@socketio.on("send_to_esp")
def handle_send(data):
    mqtt_client.publish("lires/esp1/control", data)  # MQTT-Message senden

# Blueprint registrieren
app.register_blueprint(unsecure)

# Starten der Flask-SocketIO-Anwendung
if __name__ == '__main__':
    # Verwende socketio.run() statt app.run() für asynchrone WebSocket-Kommunikation
    socketio.run(app, host="0.0.0.0", port=3060)
