import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), '../db/commands.db')
DB_PATH_COFFEE = os.path.join(os.path.dirname(__file__), '../db/coffee.db') 

### THIS CODE IS NOT PROOFED BUT LOOKS RIGHT###
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
### THIS CODE IS NOT PROOFED BUT LOOKS RIGHT###

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