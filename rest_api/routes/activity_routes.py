from flask import Blueprint, request, jsonify
from rest_api.services.activity_service import create_activity_service
from rest_api.db.models import get_all_activities

activity_blueprint = Blueprint("activity", __name__)

@activity_blueprint.route("/", methods=["GET"])
def list_activities():
    """
    List all activities in the database.
    """
    activities = get_all_activities()
    return jsonify([dict(activity) for activity in activities]), 200


@activity_blueprint.route("/", methods=["POST"])
def create_activity():
    """
    Record a new parking activity.
    """
    try:
        data = request.get_json()
        car_id = data.get("car_id")
        spot_id = data.get("spot_id")
        enterance_timestamp = data.get("enterance_timestamp")
        leave_timestamp = data.get("leave_timestamp")  # Optional

        create_activity_service(car_id, spot_id, enterance_timestamp, leave_timestamp)
        return jsonify({"message": "Activity recorded successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
