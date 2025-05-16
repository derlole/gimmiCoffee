import network
from umqtt.simple import MQTTClient
from machine import Pin
import json
import time
import urequests

class CoffeeMachine:
    def __init__(self):
        # --- Eingänge ---
        self.an = Pin(5, Pin.IN, Pin.PULL_UP)
        self.bereit = Pin(4, Pin.IN, Pin.PULL_UP)
        self.fehler = Pin(14, Pin.IN, Pin.PULL_UP)
        self.bohnen_voll = Pin(12, Pin.IN, Pin.PULL_UP)
        self.wasser_voll = Pin(13, Pin.IN, Pin.PULL_UP)

        # --- Ausgänge ---
        self.toggle_machine = Pin(0, Pin.OUT)
        self.starten = Pin(15, Pin.OUT)

        # --- Status ---
        self.kaffee_machen = 0
        self.vorbereitung = 0
        self.kaffee_fertig = 0
        self.gestartet = 0

    def get_status(self):
        return {
            "an": self.an.value(),
            "bereit": self.bereit.value(),
            "fehler": self.fehler.value(),
            "bohnen_voll": self.bohnen_voll.value(),
            "wasser_voll": self.wasser_voll.value(),
            "einschalten": self.toggle_machine.value(),
            "starten": self.starten.value(),
            "kaffee_machen": self.kaffee_machen,
            "vorbereitung": self.vorbereitung,
            "kaffee_fertig": self.kaffee_fertig
        }

    def make_coffee(self):
        if self.kaffee_machen == 1:
            self.toggle_machine.value(1)
            time.sleep(1)
            self.toggle_machine.value(0)

        if (self.kaffee_machen == 1 and 
            self.an.value() == 1 and 
            self.bereit.value() == 1 and 
            self.fehler.value() == 0):
            self.starten.value(1)
            time.sleep(1)
            self.starten.value(0)
            self.gestartet = 1
        else:
            self.starten.value(0)
            self.gestartet = 0

    def update_status(self):
        if self.bereit.value() == 0 and self.an.value() == 1 and self.fehler.value() == 0:
            self.vorbereitung = 1

        if (self.bereit.value() == 1 and 
            self.an.value() == 1 and 
            self.fehler.value() == 0 and 
            self.gestartet == 1):
            self.kaffee_fertig = 1
            self.gestartet = 0
        else:
            self.kaffee_fertig = 0

class MQTTHandler:
    BROKER = "lires.de"
    PORT = 1883
    CLIENT_ID = "esp8266_coffee"
    TOPIC_STATUS = b"coffee/status"
    TOPIC_COMMAND = b"coffee/command"
    TOPIC_RETURN = b"coffee/return"
    
    def __init__(self, coffee_machine):
        self.coffee_machine = coffee_machine
        self.client = None

    def connect(self):
        self.client = MQTTClient(self.CLIENT_ID, self.BROKER, port=self.PORT)
        self.client.set_callback(self._callback)
        self.client.connect()
        print('MQTT verbunden')
        self.client.subscribe(self.TOPIC_COMMAND)

    def _callback(self, topic, msg):
        print('-------------------------')
        print('MQTT Nachricht empfangen:')
        print(f'Topic: {topic.decode()}')
        print(f'Payload: {msg.decode()}')
        print('-------------------------')
        try:
            command = json.loads(msg.decode())
            if topic == self.TOPIC_COMMAND:
                self._handle_command(command)
        except Exception as e:
            print('Fehler bei Kommando-Verarbeitung:', e)

    def _handle_command(self, command):
        if command.get('command') == 'toggle_machine':
            if self.coffee_machine.starten.value() == 0:
                command['status'] = 'served'
            self.client.publish(self.TOPIC_RETURN, json.dumps(command))
        
        elif command.get('command') == 'make_coffee':
            self.coffee_machine.kaffee_machen = 1
            self.client.publish(self.TOPIC_RETURN, json.dumps(command))

    def publish_status(self):
        if self.client:
            status = self.coffee_machine.get_status()
            self.client.publish(self.TOPIC_STATUS, json.dumps(status))

    def check_messages(self):
        if self.client:
            self.client.check_msg()

# Objekte erstellen
coffee_machine = CoffeeMachine()
mqtt_handler = MQTTHandler(coffee_machine)

# MQTT-Verbindung herstellen
try:
    mqtt_handler.connect()
except Exception as e:
    print('MQTT Verbindungsfehler:', e)

# Hauptschleife
while True:
    try:
        mqtt_handler.check_messages()
        mqtt_handler.publish_status()
        coffee_machine.make_coffee()
        coffee_machine.update_status()
        time.sleep(5)
    except Exception as e:
        print('Fehler in Hauptschleife:', e)
        time.sleep(5)