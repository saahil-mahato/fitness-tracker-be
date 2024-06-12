from flask import Blueprint, request, jsonify
from diet_recommender.diet_recommender_service import dietRecommender

diet_recommender_blueprint = Blueprint('diet_recommender_blueprint', __name__)

@diet_recommender_blueprint.route('/', methods=['POST'])
def get_recommendation():
    bioData = request.get_json()
    if not bioData or not bioData['age'] or not bioData['weight'] or not bioData['height'] or not bioData['gender'] or not bioData['activityLevel']:
        return jsonify({"error": "Invalid data"}), 400
    
    recommendation = dietRecommender.recommend_recipes(
        age=bioData['age'],
        weight=bioData['weight'],
        height=bioData['height'],
        gender=bioData['gender'],
        activityLevel=bioData['activityLevel']
    )

    return recommendation, 200