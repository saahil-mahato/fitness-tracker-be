import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import jaccard_score

class ExerciseRecommender():
    def __init__(self):
        self.filePath = os.path.abspath(os.getcwd()) + '/app/exercise_recommender/megaGymDataset.csv'
        self.features = ['Type', 'BodyPart', 'Level']

        self.load_data()
        self.preprocess_data()

    def load_data(self):
        self.rawDf = pd.read_csv(self.filePath)
        self.rawDf.fillna({'Rating': 0.0, 'RatingDesc': 'Low'}, inplace=True)
        self.rawDf.dropna(inplace=True)
        self.df = self.rawDf[self.features].copy()

    def preprocess_data(self):
        self.typeEncoder = LabelEncoder()
        self.bodyPartEncoder = LabelEncoder()
        self.levelEncoder = LabelEncoder()

        self.df['Type_encoded'] = self.typeEncoder.fit_transform(self.df['Type'])
        self.df['BodyPart_encoded'] = self.bodyPartEncoder.fit_transform(self.df['BodyPart'])
        self.df['Level_encoded'] = self.levelEncoder.fit_transform(self.df['Level'])

    def recommend_exercises(self, type, bodyPart, level, top_n=3):
        input_encoded = [
           self.typeEncoder.transform([type])[0],
           self.bodyPartEncoder.transform([bodyPart])[0],
           self.levelEncoder.transform([level])[0]
        ]

        similarities = []
        for i in range(len(self.df)):
            row = self.df.iloc[i][['Type_encoded', 'BodyPart_encoded', 'Level_encoded']].values
            similarity = jaccard_score(list(row), input_encoded, average='macro')
            similarities.append(similarity)

        tempDf = self.df.copy()
        tempDf['similarity'] = similarities
        tempDf['original_index'] = tempDf.index
        
        maxSimilarity = tempDf['similarity'].max()
        maxSimilarityDf = tempDf[tempDf['similarity'] == maxSimilarity]
        maxSimilarityDf['rating'] = self.rawDf[self.rawDf.index == tempDf.index]['Rating']

        topRated = maxSimilarityDf.nlargest(3, 'rating')
        originalTopRated = self.rawDf.loc[list(topRated.iloc[i]['original_index'] for i in range(0, len(topRated)))]
        originalTopRated = originalTopRated.drop(columns=['Unnamed: 0'])

        return originalTopRated.to_json(orient='records')


exerciseRecommender = ExerciseRecommender()