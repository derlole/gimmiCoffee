from flask import Blueprint, render_template, request, jsonify

unsecure = Blueprint('unsecure', __name__, url_prefix='/unsecure')

pending_command = None

@unsecure.route('/')
def index():
    return render_template('index.html')

@unsecure.route('/send')
def send_command():
    global pending_command
    befehl = request.args.get('befehl')
    if befehl:
        pending_command = befehl
        return f"Befehl '{befehl}' gespeichert."
    return "Kein Befehl angegeben.", 400

@unsecure.route('/fetch')
def fetch_command():
    global pending_command
    if pending_command:
        cmd = pending_command
        pending_command = None
        return jsonify({'befehl': cmd})
    return jsonify({'befehl': None})
