# -*- coding: utf-8 -*-
# Dieses Skript erstellt eine SQLite-Datenbank mit einer Tabelle für Befehle.

import os
import sqlite3

# Ordner und Pfad definieren
db_folder = "db"
db_filename = "commands.db"
db_path = os.path.join(db_folder, db_filename)

# Ordner erstellen, falls nicht vorhanden
os.makedirs(db_folder, exist_ok=True)

# Verbindung zur SQLite-Datenbank
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Tabelle erstellen
cursor.execute("""
CREATE TABLE IF NOT EXISTS commands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    command TEXT NOT NULL,
    status TEXT NOT NULL,
    command_id INTEGER UNIQUE NOT NULL,
    tstamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print(f"[DB]Datenbank erstellt unter: {db_path}")
