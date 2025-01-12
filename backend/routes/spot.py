from flasgger import swag_from
from flask import Blueprint, request, jsonify

from backend.models.spot import add_spot, get_all_spots, get_spot, update_spot, delete_spot

spot_bp = Blueprint('spot_bp', __name__)


@spot_bp.route('/', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'A list of spots',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'spot_id': {'type': 'integer'},
                        'spot_number': {'type': 'string'},
                        'registration_number': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def list_spots():
    spots = get_all_spots()
    return jsonify([dict(spot) for spot in spots])


@spot_bp.route('/<int:spot_id>', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'spot_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the spot to retrieve'
        }
    ],
    'responses': {
        200: {
            'description': 'A spot',
            'schema': {
                'type': 'object',
                'properties': {
                    'spot_id': {'type': 'integer'},
                    'spot_number': {'type': 'string'},
                    'registration_number': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Spot not found'
        }
    }
})
def retrieve_spot(spot_id):
    spot = get_spot(spot_id)
    if spot is None:
        return jsonify({"error": "Spot not found"}), 404
    return jsonify(dict(spot))


@spot_bp.route('/', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'spot_number': {'type': 'string'},
                    'registration_number': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Spot created successfully'
        }
    }
})
def create_spot():
    data = request.get_json()
    add_spot(data['spot_number'], data.get('registration_number'))
    return jsonify({"message": "Spot created successfully"}), 201


@spot_bp.route('/<int:spot_id>', methods=['PUT'])
@swag_from({
    'parameters': [
        {
            'name': 'spot_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the spot to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'spot_number': {'type': 'string'},
                    'registration_number': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Spot updated successfully'
        },
        404: {
            'description': 'Spot not found'
        }
    }
})
def update_spot_route(spot_id):
    data = request.get_json()
    if get_spot(spot_id) is None:
        return jsonify({"error": "Spot not found"}), 404
    update_spot(spot_id, data['spot_number'], data.get('registration_number'))
    return jsonify({"message": "Spot updated successfully"}), 200


@spot_bp.route('/<int:spot_id>', methods=['DELETE'])
@swag_from({
    'parameters': [
        {
            'name': 'spot_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the spot to delete'
        }
    ],
    'responses': {
        200: {
            'description': 'Spot deleted successfully'
        },
        404: {
            'description': 'Spot not found'
        }
    }
})
def delete_spot_route(spot_id):
    if get_spot(spot_id) is None:
        return jsonify({"error": "Spot not found"}), 404
    delete_spot(spot_id)
    return jsonify({"message": "Spot deleted successfully"}), 200
