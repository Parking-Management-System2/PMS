from rest_api.db.database import get_connection


# Cars Table Operations
def add_car(registration_number, car_status):
    """Adds a new car to the Cars table."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO cars (registration_number, car_status)
            VALUES (?, ?);
            """,
            (registration_number, car_status),
        )
        conn.commit()
    finally:
        conn.close()


def update_car_status(car_id, car_status):
    """Updates the status of a car."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE cars
        SET car_status = ?
        WHERE car_id = ?;
        """,
        (car_status, car_id),
    )

    if cursor.rowcount == 0:
        conn.close()
        raise ValueError("No car found with the given ID")

    conn.commit()
    conn.close()


def get_all_cars():
    """Fetches all cars from the Cars table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars;")
    cars = cursor.fetchall()
    conn.close()
    return cars


# Parking_spot Table Operations
def add_parking_spot(spot_number, car_id=None):
    """Adds a new parking spot."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO parking_spots (spot_number, car_id)
        VALUES (?, ?);
        """,
        (spot_number, car_id),
    )
    conn.commit()
    conn.close()


def get_available_parking_spots():
    """Fetches all available parking spots."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM parking_spots WHERE car_id IS NULL;")
    spots = cursor.fetchall()
    conn.close()
    return spots


def update_parking_spot_status(spot_id, car_id):
    """Updates the status of a parking spot."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE parking_spots
        SET car_id = ?
        WHERE spot_id = ?;
        """,
        (car_id, spot_id),
    )

    if cursor.rowcount == 0:
        conn.close()
        raise ValueError("No parking spot found with the given ID")

    conn.commit()
    conn.close()


# Activity Table Operations
def record_activity(car_id, spot_id, entrance_timestamp, leave_timestamp=None, status=None):
    """Records activity for a car in the parking lot."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO activities (car_id, spot_id, entrance_timestamp, leave_timestamp, status)
        VALUES (?, ?, ?, ?, ?);
        """,
        (car_id, spot_id, entrance_timestamp, leave_timestamp, status),
    )
    conn.commit()
    conn.close()


def get_all_activities():
    """Fetches all activities from the Activity table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM activities;")
    activities = cursor.fetchall()
    conn.close()
    return activities


def update_activity(activity_id, car_id, spot_id, entrance_timestamp, leave_timestamp=None, status=None):
    """Updates an existing activity."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE activities
        SET car_id = ?, spot_id = ?, entrance_timestamp = ?, leave_timestamp = ?, status = ?
        WHERE activity_id = ?;
        """,
        (car_id, spot_id, entrance_timestamp, leave_timestamp, status, activity_id),
    )

    if cursor.rowcount == 0:
        conn.close()
        raise ValueError("No activity found with the given ID")

    conn.commit()
    conn.close()
