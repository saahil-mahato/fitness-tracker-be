from flask import Flask
from app.diet_recommender.diet_recommender_controller import diet_recommender_blueprint
from app.exercise_recommender.exercise_recommender_controller import exercise_recommender_blueprint

app = Flask(__name__)
app.register_blueprint(diet_recommender_blueprint, url_prefix='/api/recommend-diet')
app.register_blueprint(exercise_recommender_blueprint, url_prefix='/api/recommend-exercises')

if __name__ == '__main__':
    app.run(debug=True)
