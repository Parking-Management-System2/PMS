import os
import sqlite3

DB_FILE = os.path.join(os.path.dirname(__file__), "parking_management.db")
INIT_SQL_FILE = "db/init.sql"


def get_connection():
    """Establishes and returns a database connection."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Enables accessing rows as dictionaries
    return conn


def initialize_database():
    """Initializes the database by executing SQL from init.sql."""
    conn = get_connection()
    cursor = conn.cursor()

    # Read the SQL file
    with open(INIT_SQL_FILE, "r") as f:
        sql_script = f.read()

    # Execute the SQL script
    cursor.executescript(sql_script)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    initialize_database()
