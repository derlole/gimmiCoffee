from flask import Blueprint, render_template, request, jsonify
unsecure = Blueprint('unsecure', __name__, url_prefix='/unsecure')
from modules.persistence import load_dict, save_dict
from modules.persistence import esp_conn_infos
# from flask_socketio import SocketIO
from modules.socketio import resend_static_data

# def resend_static_data():
#     water = load_dict("water")
#     beans = load_dict("beans")
#     machine = load_dict("machine")
#     socketio.emit('static_data', {
#         'water': water,
#         'beans': beans,
#         'machine': machine,
#         'esp_conn_infos': esp_conn_infos
# })

@unsecure.route('/')
def index():
    water = load_dict("water")
    beans = load_dict("beans")
    machine = load_dict("machine")
    print(f"Water: {water}, Beans: {beans}, Machine: {machine}")
    return render_template('index.html', title='gimmiCoffee', water=water, beans=beans, machine=machine, esp_conn_infos=esp_conn_infos)

@unsecure.route('/update')
def update():
    resend_static_data()
    return jsonify({"status": "ok"})
