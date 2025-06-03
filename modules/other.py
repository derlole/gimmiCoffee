# this function is processing the cyclic data from the esp format:
#                           [off_value/on_value]
# {
#   # eingänge
#   "an":                   [1/0],
#   "bereit":               [1/0],
#   "fehler":               [1/0],
#   "bohnen_voll":          [1/0],
#   "Wasser_voll":          [1/0],

#   # ausgänge
#   "einschalten":          [0/1],
#   "starten":              [0/1],
  
#   # status
#   "kaffee_machen":        [0/1],
#   "vorbereitung":         [0/1],
#   "kaffee_fertig":        [0/1],
# }

from modules.persistence import load_dict, save_dict
from modules.socketio import resend_static_data
from modules.db import create_coffee_entry

def track_coffee_made(data, flanksUp, flanksDown):
    """Track if coffee has been made based on the ESP data."""
    coffee_made = False
    #logic for tracking coffee made

    if coffee_made:
        create_coffee_entry()

        print("Coffee made detected, data saved.")
        # update water fill and beans fill and coffeeOn water and beans
    return 

def track_error_water(data, flanksUp, flanksDown):
    """Track if there could be an error with water."""
    water = load_dict("water")
    if water["fill"] <= 7:
        return True
    return False

def track_error_beans(data, flanksUp, flanksDown):
    """Track if there could be an error with beans."""
    beans = load_dict("beans")
    if beans["fill"] <= 7:
        return True
    return False

def track_error(data, flanksUp, flanksDown):
    """Backrrack an Coffee machine error."""
    if track_error_water(data, flanksUp, flanksDown):
        return "Wasser Leer"
    elif track_error_beans(data, flanksUp, flanksDown):
        return "Bohnen Leer"
    return "Unbekannter Fehler"

def refactor_and_use_esp_data(data):
    """Refactor and use the ESP data to update the machine state.
    Calls track_coffee_made() and track_error functions()."""
    # global oldDataSet
    if 'oldDataSet' not in globals() or oldDataSet is None:
        oldDataSet = data  # Initialize oldDataSet with default values
    
    flanksUp = {key: (oldDataSet[key] == 0 and data[key] == 1) for key in data}
    flanksDown = {key: (oldDataSet[key] == 1 and data[key] == 0) for key in data}
    
    machine = load_dict("machine")
    if data["an"] == 0:
        machine["state"] = "ON"
    elif data["an"] == 1:                   #elif die Sängerin xD
        machine["state"] = "OFF"

    if data["bereit"] == 0:
        machine["ready"] = True
    elif data["bereit"] == 1:
        machine["ready"] = False

    if data["fehler"] == 0:
        machine["berror"] = True
        machine["error"] = track_error(data, flanksUp, flanksDown)
    elif data["fehler"] == 1:   
        machine["berror"] = False
        machine["error"] = "Keine Fehler"

    save_dict("machine", machine)
    resend_static_data()

    track_coffee_made(data, flanksUp, flanksDown)
    oldDataSet = data
    return