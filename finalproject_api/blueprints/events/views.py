from flask import Flask, Blueprint, jsonify, make_response, request
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required
from models.event import Event
from flask_login import current_user

events_api_blueprint = Blueprint('events_api', __name__)

@events_api_blueprint.route('/', methods=['POST'])
# @jwt_required
def create():
    name = request.json.get('name')
    description = request.json.get('description')
    location = request.json.get('location')
    host = request.json.get('host')
    time = request.json.get('time')
    max_number= request.json.get('max_number')

    event =Event(name=name, description=description, location=location, host=host, time=time, max_number=max_number)

    if event.save():
        print('event saved')
        event = Event.get_by_id(event.id)
        response = {'message': 'Event successfully created',
                    'data': {
                        'name':event.name,
                        'description':event.description,
                        'location': event.location,
                        'host':event.host.id,
                        'max_number':event.max_number,
                        'time':event.time
                    }}
        return make_response(jsonify(response), 200)
    else:
        response = {'message': 'Event creation failed'}
        return make_response(jsonify(response), 400)

#retrieve a list of all events
@events_api_blueprint.route('/', methods=['GET'])
def index():
    response=[]
    events = Event.select()
    for event in events:
        details={
                'id':event.id,
                'name':event.name,
                'description':event.description,
                'location': event.location,
                'host':event.host.id,
                'max_number':event.max_number,
                'time':event.time}
        response.append(details)

    if len(response)!=0:
        return make_response(jsonify(response), 200)
    else:
        response = {'message': 'No events'}
        return make_response(jsonify(response), 200)

