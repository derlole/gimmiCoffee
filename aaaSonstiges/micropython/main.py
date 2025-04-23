import urequests #this is not an issue, because micropython has its own urequests module already
import json
import socket

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

# beispiel-fetch von der hauptadresse (muss evtl in ne roop und nen thread)
def fetch_json(ip, host, path):
    url = f"http://{ip}{path}"
    try:
        print(f"Sende Anfrage an {url} mit Host '{host}' ...")
        headers = {"Host": host}
        response = urequests.get(url, headers=headers)

        if response.status_code == 200:
            print("✅ Antwort erhalten:")
            print(response.text)
            data = json.loads(response.text)
            print("📦 JSON geladen:", data)
        else:
            print(f"❌ Fehler: Status-Code {response.status_code}")

        response.close()

    except Exception as e:
        print("⚠️ Fehler bei der Anfrage (äußerer Block):", e)

# --- Hauptteil ---
host = "lires.de"
path = "/unsecure/esp/"

ip = resolve_ip(host)
if ip:
    fetch_json(ip, host, path)
