import requests


def validate_plate_service_enter(license_plate):
    # call redis function to validate the data
    redis_response = True

    url = "http://localhost:5000/activities"
    data = {
        "registration_number": license_plate,
        "spot_id": None,
        "type": "entrance" if redis_response else "rejected_entrance"
    }
    response = requests.post(url, json=data)
    if response.status_code == 201:
        return response.json()
    else:
        return {"error": "Failed to add activity", "status_code": response.status_code}


def validate_plate_service_exit(license_plate):
    # call redis function to validate the data
    redis_response = True

    url = "http://localhost:5000/activities"

    data = {
        "registration_number": license_plate,
        "spot_id": None,
        "type": "exit" if redis_response else "rejected_exit"
    }
    response = requests.post(url, json=data)
    if response.status_code == 201:
        return response.json()
    else:
        return {"error": "Failed to add activity", "status_code": response.status_code}


validate_plate_service_enter("ABC123")
