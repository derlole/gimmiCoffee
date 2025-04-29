from flask import Blueprint, render_template, request, jsonify
import routes.shared as shared
from flask import Flask, jsonify, request
import paho.mqtt.client as mqtt
import json
esp = Blueprint('eps', __name__, url_prefix='/unsecure/esp')

MQTT_BROKER = "localhost"  # oder IP/Domain
MQTT_PORT = 1883
MQTT_TOPIC = "coffee/command"

@esp.route('/')
def fetch_command():
    pCd = shared.pending_command
    shared.reset_command()
    return jsonify(pCd)

@esp.route('/toggle-machine', methods=['GET'])
def toggle_machine():

    testData = {'test': 'Live-Daten', 'status': 'OK', 'counter': 0}
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.publish(MQTT_TOPIC, json.dumps(testData))
    client.disconnect()

    return jsonify({"status": json.dumps(testData)})