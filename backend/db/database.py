import os
import sqlite3

DB_FILE = os.path.join(os.path.dirname(__file__), "parking_system.db")


def get_connection():
    """Establishes and returns a database connection."""
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None


import sqlite3

def initialize_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Check if the tables already exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='activities';")
    activities_table_exists = cursor.fetchone() is not None

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='spots';")
    spots_table_exists = cursor.fetchone() is not None

    if not activities_table_exists:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_number TEXT NOT NULL,
            spot_id INTEGER,
            type TEXT NOT NULL CHECK(type IN ('entrance', 'exit', 'rejected_entrance', 'rejected_exit', 'parked_ok', 'parked_wrong')),
            timestamp TEXT NOT NULL
        );
        """)

        # Insert sample data into the activities table
        cursor.executemany("""
        INSERT INTO activities (registration_number, spot_id, type, timestamp) VALUES (?, ?, ?, ?);
        """, [
            ('ABC123', 1, 'entrance', '2024-12-01 08:00:00'),
            ('ABC123', 1, 'exit', '2024-12-01 10:00:00'),
            ('DEF456', 2, 'entrance', '2024-12-01 09:00:00'),
            ('DEF456', 2, 'exit', '2024-12-01 11:30:00'),
            ('GHI789', 3, 'entrance', '2024-12-01 10:00:00'),
            ('GHI789', 3, 'exit', '2024-12-01 12:00:00'),
            ('JKL012', 5, 'entrance', '2024-12-01 07:30:00'),
            ('JKL012', 5, 'exit', '2024-12-01 09:45:00'),
            ('MNO345', 6, 'entrance', '2024-12-01 08:15:00'),
            ('MNO345', 6, 'exit', '2024-12-01 10:15:00'),
            ('PQR678', 8, 'entrance', '2024-12-01 06:00:00'),
            ('PQR678', 8, 'exit', '2024-12-01 08:30:00'),
            ('STU901', 10, 'entrance', '2024-12-01 09:45:00'),
            ('STU901', 10, 'exit', '2024-12-01 11:00:00'),
            ('VWX234', None, 'entrance', '2024-12-01 10:30:00'),
            ('VWX234', None, 'exit', '2024-12-01 12:30:00'),
            ('YZA567', None, 'entrance', '2024-12-01 07:00:00'),
            ('YZA567', None, 'exit', '2024-12-01 08:00:00'),
            ('BCD890', None, 'entrance', '2024-12-01 08:30:00'),
            ('BCD890', None, 'exit', '2024-12-01 09:30:00'),
            ('EFG234', 4, 'entrance', '2024-12-01 07:45:00'),
            ('EFG234', 4, 'exit', '2024-12-01 09:15:00'),
            ('HIJ567', 7, 'entrance', '2024-12-01 08:20:00'),
            ('HIJ567', 7, 'exit', '2024-12-01 10:40:00'),
            ('LMN890', None, 'rejected_entrance', '2024-12-01 13:00:00'),
            ('OPQ123', None, 'rejected_entrance', '2024-12-01 14:00:00'),
            ('RST456', None, 'rejected_exit', '2024-12-01 15:00:00')
        ])

    if not spots_table_exists:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS spots (
            spot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            spot_number TEXT NOT NULL,
            registration_number TEXT
        );
        """)

        # Insert sample data into the spots table
        cursor.executemany("""
        INSERT INTO spots (spot_number, registration_number) VALUES (?, ?);
        """, [
            ('1', 'WPL1A43'),
            ('2', 'EL123'),
            ('3', 'GDA54A3'),
            ('4', 'WGSE214'),
            ('5', None),
            ('6', None),
            ('7', None),
            ('8', None),
            ('9', None),
            ('10', None),
            ('11', None),
            ('12', None),
            ('13', None),
            ('14', None),
            ('15', None)
        ])

    conn.commit()
    conn.close()

