from flask import Flask, Blueprint, jsonify, make_response, request
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from models.user import User


sessions_api_blueprint = Blueprint('sessions_api', __name__)

@sessions_api_blueprint.route('/login', methods=['POST'])
def new():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.get_or_none(User.username == username)

    if user==None:
        response = {'message': 'No such user'}
        return make_response(jsonify(response), 400)
    if check_password_hash(user.password, password):
        access_token = create_access_token(identity = user.id)
        response = {'message': 'Login successful', 'auth_token':access_token}
        return make_response(jsonify(response),200)