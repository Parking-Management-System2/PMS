from flask import Blueprint, request, jsonify
from rest_api.services.parking_service import (
    list_available_parking_spots_service,
    create_parking_spot_service,
)
from rest_api.db.models import update_parking_spot_status

parking_blueprint = Blueprint("parking", __name__)

@parking_blueprint.route("/available", methods=["GET"])
def list_available_spots():
    """
    List all available parking spots.
    """
    spots = list_available_parking_spots_service()
    return jsonify([dict(spot) for spot in spots]), 200


@parking_blueprint.route("/", methods=["POST"])
def create_parking_spot():
    """
    Add a new parking spot.
    """
    try:
        data = request.get_json()
        spot_number = data.get("spot_number")

        create_parking_spot_service(spot_number)
        return jsonify({"message": "Parking spot created successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@parking_blueprint.route("/<int:spot_id>/update", methods=["PATCH"])
def update_parking_status(spot_id):
    """
    Update the status of a parking spot (e.g., assign/unassign a car).
    """
    try:
        data = request.get_json()
        car_id = data.get("car_id")  # Can be None to unassign a car
        update_parking_spot_status(spot_id, car_id)
        return jsonify({"message": "Parking spot updated successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
