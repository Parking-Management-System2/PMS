from rest_api.db.database import get_connection

# Cars Table Operations
def add_car(registration_number):
    """Adds a new car to the Cars table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Cars (registration_number)
        VALUES (?);
        """,
        (registration_number,),
    )
    conn.commit()
    conn.close()


def get_all_cars():
    """Fetches all cars from the Cars table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Cars;")
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
        INSERT INTO Parking_spot (spot_number, car_id)
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
    cursor.execute("SELECT * FROM Parking_spot WHERE car_id IS NULL;")
    spots = cursor.fetchall()
    conn.close()
    return spots


def update_parking_spot_status(spot_id, car_id):
    """Updates the status of a parking spot."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE Parking_spot
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
def record_activity(car_id, spot_id, enterance_timestamp, leave_timestamp=None):
    """Records activity for a car in the parking lot."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO activity (car_id, spot_id, enterance_timestamp, leave_timestamp)
        VALUES (?, ?, ?, ?);
        """,
        (car_id, spot_id, enterance_timestamp, leave_timestamp),
    )
    conn.commit()
    conn.close()


def get_all_activities():
    """Fetches all activities from the Activity table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM activity;")
    activities = cursor.fetchall()
    conn.close()
    return activities
