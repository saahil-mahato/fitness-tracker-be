import os
import secrets

from flask import Flask

from app.db import db

from app.diet_recommender.diet_recommender_controller import diet_recommender_blueprint
from app.exercise_recommender.exercise_recommender_controller import exercise_recommender_blueprint
from app.user.user_controller import user_blueprint

def create_app():
    app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = secrets.token_hex(32)

    app.register_blueprint(diet_recommender_blueprint, url_prefix='/api/recommend-diet')
    app.register_blueprint(exercise_recommender_blueprint, url_prefix='/api/recommend-exercises')
    app.register_blueprint(user_blueprint, url_prefix='/api/users')

    db.init_app(app)
    
    with app.app_context():
        from app.models.user_model import User
        
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
