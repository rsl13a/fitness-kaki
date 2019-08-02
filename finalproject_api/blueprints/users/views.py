from flask import Flask, Blueprint, jsonify, make_response, request
from models.user import User
from werkzeug.security import generate_password_hash


users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    users = User.select()

    user_list = []
    for user in users:
        user_list.append({
           'id': user.id,
           'first_name':user.first_name,
           'last_name' : user.last_name,
           'profile_pic_url':user.profile_image_url
        })
    response= {'data':user_list}
    return make_response(jsonify(response),200)

@users_api_blueprint.route('/', methods=['POST'])
def create():
   username = request.json.get('username', None)
   email = request.json.get('email', None)
   password = request.json.get('password', None)
   first_name = request.json.get('first_name', None)
   last_name = request.json.get('last_name', None)

   if len(password) <6:
      response ={ 'message': 'Password too short'}
      return make_response(jsonify(response), 400)
    
   else:
      hashed_password = generate_password_hash(password)        
      user = User(first_name=first_name, last_name=last_name, username=username, password=hashed_password, email=email)
      if user.save():
         response ={ 'message': 'Sign-up successful'}
         return make_response(jsonify(response), 200)
      else:
         message = ' .'.join(user.errors)
         response ={ 'message': message}
         return make_response(jsonify(response), 400)
