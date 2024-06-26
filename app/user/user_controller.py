from flask import Blueprint, request, jsonify
from app.user.user_service import add_user, update_user, login

user_blueprint = Blueprint('user_blueprint', __name__)

@user_blueprint.route('/add', methods=['POST'])
def addUserController():
    userData = request.get_json()
    if not userData:
        return jsonify({"error": "Payload is empty"}), 400
    
    isSuccess = add_user(userData)

    if not isSuccess:
        jsonify({'message': 'Username already exists'}), 400

    return jsonify({'message': 'User created successfully'}), 201


@user_blueprint.route('/update/<int:userId>', methods=['PUT'])
def updateUserController(userId):
    userData = request.get_json()
    if not userData:
        return jsonify({"error": "Payload is empty"}), 400
    
    isSuccess, user = update_user(userId, userData)

    if not isSuccess:
        jsonify({'message': 'There was an issue. Please try again.'}), 500

    return jsonify({'message': 'User updated successfully', 'user': user}), 200


@user_blueprint.route('/login', methods=['POST'])
def loginController():
    userData = request.get_json()
    if not userData:
        return jsonify({"error": "Payload is empty"}), 400
    
    isSuccess, token, user, error = login(userData)

    if not isSuccess:
        return jsonify({'message': error,}), 400

    return jsonify({'message': 'Succesfully logged in', 'token': token, 'user': user}), 200