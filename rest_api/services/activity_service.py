from rest_api.db.models import record_activity

def create_activity_service(car_id, spot_id, enterance_timestamp, leave_timestamp=None):
    """
    Record a parking activity.
    """
    if not (car_id and spot_id and enterance_timestamp):
        raise ValueError("Car ID, Spot ID, and Entrance Timestamp are required")
    record_activity(car_id, spot_id, enterance_timestamp, leave_timestamp)