from flask import Blueprint, render_template, request, jsonify
from flask import Flask, jsonify, request
import paho.mqtt.client as mqtt
import json
import random
import sqlite3
import os
from modules.persistence import esp_conn_infos
from datetime import datetime, timedelta
from modules.socketio import resend_static_data
from modules.persistence import load_dict, save_dict
from modules.db import create_toggle_machine, create_make_coffee

esp = Blueprint('eps', __name__, url_prefix='/unsecure/esp')

MQTT_BROKER = "localhost"  # oder IP/Domain
MQTT_PORT = 1883
MQTT_TOPIC = "coffee/command"


@esp.route('/online', methods=['POST'])
def esp_online():
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
    fullCommand = create_make_coffee()

    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.publish(MQTT_TOPIC, json.dumps(fullCommand))
    client.disconnect()

    return jsonify({"status": json.dumps(fullCommand)})