import os
import sqlite3

DB_FILE = os.path.join(os.path.dirname(__file__), "parking_system.db")
INIT_SQL_FILE = os.path.join(os.path.dirname(__file__), "init.sql")


def get_connection():
    """Establishes and returns a database connection."""
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None


def initialize_database():
    """Initializes the database by executing SQL from init.sql."""
    conn = get_connection()
    if conn is None:
        return

    cursor = conn.cursor()

    try:
        with open(INIT_SQL_FILE, "r") as f:
            sql_script = f.read()
            print("SQL script read from file:")
            print(sql_script)
    except IOError as e:
        print(f"Error reading SQL file: {e}")
        return

    try:
        cursor.executescript(sql_script)
        conn.commit()
        print("Database initialized successfully.")
    except sqlite3.Error as e:
        print(f"Error executing SQL script: {e}")
    finally:
        conn.close()



if __name__ == "__main__":
    initialize_database()
