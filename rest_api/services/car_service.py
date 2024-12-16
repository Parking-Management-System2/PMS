from rest_api.db.models import add_car, get_all_cars

def list_cars_service():
    """Fetch all cars."""
    return get_all_cars()

def create_car_service(registration_number):
    """Add a new car to the database."""
    if not registration_number:
        raise ValueError("Registration number is required")
    add_car(registration_number)
