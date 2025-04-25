from flask import Blueprint, render_template, request, jsonify
import routes.shared as shared
from flask import Flask, jsonify, request
import paho.mqtt.client as mqtt
import json
esp = Blueprint('eps', __name__, url_prefix='/unsecure/esp')

MQTT_BROKER = "localhost"  # oder IP/Domain
MQTT_PORT = 1883
MQTT_TOPIC = "iot/machine"

@esp.route('/')
def fetch_command():
    pCd = shared.pending_command
    shared.reset_command()
    return jsonify(pCd)

@esp.route('/toggle-machine', methods=['POST'])
def toggle_machine():
    pCd = shared.pending_command
    pCd['command'] = 'machineToggle'
    pCd['command-URL'] = 'NO_URL'
    pCd['command-expected'] = 'machineStatusResponse'
    pCd['command-expected-URL'] = 'http://lires.de/unsecure/esp/machine-status'

    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.publish(MQTT_TOPIC, json.dumps(pCd))
    client.disconnect()

    return jsonify({"status": json.dumps(pCd)})