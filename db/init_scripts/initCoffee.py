# -*- coding: utf-8 -*-
# Dieses Skript erstellt eine SQLite-Datenbank mit einer Tabelle für Befehle.

import os
import sqlite3

db_folder = "db"
db_filename = "coffee.db"
db_path = os.path.join(db_folder, db_filename)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Tabelle erstellen mit entsprechenden Atributen
cursor.execute("""
CREATE TABLE IF NOT EXISTS coffee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    status TEXT NOT NULL,
    tstamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print(f"[DB]Datenbank erstellt unter: {db_path}")
