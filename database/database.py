import os
import sqlite3
from pathlib import Path

def _get_database_path(db_path=None):
    if db_path:
        return Path(db_path)
    volume_path = os.getenv("RAILWAY_VOLUME_MOUNT_PATH", "").strip()
    if volume_path:
        p = Path(volume_path)
        p.mkdir(parents=True, exist_ok=True)
        return p / "database.db"
    database_url = os.getenv("DATABASE_URL", "").strip()
    if database_url.startswith("sqlite:///"):
        raw = database_url[len("sqlite:///"):]
        p = Path(raw) if Path(raw).is_absolute() else Path.cwd() / raw
        p.parent.mkdir(parents=True, exist_ok=True)
        return p
    p = Path("database.db")
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

class Database:
    def __init__(self, db_path=None):
        self.db_path = _get_database_path(db_path)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS warnings (
                user_id INTEGER PRIMARY KEY,
                warning_count INTEGER NOT NULL,
                last_warning_time TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS xp (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER NOT NULL DEFAULT 0
            )
        """)
        self.conn.commit()

    def add_warning(self, user_id):
        self.cursor.execute("SELECT warning_count FROM warnings WHERE user_id=?", (user_id,))
        row = self.cursor.fetchone()
        count = (row[0] + 1) if row else 1
        self.cursor.execute("""
            INSERT INTO warnings(user_id, warning_count, last_warning_time)
            VALUES (?, ?, datetime('now'))
            ON CONFLICT(user_id) DO UPDATE SET
                warning_count=excluded.warning_count,
                last_warning_time=excluded.last_warning_time
        """, (user_id, count))
        self.conn.commit()
        return count

    def get_warning(self, user_id):
        self.cursor.execute("SELECT warning_count, last_warning_time FROM warnings WHERE user_id=?", (user_id,))
        return self.cursor.fetchone()

    def reset_warning(self, user_id):
        self.cursor.execute("DELETE FROM warnings WHERE user_id=?", (user_id,))
        self.conn.commit()

    def add_xp(self, user_id, amount=1):
        self.cursor.execute("SELECT xp FROM xp WHERE user_id=?", (user_id,))
        row = self.cursor.fetchone()
        new_xp = (row[0] if row else 0) + amount
        self.cursor.execute("""
            INSERT INTO xp(user_id, xp) VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET xp=excluded.xp
        """, (user_id, new_xp))
        self.conn.commit()
        return new_xp

    def get_xp(self, user_id):
        self.cursor.execute("SELECT xp FROM xp WHERE user_id=?", (user_id,))
        row = self.cursor.fetchone()
        return row[0] if row else 0

    def close(self):
        self.conn.close()
