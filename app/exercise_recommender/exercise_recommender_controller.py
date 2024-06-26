from flask import Blueprint, request, jsonify
from app.exercise_recommender.exercise_recommender_service import exerciseRecommender

exercise_recommender_blueprint = Blueprint('exercise_recommender_blueprint', __name__)

@exercise_recommender_blueprint.route('/<int:userId>', methods=['POST'])
def get_recommendation_controller(userId):
    if not userId:
        return jsonify({"error": "No user Id given"}), 400
    
    exercise_preference = request.get_json()
    if not exercise_preference:
        return jsonify({"error": "Payload is empty"}), 400
    
    hasError, errorMessages = exerciseRecommender.validatePayload(exercise_preference)
    if hasError:
        return jsonify(errorMessages), 400
    
    recommendation = exerciseRecommender.recommend_exercises(
        userId,
        exercise_preference['type'],
        exercise_preference['bodyPart'],
        exercise_preference['level']
    )

    return recommendation, 200

@exercise_recommender_blueprint.route('/rate', methods=['PUT'])
def change_rating_controller():
    ratingData = request.get_json()

    isSuccess, message =  exerciseRecommender.update_rating(ratingData)
    if not isSuccess:
        return jsonify({'message': message}), 400
    
    return jsonify({'message': message}), 200


@exercise_recommender_blueprint.route('/list', methods=['GET'])
def get_all_exercises_controller():
    exercises = exerciseRecommender.get_all_exercises()

    return jsonify(exercises), 200
