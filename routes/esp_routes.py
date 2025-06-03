from flask import Blueprint, request, jsonify
import paho.mqtt.client as mqtt
import json
import random
import sqlite3
import os
from modules.persistence import esp_conn_infos
from datetime import datetime
from modules.socketio import resend_static_data
from modules.persistence import load_dict, save_dict
from modules.db import create_toggle_machine, create_make_coffee

esp = Blueprint('eps', __name__, url_prefix='/unsecure/esp')

MQTT_BROKER = "localhost"  
MQTT_PORT = 1883
MQTT_TOPIC = "coffee/command"


@esp.route('/online', methods=['POST'])
def esp_online():
    """Endpoint to mark the ESP as online and update its connection info."""
    data = request.get_json()
    sender_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    esp_ip = data.get("ip", "unknown")

    esp_conn_infos["ip_local"] = esp_ip[0]
    esp_conn_infos["ip_global"] = sender_ip
    esp_conn_infos["last_seen"] = datetime.now()
    esp_conn_infos["connection_valid"] = True
    resend_static_data()
    return jsonify({"status": "ok"})

@esp.route('/toggle-machine', methods=['POST'])
def toggle_machine():
    """Endpoint to toggle the coffee machine state."""
    fullCommand = create_toggle_machine()

    new_status = load_dict("machine")
    new_status["state"] = "PENDING"
    save_dict("machine", new_status)

    
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.publish(MQTT_TOPIC, json.dumps(fullCommand))
    client.disconnect()

    return jsonify({"status": json.dumps(fullCommand)})

@esp.route('/make_coffee', methods=['POST'])
def make_coffee():
    """Endpoint to create a command to make coffee."""
    fullCommand = create_make_coffee()

    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.publish(MQTT_TOPIC, json.dumps(fullCommand))
    client.disconnect()

    return jsonify({"status": json.dumps(fullCommand)})