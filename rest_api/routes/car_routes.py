from flask import Blueprint, request, jsonify
from flasgger import swag_from
from rest_api.services.car_service import list_cars_service, create_car_service

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
                        'registration_number': {'type': 'string'}
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
                    'registration_number': {'type': 'string'}
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
        create_car_service(registration_number)
        return jsonify({"message": "Car added successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400