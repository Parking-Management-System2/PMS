from rest_api.db.models import add_parking_spot, get_available_parking_spots, update_parking_spot_status

def list_available_parking_spots_service():
    """
    Fetch all available parking spots.
    """
    return get_available_parking_spots()

def create_parking_spot_service(spot_number):
    """
    Add a new parking spot to the database.
    """
    if not spot_number:
        raise ValueError("Spot number is required")
    add_parking_spot(spot_number)

def update_parking_status_service(spot_id, car_id):
    """
    Update the status of a parking spot (assign or unassign a car).
    """
    if not spot_id:
        raise ValueError("Spot ID is required")
    update_parking_spot_status(spot_id, car_id)
