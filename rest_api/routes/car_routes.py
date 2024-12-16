from flask import Blueprint, request, jsonify
from flasgger import swag_from
from rest_api.services.car_service import list_cars_service, create_car_service, update_car_status_service

cars_blueprint = Blueprint("cars", __name__)


@cars_blueprint.route("/", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'List of all cars',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'car_id': {'type': 'integer'},
                        'registration_number': {'type': 'string'},
                        'car_status': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def list_cars():
    """List all cars."""
    cars = list_cars_service()
    return jsonify([dict(car) for car in cars])


@cars_blueprint.route("/", methods=["POST"])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'registration_number': {'type': 'string'},
                    'car_status': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Car added successfully'},
        400: {'description': 'Invalid input'}
    }
})
def create_car():
    """Add a new car."""
    try:
        data = request.get_json()
        registration_number = data.get("registration_number")
        car_status = data.get("car_status")
        create_car_service(registration_number, car_status)
        return jsonify({"message": "Car added successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@cars_blueprint.route("/<int:car_id>/status", methods=["PATCH"])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'car_status': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Car status updated successfully'},
        400: {'description': 'Invalid input'}
    }
})
def update_car_status(car_id):
    """Update the status of a car."""
    try:
        data = request.get_json()
        car_status = data.get("car_status")
        update_car_status_service(car_id, car_status)
        return jsonify({"message": "Car status updated successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
