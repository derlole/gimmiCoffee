import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), '../db/commands.db')

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