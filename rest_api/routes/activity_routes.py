from flask import Blueprint, request, jsonify
from flasgger import swag_from
from rest_api.services.activity_service import create_activity_service, update_activity_service
from rest_api.db.models import get_all_activities

activity_blueprint = Blueprint("activities", __name__)


@activity_blueprint.route("/", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'List of all activities',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'activity_id': {'type': 'integer'},
                        'car_id': {'type': 'integer'},
                        'spot_id': {'type': 'integer'},
                        'entrance_timestamp': {'type': 'string'},
                        'leave_timestamp': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def list_activities():
    activities = get_all_activities()
    return jsonify([dict(activity) for activity in activities]), 200


@activity_blueprint.route("/", methods=["POST"])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'car_id': {'type': 'integer'},
                    'spot_id': {'type': 'integer'},
                    'entrance_timestamp': {'type': 'string'},
                    'leave_timestamp': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Activity recorded successfully'},
        400: {'description': 'Invalid input'}
    }
})
def create_activity():
    try:
        data = request.get_json()
        car_id = data.get("car_id")
        spot_id = data.get("spot_id")
        entrance_timestamp = data.get("entrance_timestamp")
        leave_timestamp = data.get("leave_timestamp")  # Optional

        create_activity_service(car_id, spot_id, entrance_timestamp, leave_timestamp)
        return jsonify({"message": "Activity recorded successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@activity_blueprint.route("/<int:activity_id>", methods=["PATCH"])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'car_id': {'type': 'integer'},
                    'spot_id': {'type': 'integer'},
                    'entrance_timestamp': {'type': 'string'},
                    'leave_timestamp': {'type': 'string'},
                    'status': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Activity updated successfully'},
        400: {'description': 'Invalid input'}
    }
})
def update_activity(activity_id):
    try:
        data = request.get_json()
        car_id = data.get("car_id")
        spot_id = data.get("spot_id")
        entrance_timestamp = data.get("entrance_timestamp")
        leave_timestamp = data.get("leave_timestamp")  # Optional
        status = data.get("status")

        update_activity_service(activity_id, car_id, spot_id, entrance_timestamp, leave_timestamp, status)
        return jsonify({"message": "Activity updated successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
