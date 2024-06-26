from app.db import db
from app.models.user_model import User


def add_recommendation(userId, exercise, recipe, ):
    new_user = User(
        username=recommendationData['username'],
    )
    new_user.password = userData['password']
    db.session.add(new_user)
    db.session.commit()
    return True