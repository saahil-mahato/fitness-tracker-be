from flask import Blueprint, request, jsonify
from app.diet_recommender.diet_recommender_service import dietRecommender

diet_recommender_blueprint = Blueprint('diet_recommender_blueprint', __name__)

@diet_recommender_blueprint.route('/<int:userId>', methods=['GET'])
def get_recommendation_controller(userId):
    if not userId:
        return jsonify({"error": "No user Id given"}), 400
    
    isSuccess, result = dietRecommender.recommend_recipes(userId)

    if not isSuccess:
        return result, 400

    return result, 200


@diet_recommender_blueprint.route('/rate', methods=['PUT'])
def change_rating_controller():
    ratingData = request.get_json()

    isSuccess, message =  dietRecommender.update_rating(ratingData)
    if not isSuccess:
        return jsonify({'message': message}), 400
    
    return jsonify({'message': message}), 200


@diet_recommender_blueprint.route('/list', methods=['GET'])
def get_all_recipes_controller():
    recipes = dietRecommender.get_all_recipes()

    return jsonify(recipes), 200