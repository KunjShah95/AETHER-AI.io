import sqlite3
import os
from datetime import datetime
import logging

class AnalyticsManager:
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.path.join(os.path.expanduser("~"), ".nexus", "analytics.db")
        
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS usage_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        username TEXT,
                        command_type TEXT,
                        details TEXT
                    )
                ''')
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS error_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        error_type TEXT,
                        message TEXT
                    )
                ''')
                conn.commit()
        except Exception as e:
            logging.error(f"Analytics DB Init Error: {e}")

    def log_usage(self, username: str, command_type: str, details: str = ""):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO usage_logs (timestamp, username, command_type, details) VALUES (?, ?, ?, ?)',
                    (datetime.now().isoformat(), username, command_type, details)
                )
                conn.commit()
        except Exception as e:
            logging.error(f"Log Usage Error: {e}")

    def log_error(self, error_type: str, message: str):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO error_logs (timestamp, error_type, message) VALUES (?, ?, ?)',
                    (datetime.now().isoformat(), error_type, message)
                )
                conn.commit()
        except Exception as e:
            logging.error(f"Log Error Error: {e}")

    def get_stats(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT command_type, COUNT(*) FROM usage_logs GROUP BY command_type')
                return dict(cursor.fetchall())
        except Exception:
            return {}
