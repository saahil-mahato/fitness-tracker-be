from flask import Blueprint, request, jsonify
from app.diet_recommender.diet_recommender_service import dietRecommender

diet_recommender_blueprint = Blueprint('diet_recommender_blueprint', __name__)

@diet_recommender_blueprint.route('/', methods=['POST'])
def get_recommendation():
    userHealthData = request.get_json()
    if not userHealthData:
        return jsonify({"error": "Empty payload"}), 400
    
    hasError, errorMessages = dietRecommender.validate_payload(userHealthData)
    if hasError:
        return jsonify(errorMessages), 400
    
    recommendation = dietRecommender.recommend_recipes(
        age=userHealthData['age'],
        weight=userHealthData['weight'],
        height=userHealthData['height'],
        gender=userHealthData['gender'],
        activityLevel=userHealthData['activityLevel']
    )

    return recommendation, 200