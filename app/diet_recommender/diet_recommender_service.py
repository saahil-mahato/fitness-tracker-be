import os
import json
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class DietRecommender():
    def __init__(self):
        self.filePath = os.path.abspath(os.getcwd() + '/app/diet_recommender/epi_r.csv')
        self.jsonPath = os.path.abspath(os.getcwd() + '/app/diet_recommender/full_format_recipes.json')
        self.features = ['calories', 'protein', 'fat']

        self.activityFactor = {
            'Sedentary': 1.2,
            'Lightly active': 1.375,
            'Moderately active': 1.55,
            'Very active': 1.725,
            'Super active': 1.9
        }

        self.load_data()



    def load_data(self):
        self.rawDf = pd.read_csv(self.filePath).loc[:, ['title', 'calories', 'fat', 'protein', 'sodium', 'rating']]
        self.rawDf = self.rawDf.loc[self.rawDf['rating'] >= 5.0]
        self.rawDf.fillna({'rating': 0.0, 'calories': 0.0, 'protein': 0.0, 'fat': 0.0}, inplace=True)
        self.rawDf.dropna(inplace=True)
        self.df = self.rawDf.copy()

        with open(self.jsonPath, 'r') as file:
            self.recipes = json.load(file)
        file.close()
        
    def validate_payload(self, payload):
        hasError = False
        errorMessages = {}

        if not isinstance(payload['age'], (int, float)) or (payload['age'] <= 0 or payload['age'] >= 100):
            hasError = True
            errorMessages['age'] = "Age must be a number between 0 and 100 (years)"

        if not isinstance(payload['weight'], (int, float)):
            hasError = True
            errorMessages['weight'] = "Weight must be a number (kg)"

        if not isinstance(payload['height'], (int, float)):
            hasError = True
            errorMessages['height'] = "Height must be a number between 0 and 300 (cms)"

        if payload['gender'] not in ('male', 'female'):
            hasError = True
            errorMessages['gender'] = "Gender must be either 'male' or 'female'"

        if payload['activityLevel'] not in self.activityFactor.keys():
            hasError = True
            errorMessages['activityLevel'] = "Activity Level is not valid"

        return hasError, errorMessages
        

    def calculate_nutrition(self, age, height, weight, gender, activity_level):
        nutrition = {}

        bmr = 0
        if gender == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        elif gender == 'female':
            bmr = 10 * weight + 6.25 * height - 5 * age -161

        nutrition['calories'] = bmr * self.activityFactor[activity_level]

        nutrition['protein'] = 0.8 * weight
        nutrition['fat'] = nutrition['calories']/9

        return nutrition
        
    def recommend_recipes(self, age, weight, height, gender, activityLevel, top_n=3):
        nutrition = self.calculate_nutrition(age, weight, height, gender, activityLevel)
        inputFeatures = np.array([nutrition['calories'], nutrition['protein'], nutrition['fat']]).reshape(1, -1)

        self.df['similarity'] = cosine_similarity(inputFeatures, self.df[self.features].values)[0]
        self.df = self.df.sort_values(by=['similarity', 'rating'], ascending=[False, False])

        topFoods = self.df.head(top_n).to_dict(orient='records')
        
        recipeData = []
        for food in topFoods:
            if food.get('title', '') == '':
                continue

            recipe = next((item for item in self.recipes if item.get('title', '') == food['title']), None)
            recipeData.append(recipe)
        
        self.load_data()

        return {
            'recommendedDailyNutrition': nutrition,
            'possibleRecipes': recipeData
        }


dietRecommender = DietRecommender()
