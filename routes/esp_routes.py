from flask import Blueprint, render_template, request, jsonify
import routes.shared as shared
esp = Blueprint('eps', __name__, url_prefix='/unsecure/esp')


@esp.route('/')
def fetch_command():
    pCd = shared.pending_command
    shared.reset_command()
    return jsonify(pCd)