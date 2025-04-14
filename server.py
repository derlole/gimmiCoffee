from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
pending_command = None

@app.route('/')
def index():
    return render_template('index.html')  # Lädt templates/index.html

@app.route('/send')
def send_command():
    global pending_command
    befehl = request.args.get('befehl')
    if befehl:
        pending_command = befehl
        return f"Befehl '{befehl}' gespeichert."
    return "Kein Befehl angegeben.", 400

@app.route('/fetch')
def fetch_command():
    global pending_command
    if pending_command:
        cmd = pending_command
        pending_command = None
        return jsonify({'befehl': cmd})
    return jsonify({'befehl': None})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3060)
