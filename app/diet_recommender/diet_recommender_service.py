import os
import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity


class DietRecommender():
    def __init__(self):
        self.filePath = os.path.abspath(os.getcwd() + '/app/diet_recommender/epi_r.csv')
        self.jsonPath = os.path.abspath(os.getcwd() + '/app/diet_recommender/full_format_recipes.json')
        self.features = ['calories', 'protein', 'fat', 'sodium']

        self.load_data()
        self.preprocess_data()


    def load_data(self):
        self.rawDf = pd.read_csv(self.filePath)
        self.rawDf.dropna(inplace=True)
        self.df = self.rawDf[self.features].copy()

        with open(self.jsonPath, 'r') as file:
            self.recipes = json.load(file)
    
    def preprocess_data(self):
        self.scaler = MinMaxScaler()
        self.normalizedFeatures = self.scaler.fit_transform(self.df[self.features].values)
        
    def recommend_recipes(self, calories, protein, fat, sodium, top_n=3):
        inputFeatures = self.scaler.transform(np.array([[calories, protein, fat, sodium]]))
        cosineSimMatrix = cosine_similarity(inputFeatures, self.normalizedFeatures)
        simScores = list(enumerate(cosineSimMatrix[0]))
        simScores = sorted(simScores, key=lambda x: x[1], reverse=True)
        simScores = simScores[:top_n]
        foodIndices = [i[0] for i in simScores]
        foodData = self.rawDf.iloc[foodIndices]
        foodData = foodData.to_dict(orient='records')

        recipeData = []
        for food in foodData:
            if food.get('title', '') == '':
                continue

            recipe = next((item for item in self.recipes if item.get('title', '') == food['title']), None)
            recipeData.append(recipe)
        
        return recipeData


dietRecommender = DietRecommender()
