from flask import Blueprint, request, jsonify
from diet_recommender.diet_recommender_service import dietRecommender

diet_recommender_blueprint = Blueprint('diet_recommender_blueprint', __name__)

@diet_recommender_blueprint.route('/', methods=['POST'])
def get_recommendation():
    diet_preference = request.get_json()
    if not diet_preference or not diet_preference['calories'] or not diet_preference['protein'] or not diet_preference['fat'] or not diet_preference['sodium']:
        return jsonify({"error": "Invalid data"}), 400
    
    recommendation = dietRecommender.recommend_recipes(
        calories=diet_preference['calories'],
        protein=diet_preference['protein'],
        fat=diet_preference['fat'],
        sodium=diet_preference['sodium']
    )

    return recommendation, 200