from rest_api.db.models import add_car, get_all_cars, update_car_status

def list_cars_service():
    """Fetch all cars."""
    return get_all_cars()

def create_car_service(registration_number, car_status):
    """Add a new car to the database."""
    if not registration_number or not car_status:
        raise ValueError("Registration number and car status are required")
    add_car(registration_number, car_status)

def update_car_status_service(car_id, car_status):
    """Update the status of a car."""
    if not car_id or not car_status:
        raise ValueError("Car ID and car status are required")
    update_car_status(car_id, car_status)