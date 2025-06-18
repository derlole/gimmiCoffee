import network
from umqtt.simple import MQTTClient
from machine import Pin
import json
import time
import urequests

# MQTT-Konfiguration
MQTT_BROKER = "lires.de"  
MQTT_PORT = 1884
MQTT_CLIENT_ID = "esp8266_coffee"
MQTT_TOPIC_STATUS = b"coffee/status"
MQTT_TOPIC_COMMAND = b"coffee/command"
MQTT_TOPIC_RETURN = b"coffee/return"

# Other Constants
SERVER_URL = "http://lires.de/unsecure/esp/online"

# --- Eingänge ---
an = Pin(5, Pin.IN)
bereit = Pin(4, Pin.IN)
fehler = Pin(14, Pin.IN)
bohnen_voll = Pin(12, Pin.IN)
Wasser_voll = Pin(13, Pin.IN)

# --- Ausgänge ---
einschalten = Pin(0, Pin.OUT)
starten = Pin(15, Pin.OUT)
einschalten.value(1)
starten.value(1)
# --- Status ---
toggle_machine=0
gestartet = 0

make_coffee= 0
counter_negirp=0
kaffee_fertig = 0
in_process = 0
counter=0


def mqtt_callback(topic, msg):
    print('-------------------------')
    print('MQTT Nachricht empfangen:')
    print(f'Topic: {topic.decode()}')
    print(f'Payload: {msg.decode()}')
    print('-------------------------')
    try:
        global toggle_machine, make_coffee, kaffee_fertig, gestartet, in_process
        command = json.loads(msg.decode())
        if topic == MQTT_TOPIC_COMMAND:
            if  command['command']=='toggle_machine':
                
                toggle_machine=1
                if gestartet == 1:
                    command['status']='served'
                   
                print(command)
                client.publish(MQTT_TOPIC_RETURN, json.dumps(command))
                
            if  command['command']=='make_coffee':
                kaffee_machen=1
               
                if kaffee_fertig==1:
                    print(command)
                    client.publish(MQTT_TOPIC_RETURN, json.dumps(command))

    except Exception as e:
        print('Fehler bei Kommando-Verarbeitung:', e)

def connect_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.set_callback(mqtt_callback)
    client.connect()
    print('MQTT verbunden')
    client.subscribe(MQTT_TOPIC_COMMAND)
    return client

def send_online_status():
    try:
        ip = network.WLAN(network.STA_IF).ifconfig()
        payload = json.dumps({"ip": ip})
        headers = {'Content-Type': 'application/json'}
        response = urequests.post(SERVER_URL, data=payload, headers=headers)
        print("Antwort vom Server:", response.text)
        response.close()
    except Exception as e:
        print("Fehler beim Senden:", e)


# MQTT-Verbindung herstellen
try:
    client = connect_mqtt()
except Exception as e:
    print('MQTT Verbindungsfehler:', e)
    client = None

send_online_status()

def interrupt_handler(pin):
    if pin is an:
        if an.value() == 1:
            
            an.value(1)
        else:
            print("'an' FALLING event")
            an.value(0)  
    elif pin is bereit:
        if bereit.value() == 1:
            print("'bereit' RISING event")
        else:
            print("'bereit' FALLING event")
            bereit.value(0)
            counter_negirp = counter_negirp + 1
    elif pin is fehler:
        if fehler.value() == 1:
            print("'fehler' RISING event")
            
            fehler.value(1)
        else:
            print("'fehler' FALLING event")
            
            fehler.value(0)

# Interrupts für die Eingänge einrichten
an.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=interrupt_handler)
bereit.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=interrupt_handler)
fehler.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=interrupt_handler)

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
                "Wasser_voll": Wasser_voll.value(),
                "einschalten": einschalten.value(),
                "starten": starten.value(),

                # ---komunikation---
                "kaffee_machen": make_coffee,
                #"vorbereitung": vorbereitung,
                "kaffee_fertig": kaffee_fertig, 
            }
            client.publish(MQTT_TOPIC_STATUS, json.dumps(status))
            # print(starten.value(), einschalten.value())
        else:   
            # Versuche Neuverbindung
            try:
                    client = connect_mqtt()
            except:
                    pass
                
       
        
    except Exception as e:
        print('Fehler in Hauptschleife:', e)
        time.sleep(5)
        client = None
    time.sleep(1)  # Kurze Pause, um CPU-Last zu reduzieren	
    if counter_negirp >2:
        bereit.value(0)
        counter_negirp = 0

    print(toggle_machine, an.value(), bereit.value(), fehler.value())
        # Einschalten der Kaffeemaschine per remote
    if toggle_machine == 1 and an.value() == 0 and bereit.value() == 0 and fehler.value() == 0:
        einschalten.value(0)
        gestartet = 1
        print("Kaffeemaschine eingeschaltet")
        toggle_machine = 0

          #Starten der Kaffeemaschine per remote
    if make_coffee == 1 and an.value() == 1 and bereit.value() == 1 and fehler.value() == 0 and gestartet == 1:
        starten.value(0)
        time.sleep(1)
        starten.value(1)
        make_coffee = 0
        in_process = 1
        print("Kaffeemaschine gestartet")
    
           
            # Kaffee fertig
    if bereit() == 1 and an() == 1 and fehler() == 0 and in_process == 1:
                kaffee_fertig=1
                in_process = 0
    else:
        kaffee_fertig=0            
    
    # Fehlerbehandlung
    if fehler() == 1:
        fehler(1)
    else:
        fehler(0)


