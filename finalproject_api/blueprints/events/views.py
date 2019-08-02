from flask import Flask, Blueprint, jsonify, make_response, request
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required
from models.events import Event
from flask_login import current_user

events_api_blueprint = Blueprint('events_api', __name__)

@events_api_blueprint.route('/', methods=['POST'])
@jwt_required
def create():
    event_name = request.json.get('event_name')
    description = request.json.get('description')
    location = request.json.get('location')
    host = current_user.id
    time = request.json.get('time')
    max_number=request.json.get('max_number')

    event =Event(event_name=event_name, description=description, location=location, host=host, time=time, max_number=max_number)

    if event.save():
        event = Event.get_by_id(event.id)
        response = {'message': 'Event successfully created',
                    'data': {
                        'event_name':event.event_name,
                        'description':event.description,
                        'location': event.location,
                        'host':event.host,
                        'max_number':event.max_number,
                    }}
        return make_response(jsonify(response), 200)
    else:
        response = {'message': 'Event creation failed'}
        return make_response(jsonify(response), 400)