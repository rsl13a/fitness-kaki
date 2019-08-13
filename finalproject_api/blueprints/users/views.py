from flask import Flask, Blueprint, jsonify, make_response, request
from models.user import User
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

users_api_blueprint = Blueprint('users_api', __name__)

@users_api_blueprint.route('/', methods=['GET'])
@jwt_required
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

   if len(password) <8:
      response ={ 'message': 'Password too short'}
      return make_response(jsonify(response), 400)
    
   else:
      hashed_password = generate_password_hash(password)        
      user = User(first_name=first_name, last_name=last_name, username=username, password=hashed_password, email=email)
      if user.save():
         response ={ 'message': 'Sign-up successful'}
         identity={
            'id': user.id,
         }
         auth_token =  create_access_token(identity = identity)
         response['data']={'JWT':auth_token}
         return make_response(jsonify(response), 200)

      else:
         message = ' .'.join(user.errors)
         response ={ 'message': message}
         return make_response(jsonify(response), 400)
   
@users_api_blueprint.route('/update', methods=['POST'])
@jwt_required
def update():
   current_user = get_jwt_identity()
   user = User.get_by_id(current_user)

   current_username = user.username
   current_first_name = user.first_name
   current_last_name = user.last_name
   current_email=user.email

   #update user details if there are any updates in JSON. else,use original detail stored in database
   user.username = request.json.get('username')
   if user.username==None or user.username=='':
      user.username = current_username
   
   user.first_name = request.json.get('first_name')
   if user.first_name==None or user.first_name=='':
      user.first_name = current_first_name

   user.last_name = request.json.get('last_name')
   if user.last_name==None or user.last_name=='':
      user.last_name = current_last_name

   user.email = request.json.get('email')
   if user.email==None or user.email=='':
      user.email = current_email
      

   # print(user.username)
   # user.email = request.json.get('email', user.email)
   # print(user.email)
   # user.first_name = request.json.get('first_name', user.first_name)
   # print(user.first_name)
   # user.last_name = request.json.get('last_name', user.last_name)
   # print(user.last_name)
   
   if user.save():
      updated_details={
         'username':user.username,
         'email':user.email,
         'first_name':user.first_name,
         'last_name':user.last_name
      }
      response={'message':'update successful', 'updated_details':updated_details}
      return make_response(jsonify(response), 200)
   else:
      response = {'message': 'user update failed', 'errors':user.errors}
      print(user.errors)
      return make_response(jsonify(response), 400)

