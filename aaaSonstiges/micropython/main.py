from umqtt.simple import MQTTClient
from machine import Pin
import json
import time

# MQTT-Konfiguration
MQTT_BROKER = "broker.hivemq.com"  # oder Ihr eigener MQTT Broker
MQTT_PORT = 1883
MQTT_CLIENT_ID = "esp8266_coffee"
MQTT_TOPIC_STATUS = b"coffee/status"
MQTT_TOPIC_COMMAND = b"coffee/command"

# --- Eingänge ---
an = Pin(5, Pin.IN)
bereit = Pin(4, Pin.IN)
fehler = Pin(14, Pin.IN)
bohnen_voll = Pin(12, Pin.IN)
Wasser_voll = Pin(13, Pin.IN)
# --- Ausgänge ---
einschalten = Pin(0, Pin.OUT)
starten = Pin(15, Pin.OUT)

def mqtt_callback(topic, msg):
    print('Empfangen:', topic, msg)
    try:
        command = json.loads(msg.decode())
        if topic == MQTT_TOPIC_COMMAND:
            if 'einschalten' in command:
                einschalten.value(command['einschalten'])
            if 'starten' in command:
                starten.value(command['starten'])
    except Exception as e:
        print('Fehler bei Kommando-Verarbeitung:', e)

def connect_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.set_callback(mqtt_callback)
    client.connect()
    print('MQTT verbunden')
    client.subscribe(MQTT_TOPIC_COMMAND)
    return client

# MQTT-Verbindung herstellen
try:
    client = connect_mqtt()
except Exception as e:
    print('MQTT Verbindungsfehler:', e)
    client = None

# Hauptschleife
while True:
    try:
        if client:
            client.check_msg()  # Prüfe auf neue MQTT-Nachrichten
            
            # Status senden
            status = {
                # ---IOs---
                "an": an.value(),
                "bereit": bereit.value(),
                "fehler": fehler.value(),
                "bohnen_voll": bohnen_voll.value(),
                "wasser_voll": Wasser_voll.value(),
                "einschalten": einschalten.value(),
                "starten": starten.value(),
                # ---komunikation---
                "kaffee_machen": kaffe_machen.value(),
                "vorbereitung": vorbereitung.value(),
                "kaffee_fertig": kaffee_fertig.value(),
                
            }
            client.publish(MQTT_TOPIC_STATUS, json.dumps(status))
        else:
            # Versuche Neuverbindung
            try:
                client = connect_mqtt()
            except:
                pass
                
        time.sleep(1)
        
    except Exception as e:
        print('Fehler in Hauptschleife:', e)
        time.sleep(5)
        client = None
            #Einschalten der Kaffeemaschine
            if (kaffe_machen.value() == 1)
            {
                einschalten = 1
                delay(1000);
                einschalten=0
            }
            
            #Starten der Kaffeemaschine
            
            if (kaffe_machen.value() == 1 && bereit == 1&&fehler==0)
            {
                starten = 1
                delay(1000)
                starten=0
                gestartet =1
            }
            else
            {
                starten = 0
                gestartet = 0
            }
            #Vorbereitung der Kaffeemaschine
            if (bereit == 0&&an==1&&fehler==0)
            {
                vorbereitung.value()=1 
            }
            else
            {
                vorbereitung.value()=0
            }
            #Kaffeemaschine fertig
            if (bereit == 1&&an==1&&fehler==0&& gestartet==1)
            {
                kaffee_fertig.value()=1
                gestartet = 0
            }
            else
            {
                kaffee_fertig.value()=0
            }

            #Fehlerbehandlung
            if(fehler==1)
            {
                fehler.value()=1
            }   
            else
            {
                fehler.value()=0
            }
    if (bohnen_voll == 1)
    {
        bohnen_voll.value()=1
    }
    if (Wasser_voll == 1)
    {
        Wasser_voll.value()=1
    }
    

            
            
                