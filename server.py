

# import eventlet
# eventlet.monkey_patch()  # Das sollte ganz oben sein, um sicherzustellen, dass eventlet alles patcht

# from flask import Flask, render_template
# from flask_socketio import SocketIO
# import paho.mqtt.client as mqtt
# from routes.unsecure_routes import unsecure

# app = Flask(__name__, static_url_path='/unsecure/static')
# socketio = SocketIO(app, cors_allowed_origins="*")

# # MQTT Setup
# mqtt_client = mqtt.Client(protocol=mqtt.MQTTv5)

# def on_mqtt_message(client, userdata, msg):
#     payload = msg.payload.decode()
#     print(f"[MQTT] {msg.topic}: {payload}")
#     # Sende die erhaltenen MQTT-Daten über WebSocket an alle verbundenen Clients
#     socketio.emit("esp_update", {"topic": msg.topic, "payload": payload})

# mqtt_client.on_message = on_mqtt_message
# mqtt_client.connect("localhost", 1883)  # MQTT-Broker-Adresse
# mqtt_client.subscribe("lires/esp1/status") 
# mqtt_client.loop_start()  

# @socketio.on("send_to_esp")
# def handle_send(data):
#     mqtt_client.publish("lires/esp1/control", data)  

# app.register_blueprint(unsecure)

# if __name__ == '__main__':
#     socketio.run(app, host="0.0.0.0", port=3060)

from flask import Flask
from flask_socketio import SocketIO
from routes.unsecure_routes import unsecure
from routes.esp_routes import esp



app = Flask(__name__, static_url_path='/unsecure/static')
app.config['SECRET_KEY'] = 'super-secret-key'  # beliebig ändern
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')


# Blueprint registrieren
app.register_blueprint(unsecure)
app.register_blueprint(esp)

# Simuliere regelmäßige Daten-Updates
import threading
import time

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
