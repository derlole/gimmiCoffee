
# from flask import Flask
# from flask_socketio import SocketIO, emit
# import threading
# import time
from routes.unsecure_routes import unsecure

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


from flask import Flask, render_template
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt

app = Flask(__name__, static_url_path='/unsecure/static')
socketio = SocketIO(app, cors_allowed_origins="*")

# MQTT Setup
mqtt_client = mqtt.Client()

def on_mqtt_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"[MQTT] {msg.topic}: {payload}")
    socketio.emit("esp_update", {"topic": msg.topic, "payload": payload})

mqtt_client.on_message = on_mqtt_message
mqtt_client.connect("localhost", 1883)
mqtt_client.subscribe("lires/esp1/status")
mqtt_client.loop_start()

# Socket.IO → MQTT
@socketio.on("send_to_esp")
def handle_send(data):
    mqtt_client.publish("lires/esp1/control", data)

app.register_blueprint(unsecure)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=3060)

