from backend.db.database import get_connection

def add_spot(spot_number, registration_number=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO spots (spot_number, registration_number)
        VALUES (?, ?);
        """,
        (spot_number, registration_number),
    )
    conn.commit()
    conn.close()

def get_all_spots():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM spots;")
    spots = cursor.fetchall()
    conn.close()
    return spots

def get_spot(spot_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM spots WHERE spot_id = ?;", (spot_id,))
    spot = cursor.fetchone()
    conn.close()
    return spot

def update_spot(spot_id, spot_number, registration_number):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE spots
        SET spot_number = ?, registration_number = ?
        WHERE spot_id = ?;
        """,
        (spot_number, registration_number, spot_id),
    )
    conn.commit()
    conn.close()

def delete_spot(spot_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM spots WHERE spot_id = ?;", (spot_id,))
    conn.commit()
    conn.close()