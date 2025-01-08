from flasgger import swag_from
from flask import Blueprint, request, jsonify

from backend.models.activity import get_all_activities, get_activity, add_activity, \
    get_activities_by_registration_number

activity_bp = Blueprint('activity_bp', __name__)


@activity_bp.route('/', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'A list of activities',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'activity_id': {'type': 'integer'},
                        'registration_number': {'type': 'string'},
                        'spot_id': {'type': 'integer'},
                        'type': {'type': 'string'},
                        'timestamp': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def list_activities():
    activities = get_all_activities()
    return jsonify([dict(activity) for activity in activities])


@activity_bp.route('/<int:activity_id>', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'activity_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the activity to retrieve'
        }
    ],
    'responses': {
        200: {
            'description': 'An activity',
            'schema': {
                'type': 'object',
                'properties': {
                    'activity_id': {'type': 'integer'},
                    'registration_number': {'type': 'string'},
                    'spot_id': {'type': 'integer'},
                    'type': {'type': 'string'},
                    'timestamp': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Activity not found'
        }
    }
})
def retrieve_activity(activity_id):
    activity = get_activity(activity_id)
    if activity is None:
        return jsonify({"error": "Activity not found"}), 404
    return jsonify(dict(activity))


@activity_bp.route('/', methods=['POST'])
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
                    'spot_id': {'type': 'integer'},
                    'type': {'type': 'string'},
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Activity created successfully'
        }
    }
})
def create_activity():
    data = request.get_json()
    add_activity(data['registration_number'], data.get('spot_id'), data['type'])
    return jsonify({"message": "Activity created successfully"}), 201


@activity_bp.route('/registration/<string:registration_number>', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'registration_number',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'The registration number of the activities to retrieve'
        }
    ],
    'responses': {
        200: {
            'description': 'A list of activities for the given registration number',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'activity_id': {'type': 'integer'},
                        'registration_number': {'type': 'string'},
                        'spot_id': {'type': 'integer'},
                        'type': {'type': 'string'},
                        'timestamp': {'type': 'string'}
                    }
                }
            }
        },
        404: {
            'description': 'No activities found for the given registration number'
        }
    }
})
def retrieve_activities_by_registration_number(registration_number):
    activities = get_activities_by_registration_number(registration_number)
    if not activities:
        return jsonify({"error": "No activities found for the given registration number"}), 404
    return jsonify([dict(activity) for activity in activities])
