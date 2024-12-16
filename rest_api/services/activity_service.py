from rest_api.db.models import record_activity, update_activity

def create_activity_service(car_id, spot_id, entrance_timestamp, leave_timestamp=None, status="active"):
    """
    Record a parking activity.
    """
    if not (car_id and spot_id and entrance_timestamp):
        raise ValueError("Car ID, Spot ID, and Entrance Timestamp are required")
    record_activity(car_id, spot_id, entrance_timestamp, leave_timestamp, status)

def update_activity_service(activity_id, car_id, spot_id, entrance_timestamp, leave_timestamp=None, status=None):
    """
    Update a parking activity.
    """
    if not (activity_id and car_id and spot_id and entrance_timestamp and status):
        raise ValueError("Activity ID, Car ID, Spot ID, Entrance Timestamp, and Status are required")
    update_activity(activity_id, car_id, spot_id, entrance_timestamp, leave_timestamp, status)