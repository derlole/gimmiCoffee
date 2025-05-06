from flask import Blueprint, render_template, request, jsonify
import routes.shared as shared
from flask import Flask, jsonify, request
import paho.mqtt.client as mqtt
import json
import random
import sqlite3
import os

esp = Blueprint('eps', __name__, url_prefix='/unsecure/esp')

DB_PATH = os.path.join(os.path.dirname(__file__), '../db/commands.db')

MQTT_BROKER = "localhost"  # oder IP/Domain
MQTT_PORT = 1883
MQTT_TOPIC = "coffee/command"

@esp.route('/')
def fetch_command():
    pCd = shared.pending_command
    shared.reset_command()
    return jsonify(pCd)

@esp.route('/online', methods=['POST'])
def esp_online():
    data = request.get_json()
    sender_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    esp_ip = data.get("ip", "unknown")

    print(f"ESP ONLINE von IP: {esp_ip}, roher IP: {sender_ip}")
    return jsonify({"status": "ok"})

@esp.route('/toggle-machine', methods=['GET'])
def toggle_machine():
    randID = random.randint(1000, 9999)
    fullCommand = {'command': 'toggle_machine', 'status': 'pending', 'command_id': randID}

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO commands (command, status, command_id)
        VALUES (?, ?, ?)
    """, (fullCommand["command"], fullCommand["status"], fullCommand["command_id"]))

    conn.commit()
    conn.close()

    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.publish(MQTT_TOPIC, json.dumps(fullCommand))
    client.disconnect()

    return jsonify({"status": json.dumps(fullCommand)})