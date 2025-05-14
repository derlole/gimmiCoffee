import sqlite3
import os

class User:
    def __init__(self, user_id, name, email):
        self._user_id = user_id
        self._name = name
        self._email = email
        self._db_path = os.path.join("..", "db", "user.db")
        self._init_db()

    # Getter
    def get_id(self):
        return self._user_id

    def get_name(self):
        return self._name

    def get_email(self):
        return self._email

    # Setter
    def set_name(self, name):
        self._name = name
        self._update_db()

    def set_email(self, email):
        self._email = email
        self._update_db()

    def _init_db(self):
        """Create the database and table if it doesn't exist"""
        with sqlite3.connect(self._db_path) as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL
                )
            ''')
            conn.commit()
            self._save_to_db()

    def _save_to_db(self):
        """Insert or update the user in the DB"""
        with sqlite3.connect(self._db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT id FROM users WHERE id = ?", (self._user_id,))
            if c.fetchone():
                # update
                c.execute('UPDATE users SET name = ?, email = ? WHERE id = ?',
                          (self._name, self._email, self._user_id))
            else:
                # insert
                c.execute('INSERT INTO users (id, name, email) VALUES (?, ?, ?)',
                          (self._user_id, self._name, self._email))
            conn.commit()

    def _update_db(self):
        """Update the user's data in the DB"""
        with sqlite3.connect(self._db_path) as conn:
            c = conn.cursor()
            c.execute('UPDATE users SET name = ?, email = ? WHERE id = ?',
                      (self._name, self._email, self._user_id))
            conn.commit()