from flask import Blueprint, render_template, request, jsonify
unsecure = Blueprint('unsecure', __name__, url_prefix='/unsecure')
from modules.persistence import load_dict, save_dict
from modules.persistence import esp_conn_infos
from datetime import datetime
from modules.socketio import resend_static_data
from modules.db import get_coffee_count, get_coffees


@unsecure.route('/')
def index():
    water = load_dict("water")
    beans = load_dict("beans")
    machine = load_dict("machine")
    coffee_count = get_coffee_count()
    print(f"Water: {water}, Beans: {beans}, Machine: {machine}")
    return render_template('index.html', title='gimmiCoffee', water=water, beans=beans, machine=machine, esp_conn_infos=esp_conn_infos, coffee_count=coffee_count)

# @unsecure.route('/update')
# def update():
#     resend_static_data()
#     return jsonify({"status": "ok", "task": "update-executed"})

@unsecure.route('/refill-water', methods=['POST'])
def update_water():
    water = load_dict("water")
    water["lastFilled"] = datetime.now()
    water["fill"] = 100
    water["coffeesOnFill"] = 0
    water["refilled"] = water["refilled"] + 1
    save_dict("water", water)
    resend_static_data()
    return jsonify({"status": "ok", "task": "refill-water-executed"})

@unsecure.route('/refill-beans', methods=['POST'])
def update_beans():
    beans = load_dict("beans")
    beans["lastFilled"] = datetime.now()
    beans["fill"] = 100
    beans["coffeesOnFill"] = 0
    beans["refilled"] = beans["refilled"] + 1
    save_dict("beans", beans)
    resend_static_data()
    return jsonify({"status": "ok", "task": "refill-beans-executed"})

@unsecure.route('/coffees-made')
def coffees_made():
    coffees = get_coffees()
    return render_template('coffees.html', title='gimmiCoffee', coffees=coffees)

@unsecure.route('/water')
def water():
    water = load_dict("water")
    return render_template('water.html', title='gimmiCoffee', last_filled=water["lastFilled"], current_level=water["fill"], total_refills=water["refilled"], coffees_made=water["coffeesOnFill"])
@unsecure.route('/beans')
def beans():
    beans = load_dict("beans")
    return render_template('beans.html', title='gimmiCoffee', last_filled=beans["lastFilled"], current_level=beans["fill"], total_refills=beans["refilled"], coffees_made=beans["coffeesOnFill"])
