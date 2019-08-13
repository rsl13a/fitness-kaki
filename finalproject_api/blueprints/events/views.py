from flask import Flask, Blueprint, jsonify, make_response, request
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.event import Event
from models.user import User
from models.guestlist import Guestlist
from flask_login import current_user

events_api_blueprint = Blueprint('events_api', __name__)

@events_api_blueprint.route('/', methods=['POST'])
@jwt_required
def create():
    name = request.json.get('name')
    description = request.json.get('description')
    location = request.json.get('location')
    host = get_jwt_identity()
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
# @jwt_required
def index():
    response=[]
    events = Event.select().order_by(Event.time.desc())

    for event in events:
        data={
                'id':event.id,
                'name':event.name,
                'description':event.description,
                'location': event.location,
                'max_number':event.max_number,
                'time':event.time}
        
        #obtain names of host, guests and provide in event
        host = {'id':event.host.id, 'username':event.host.username, 'profile_image_url':event.host.profile_image_url}
        data['host'] = host
        guestlistExists = Guestlist.get_or_none(Guestlist.event == event.id)
        if guestlistExists!=None:
            guestlist = User.select().join(Guestlist, on=(Guestlist.guest == User.id)).where(Guestlist.event == event.id)
            roster=[]
            for entry in guestlist:
                roster.append({
                    'id':entry.id,
                    'username':entry.username,
                    'profile_image_url':entry.profile_image_url
                })
        else:
            roster='no guests'
        
        data['guests']=roster
        response.append(data)
    return make_response(jsonify(response), 200)

