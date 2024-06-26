import jwt
import datetime

from flask import current_app

from sqlalchemy.inspection import inspect

from app.models.user_model import User
from app.db import db

def add_user(userData):
    user = User.query.filter_by(username=userData['username']).first()
    if user:
        return False
    
    new_user = User(
        username=userData['username'],
        firstName=userData['firstName'],
        lastName=userData['lastName'],
        age=userData['age'],
        weight=userData['weight'],
        height=userData['height'],
        gender=userData['gender'],
        activityLevel=userData['activityLevel'],
        isTrainer=userData['isTrainer']
    )
    new_user.password = userData['password']
    db.session.add(new_user)
    db.session.commit()
    return True

def update_user(userId, userData):
    user = getUser(userId)
    if not user:
        return False, {}

    user.username = userData.get('username', user.username)
    user.firstName = userData.get('firstName', user.firstName)
    user.lastName = userData.get('lastName', user.lastName)
    user.age = userData.get('age', user.age)
    user.weight = userData.get('weight', user.weight)
    user.height = userData.get('height', user.height)
    user.gender = userData.get('gender', user.gender)
    user.activityLevel = userData.get('activityLevel', user.activityLevel)
    user.isTrainer = userData.get('isTrainer', user.isTrainer)
    user.password = userData['password']
    
    db.session.commit()

    user_json = {}
    columns = inspect(User).columns.keys()
    for col in columns:
        if col in ('password', 'passwordHash') :
            continue
        user_json[col] = getattr(user, col)

    return True, user_json

def login(loginData):
    user = User.query.filter_by(username=loginData['username']).first()
    if not user:
        return False, "", {}, "User does not exist"
    if user.verify_password(loginData['password']):
        token = jwt.encode(
            {
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            },
            current_app._get_current_object().config['SECRET_KEY'],
            algorithm='HS256'
        )

        user_json = {}
        columns = inspect(User).columns.keys()
        for col in columns:
            if col in ('password', 'passwordHash') :
                continue
            user_json[col] = getattr(user, col)

        return True, token, user_json, ""
    return False, "", {}, "Invalid password"


def getUser(id):
    user = User.query.get(id)
    return user