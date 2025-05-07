from flask import Flask
from routes.unsecure_routes import unsecure
from routes.esp_routes import esp
import threading
import time
import os
import paho.mqtt.client as mqtt
from datetime import datetime, timedelta
import sqlite3
from modules.persistence import load_dict, save_dict, esp_conn_infos
from modules.socketio import socketio, resend_static_data

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC_SUB = "coffee/status"
MQTT_TOPIC_SEND = "coffee/command"


app = Flask(__name__, static_url_path='/unsecure/static')
app.config['SECRET_KEY'] = 'super-secret-key'

socketio.init_app(app)


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

# MQTT-Thread
def mqtt_thread():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

# DB-Cleanup-Thread
def cleanup_old_commands():

    db_path = os.path.join(os.path.dirname(__file__), "db", "commands.db")

    while True:
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            five_minutes_ago = (datetime.utcnow() - timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute("""
                UPDATE commands
                SET status = 'failed'
                WHERE status = 'pending' AND tstamp <= ?
            """, (five_minutes_ago,))

            updated_rows = cursor.rowcount
            conn.commit()
            conn.close()

            if updated_rows > 0:
                print(f"[Cleanup] {updated_rows} Einträge als 'failed' markiert.")
        except Exception as e:
            print(f"[Cleanup-Fehler] {e}")

        time.sleep(60)  # jede Minute prüfen ob es pending Einträge gibt, die älter als 5 Minuten sind

# Clear commands DB
def clear_commands_db():
    import os
    import sqlite3

    db_path = os.path.join(os.path.dirname(__file__), "db", "commands.db")

    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM commands")
        conn.commit()
        conn.close()
        print("[DB] commands-Tabelle geleert.")
    else:
        print("[DB] Keine Datenbank gefunden – nichts geleert.")

# Motitior ESP-Connection
def monitor_esp_connection():
    while True:
        if esp_conn_infos["last_seen"]:
            time_diff = datetime.now() - esp_conn_infos["last_seen"]
            if time_diff > timedelta(minutes=30):
                esp_conn_infos["connection_valid"] = False
                resend_static_data()
        time.sleep(60)  # einmal pro Minute die Verbindung zum ESP prüfen

### THREADS START ###
threading.Thread(target=cleanup_old_commands, daemon=True).start()
threading.Thread(target=monitor_esp_connection, daemon=True).start()

#threading.Thread(target=mqtt_thread, daemon=True).start()

if __name__ == '__main__':
    #clear_commands_db()
    socketio.run(app, host='0.0.0.0', port=3060, allow_unsafe_werkzeug=True)

