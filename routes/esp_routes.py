from flask import Blueprint, render_template, request, jsonify
from flask import Flask, jsonify, request
import paho.mqtt.client as mqtt
import json
import random
import sqlite3
import os
from modules.persistence import esp_conn_infos
import datetime
from modules.socketio import resend_static_data

esp = Blueprint('eps', __name__, url_prefix='/unsecure/esp')

DB_PATH = os.path.join(os.path.dirname(__file__), '../db/commands.db')

MQTT_BROKER = "localhost"  # oder IP/Domain
MQTT_PORT = 1883
MQTT_TOPIC = "coffee/command"


@esp.route('/online', methods=['POST'])
def esp_online():
    data = request.get_json()
    sender_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    esp_ip = data.get("ip", "unknown")

    esp_conn_infos["ip_local"] = esp_ip
    esp_conn_infos["ip_global"] = sender_ip
    esp_conn_infos["last_seen"] = datetime.now()
    esp_conn_infos["connection_valid"] = True
    resend_static_data()
    
    print(f"ESP ONLINE von IP: {esp_ip}, roher IP: {sender_ip}")
    return jsonify({"status": "ok"})

@esp.route('/toggle-machine', methods=['POST'])
def toggle_machine():
    print("ESP: toggle-machine")
    randID = random.randint(1000, 9999)
    fullCommand = {'command': 'toggle_machine', 'status': 'pending', 'command_id': randID}
    print("ESP: toggle-machine 1")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO commands (command, status, command_id)
        VALUES (?, ?, ?)
    """, (fullCommand["command"], fullCommand["status"], fullCommand["command_id"]))

    conn.commit()
    conn.close()
    print("ESP: toggle-machine 2")
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.publish(MQTT_TOPIC, json.dumps(fullCommand))
    client.disconnect()
    print("ESP: toggle-machine 3")
    return jsonify({"status": json.dumps(fullCommand)})