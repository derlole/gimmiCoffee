from flask import Blueprint, render_template, request, jsonify, redirect
unsecure = Blueprint('unsecure', __name__, url_prefix='/unsecure')
from modules.persistence import load_dict, save_dict
from modules.persistence import esp_conn_infos
from datetime import datetime
from modules.socketio import resend_static_data
from modules.db import get_coffee_count, get_coffees
from obj import user
import random


@unsecure.route('/')
def index():
    """Render the main page with user validation."""
    username = request.args.get('username')
    userid = request.args.get('userid')

    if not username or not userid:
        return redirect('/unsecure/login')

    valid_user = user.User.validate_user(username=username, userid=userid)
    print(valid_user)
    if not valid_user:
        return redirect('/unsecure/login')
    

    water = load_dict("water")
    beans = load_dict("beans")
    machine = load_dict("machine")
    coffee_count = get_coffee_count()
    # print(f"[DEBUG] Water: {water}, Beans: {beans}, Machine: {machine}")
    return render_template('index.html', title='gimmiCoffee', water=water, beans=beans, machine=machine, esp_conn_infos=esp_conn_infos, coffee_count=coffee_count, username = username)

@unsecure.route('/verify', methods=['POST'])
def verify():
    """Verify user credentials and redirect accordingly."""
    username = request.args.get('username')
    password = request.args.get('pass')

    if not username or not password:
        return jsonify({'route': '/unsecure/login'}), 400

    is_existent = user.User.authenticate_user(username, password)
    if is_existent:
        # Erfolgreich eingeloggt → weiterleiten
        return jsonify({'route': f"/unsecure/?username={is_existent.get_name()}&userid={is_existent.get_id()}"})
    else:
        # Fehler → zurück zur Login-Seite
        return jsonify({'route': '/unsecure/login', 'error': 'Invalid credentials'}), 401

@unsecure.route('/register', methods=['POST'])
def register():
    """Register a new user and redirect to the login page."""
    username = request.args.get('username')
    password = request.args.get('pass')
    userid = random.randint(10000, 99999)
    print(username, password, userid)
    if not username or not password:
        return jsonify({'err': 'invalidData'}), 400
    
    new_user = user.User(user_id=userid, name=username, email = "", password=password)
    new_user.save_to_db()
    return redirect('/unsecure/login')

@unsecure.route('/login')
def login():
    """Render the login page."""
    return render_template('login.html')

@unsecure.route('/refill-water', methods=['POST'])
def update_water():
    """Refill the water tank and update the water status."""
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
    """Refill the beans container and update the beans status."""
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
    """Render the coffees made page with a list of coffees."""
    coffees = get_coffees()
    return render_template('coffees.html', title='gimmiCoffee', coffees=coffees)

@unsecure.route('/water')
def water():
    """Render the water status page."""
    water = load_dict("water")
    return render_template('water.html', title='gimmiCoffee', last_filled=datetime.strptime(water["lastFilled"], "%Y-%m-%d %H:%M:%S.%f"), current_level=water["fill"], total_refills=water["refilled"], coffees_made=water["coffeesOnFill"])
@unsecure.route('/beans')
def beans():
    """Render the beans status page."""
    beans = load_dict("beans")
    return render_template('beans.html', title='gimmiCoffee', last_filled=datetime.strptime(beans["lastFilled"], "%Y-%m-%d %H:%M:%S.%f"), current_level=beans["fill"], total_refills=beans["refilled"], coffees_made=beans["coffeesOnFill"])
