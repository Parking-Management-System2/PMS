from flask import Blueprint, request, jsonify
from rest_api.services.cars_service import list_cars_service, create_car_service

cars_blueprint = Blueprint("cars", __name__)

@cars_blueprint.route("/", methods=["GET"])
def list_cars():
    """List all cars."""
    cars = list_cars_service()
    return jsonify([dict(car) for car in cars])

@cars_blueprint.route("/", methods=["POST"])
def create_car():
    """Add a new car."""
    try:
        data = request.get_json()
        registration_number = data.get("registration_number")
        create_car_service(registration_number)
        return jsonify({"message": "Car added successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
