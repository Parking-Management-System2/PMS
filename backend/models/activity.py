from datetime import datetime

from backend.db.database import get_connection


def get_all_activities():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM activities;")
    activities = cursor.fetchall()
    conn.close()
    return activities


def get_activity(activity_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM activities WHERE activity_id = ?;", (activity_id,))
    activity = cursor.fetchone()
    conn.close()
    return activity


def add_activity(registration_number, spot_id, type):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(
        """
        INSERT INTO activities (registration_number, spot_id, type, timestamp)
        VALUES (?, ?, ?, ?);
        """,
        (registration_number, spot_id, type, timestamp),
    )
    conn.commit()
    conn.close()


def get_activities_by_registration_number(registration_number):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM activities WHERE registration_number = ?;", (registration_number,))
    activities = cursor.fetchall()
    conn.close()
    return activities
