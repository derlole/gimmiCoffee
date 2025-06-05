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
from modules.db import update_command_status
import json
from modules.other import refactor_and_use_esp_data

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC_SUB = "coffee/status"
MQTT_TOPIC_SEND = "coffee/command"
MQTT_TOPIC_RETURN = "coffee/return"


app = Flask(__name__, static_url_path='/unsecure/static')
app.config['SECRET_KEY'] = 'super-secret-key'

socketio.init_app(app, cors_allowed_origins="*", async_mode='threading')


# Blueprints registrieren
app.register_blueprint(unsecure)
app.register_blueprint(esp)

# MQTT Callback-Funktionen
def on_connect(client, userdata, flags, rc):
    """Callback-Funktion, die aufgerufen wird, wenn der Client sich mit dem Broker verbindet."""
    print(f"[MQTT] Verbunden mit Code {rc}")
    client.subscribe(MQTT_TOPIC_SUB)
    client.subscribe(MQTT_TOPIC_RETURN)
    print(f"[MQTT] Subscribed to topic: {MQTT_TOPIC_RETURN}")
    print(f"[MQTT] Subscribed to topic: {MQTT_TOPIC_SUB}")

def on_message(client, userdata, msg):
    """Callback-Funktion, die aufgerufen wird, wenn eine Nachricht empfangen wird."""
    if msg.topic == MQTT_TOPIC_SUB:
        print(f"[MQTT] Nachricht empfangen: {msg.topic} -> {msg.payload.decode()}")
        esp_conn_infos["last_seen"] = datetime.now()
        refactor_and_use_esp_data(msg.payload.decode()) # form modules other
    elif msg.topic == MQTT_TOPIC_RETURN:
        print(f"[MQTT] Nachricht empfangen: {msg.topic} -> {msg.payload.decode()}")
        try:
            payload = json.loads(msg.payload.decode())
            command_id = payload.get("command_id")
            if command_id:
                update_command_status(command_id, "served") # form modules db
            else:
                print("[MQTT] Keine command_id im Payload gefunden.")
        except json.JSONDecodeError as e:
            print(f"[MQTT] Fehler beim Dekodieren der Nachricht: {e}")
    else:
        print(f"[MQTT] Unbekanntes Topic: {msg.topic}")
        return
    
# MQTT-Thread
def mqtt_thread():
    """Thread, der die MQTT-Verbindung aufbaut und Nachrichten verarbeitet."""
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

# DB-Cleanup-Thread
def cleanup_old_commands():
    """Thread, der alle 5 Minuten die Datenbank nach 'pending' Befehlen durchsucht und diese auf 'failed' setzt, wenn sie älter als 5 Minuten sind."""
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
    """Löscht alle Einträge in der commands- und coffee-Tabelle der Datenbank."""
    import os
    import sqlite3

    db_path_command = os.path.join(os.path.dirname(__file__), "db", "commands.db")
    db_path_coffee = os.path.join(os.path.dirname(__file__), "db", "coffee.db")

    if os.path.exists(db_path_command):
        conn = sqlite3.connect(db_path_command)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM commands")
        conn.commit()
        conn.close()
        print("[DB] commands-Tabelle geleert.")
        conn = sqlite3.connect(db_path_coffee)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM coffee")
        conn.commit()
        conn.close()
        print("[DB] coffee-Tabelle geleert.")
    else:
        print("[DB] Keine Datenbank gefunden – nichts geleert.")

# Motitior ESP-Connection
def monitor_esp_connection():
    """Überwacht die Verbindung zum ESP und setzt die Verbindung auf ungültig, wenn der ESP länger als 3 Minuten nicht gesehen wurde."""
    while True:
        if esp_conn_infos["last_seen"]:
            time_diff = datetime.now() - esp_conn_infos["last_seen"]
            if time_diff > timedelta(minutes=3):
                esp_conn_infos["connection_valid"] = False
                resend_static_data()
        time.sleep(60)  # einmal pro Minute die Verbindung zum ESP prüfen

### THREADS START ###
threading.Thread(target=cleanup_old_commands, daemon=True).start()
threading.Thread(target=monitor_esp_connection, daemon=True).start()

threading.Thread(target=mqtt_thread, daemon=True).start()

if __name__ == '__main__':
    #
    #clear_commands_db()
    socketio.run(app, host='0.0.0.0', port=3060, allow_unsafe_werkzeug=True)

