from flask import Blueprint, render_template, request, jsonify
import routes.shared as shared
unsecure = Blueprint('unsecure', __name__, url_prefix='/unsecure')



@unsecure.route('/')
def index():
    return render_template('index.html')

@unsecure.route('/send')
def send_command():
    pCd = shared.pending_command
    befehl = request.args.get('befehl')
    if befehl:
        pCd['command'] = befehl
        pCd['command-URL'] = '/unsecure/esp/someURI'
        pCd.update({'extra': 'test'})
        print(pCd)
        return f"Befehl '{pCd}' gespeichert."
    return "Kein Befehl angegeben.", 400

@unsecure.route('/test')
def test():
    return render_template('test.html')
