import os
import json
import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

from app.user.user_service import getUser

class DietRecommender():
    def __init__(self):
        self.filePath = os.path.abspath(os.getcwd() + '/app/diet_recommender/recipe.csv')
        self.jsonPath = os.path.abspath(os.getcwd() + '/app/diet_recommender/recipe.json')
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
        
        self.rawDf.fillna({'rating': 0.0, 'calories': 0.0, 'protein': 0.0, 'fat': 0.0}, inplace=True)
        self.rawDf.dropna(inplace=True)
        self.rawDf = self.rawDf.drop_duplicates(subset=['title'])
        self.df = self.rawDf.copy()

        with open(self.jsonPath, 'r') as file:
            self.recipes = json.load(file)
        file.close()
        

    def validate_health_data(self, age, weight, height, gender, activityLevel):
        hasError = False
        errorMessages = {}

        if not isinstance(age, (int, float)) or (age <= 0 or age >= 100):
            hasError = True
            errorMessages['age'] = "Age must be a number between 0 and 100 (years)"

        if not isinstance(weight, (int, float)):
            hasError = True
            errorMessages['weight'] = "Weight must be a number (kg)"

        if not isinstance(height, (int, float)):
            hasError = True
            errorMessages['height'] = "Height must be a number between 0 and 300 (cms)"

        if gender not in ('male', 'female'):
            hasError = True
            errorMessages['gender'] = "Gender must be either 'male' or 'female'"

        if activityLevel not in self.activityFactor.keys():
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
        

    def recommend_recipes(self, userId, top_n=3):
        user = getUser(userId)

        hasError, errorMessages = self.validate_health_data(user.age, user.weight, user.height, user.gender, user.activityLevel)
        if hasError:
            return False, errorMessages
        
        nutrition = self.calculate_nutrition(user.age, user.weight, user.height, user.gender, user.activityLevel)
        inputFeatures = np.array([nutrition['calories'], nutrition['protein'], nutrition['fat']]).reshape(1, -1)

        self.df['similarity'] = cosine_similarity(inputFeatures, self.df[self.features].values)[0]
        self.df = self.df.sort_values(by=['similarity', 'rating'], ascending=[False, False])

        topFoods = self.df.head(top_n).to_dict(orient='records')
        
        recipeData = []
        for food in topFoods:
            for item in self.recipes:
                if item and item['title'] == food['title']:
                    recipeData.append(item)
        
        self.load_data()

        return True, {
            'recommendedDailyNutrition': nutrition,
            'possibleRecipes': recipeData
        }
    

    def update_rating(self, ratingData):
        user = getUser(ratingData["userId"])
        if not user.isTrainer:
            return False, "User doesn't have permission"
        
        self.rawDf.loc[self.rawDf['title'].str.strip() == ratingData['title'].strip(), 'rating'] = ratingData['rating']

        self.rawDf.to_csv(self.filePath, index=False)

        self.load_data()

        return True, f"Successfully changed rating of {ratingData['title'].strip()}"
    

    def get_all_recipes(self):
        return self.rawDf['title'].unique().tolist()


dietRecommender = DietRecommender()
