import sqlite3
import os
from datetime import datetime, timedelta
from modules.socketio import resend_static_data
import random

DB_PATH = os.path.join(os.path.dirname(__file__), '../db/commands.db')
DB_PATH_COFFEE = os.path.join(os.path.dirname(__file__), '../db/coffee.db') 


def update_command_status(command_id, status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE commands
        SET status = ?
        WHERE command_id = ?
    """, (status, command_id))
    
    conn.commit()
    conn.close()
    print(f"[DB] Befehl {command_id} auf {status} aktualisiert.")
    return status

def get_coffee_count():
    conn = sqlite3.connect(DB_PATH_COFFEE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM coffee")
    count = cursor.fetchone()[0]
    
    conn.close()
    return count

def get_coffees():
    conn = sqlite3.connect(DB_PATH_COFFEE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM coffee")
    coffees = cursor.fetchall()
    
    conn.close()
    return coffees
def create_toggle_machine():
    randID = random.randint(1000, 9999)
    fullCommand = {'command': 'toggle_machine', 'status': 'pending', 'command_id': randID}
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO commands (command, status, command_id)
        VALUES (?, ?, ?)
    """, (fullCommand["command"], fullCommand["status"], fullCommand["command_id"]))

    resend_static_data()
    
    conn.commit()
    conn.close()
    return fullCommand

def create_make_coffee():
    randID = random.randint(1000, 9999)
    fullCommand = {'command': 'make_coffee', 'status': 'pending', 'command_id': randID}
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO commands (command, status, command_id)
        VALUES (?, ?, ?)
    """, (fullCommand["command"], fullCommand["status"], fullCommand["command_id"]))

    conn.commit()
    conn.close()
    return fullCommand

def create_coffee_entry():
    conn = sqlite3.connect(DB_PATH_COFFEE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO coffee (user, status)
        VALUES (?, ?)
    """, ("admin", "served"))
    conn.commit()
    conn.close()