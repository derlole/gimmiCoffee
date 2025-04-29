import urequests
import json
import socket
import network
import time
import ubinascii
from umqtt.simple import MQTTClient
import machine
host = "lires.de"

# one time dns resolve, damit der arme ESP und nicht wegkocht.
def resolve_ip(hostname):
    try:
        print(f"🌐 Resolvieren von '{hostname}' ...")
        addr_info = socket.getaddrinfo(hostname, 80)
        ip = addr_info[0][4][0]
        print(f"🔎 IP-Adresse gefunden: {ip}")
        return ip
    except Exception as e:
        print("❌ Fehler beim Resolvieren:", e)
        return None
    
ip = resolve_ip(host)
if ip is None:
    print("❌ Fehler: IP-Adresse konnte nicht aufgelöst werden.")
    raise SystemExit(1)
MQTT_BROKER = ip
MQTT_TOPIC = b'iot/testdata'

#callback
def mqtt_callback(topic, msg):
    print("Neue Nachricht:", msg.decode())

#send data to the server on the given url
def main():
    client_id = ubinascii.hexlify(machine.unique_id())
    client = MQTTClient(client_id, MQTT_BROKER)
    client.set_callback(mqtt_callback)
    client.connect()
    client.subscribe(MQTT_TOPIC)
    print("Warte auf Nachrichten...")

    try:
        while True:
            client.wait_msg()  # blockiert, bis Nachricht ankommt
    finally:
        client.disconnect()

main()


while True:
    {

        
    }







