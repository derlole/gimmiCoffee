import network
import time
import gc

gc.collect()

# (SSID: Passwort)
known_networks = {
    "Vodafone-9454": "AchXHta93YCTgC3M",
    "WGLan": "2Bierund1Pizza!", 
    "No": "",
    "placeholder2": "placeholder2"
}

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # Suche nach verfügbaren Netzwerken
    print("Scanne nach WLAN-Netzwerken...")
    available_networks = wlan.scan()
    print(f"Gefundene Netzwerke: {(available_networks)}")
    for net in available_networks:
        ssid = net[0].decode('utf-8') if isinstance(net[0], bytes) else net[0]
        if ssid in known_networks:
            password = known_networks[ssid]
            print(f"Versuche Verbindung mit '{ssid}'...")
            wlan.connect(ssid, password)

            while not wlan.isconnected():
                time.sleep(1)
                print(".", end="")

            if wlan.isconnected():
                print(f"\nVerbunden mit '{ssid}'")
                print("IP-Adresse:", wlan.ifconfig()[0])
                return True
            else:
                print(f"\n❌ Verbindung mit '{ssid}' fehlgeschlagen.")
    
    print("Kein bekanntes Netzwerk verfügbar oder Verbindung fehlgeschlagen.")
    return False

# Verbindung herstellen beim Boot
connect_wifi()
