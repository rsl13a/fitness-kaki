from flask import Blueprint,make_response,jsonify, request
from models.guestlist import Guestlist
from models.user import User
from models.event import Event
from flask_jwt_extended import get_jwt_identity, jwt_required

guestlists_api_blueprint=Blueprint('guestlists_api', __name__)

#retrieve all guests - need?
# @guestlists_api_blueprint.route('/', methods=['GET'])
# def index():

@guestlists_api_blueprint.route('/', methods=['POST'])
@jwt_required
def create():
    event_id = request.json.get('event_id')
    guest = get_jwt_identity()
    event_details = Event.get_or_none(Event.id==event_id)
    if event_details!=None:
        guestlist = Guestlist.get_or_none(Guestlist.event == event_id, Guestlist.guest==guest)

        if guestlist!=None:
            #delete entry if it exists
            guestlist.delete_instance()
            response={'message':'guest removed from guestist'}
            return make_response(jsonify(response),200)

        else:
            guestlist = Guestlist(event = event_id, guest = guest)
            if guestlist.save():
                print(f'guest with id {guest} was saved for event_id: {event_id}')
                response={'message':'guest added'}
                return make_response(jsonify(response),200)
            else:
                print('guest_id not provided')
                error={'error':'guest id not provided'}
                return make_response(jsonify(error),200)

    else:
        print('event_id not exists')
        error={'error':'event id does not exist'}
        return make_response(jsonify(error),200)

#retrieve list of guests for an event. route(app/guestlists/:id) where id is the event id (GET)
#not quite correct. guestlist_id is 
@guestlists_api_blueprint.route('/<id>', methods=['GET'])
def show(id):
    data=[]
    event = Event.get_or_none(Event.id==id)
    if event:
        print('event exists')
        print(event)
        for guest in event.guests:
            user = User.get_by_id(guest)
            guest_data = {'id':user.id, 'profile_image':user.profile_image_url, 'username':user.username}
            data.append(guest_data)
        response={'message':'success', 'data': data}
        return make_response(jsonify(response),200)
    else:
        error ={'error':'no such event exists'}
        return make_response(jsonify(error),422)


#add guests for an event, (POST)
#remove guests for an event, (DELETE). axios.delete exists.
#edit guests
#clone an event & guest list