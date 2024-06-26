import os
import pandas as pd
import googleapiclient.discovery

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import jaccard_score

from app.user.user_service import getUser, addLatestExercises


class ExerciseRecommender():
    def __init__(self):
        self.filePath = os.path.abspath(os.getcwd()) + '/app/exercise_recommender/megaGymDataset.csv'
        self.features = ['Type', 'BodyPart', 'Level']

        self.load_data()
        self.preprocess_data()


    def load_data(self):
        self.rawDf = pd.read_csv(self.filePath)
        self.rawDf.fillna({'Rating': 0.0}, inplace=True)
        self.rawDf.dropna(inplace=True)
        self.df = self.rawDf.copy()


    def preprocess_data(self):
        self.typeEncoder = LabelEncoder()
        self.bodyPartEncoder = LabelEncoder()
        self.levelEncoder = LabelEncoder()

        self.df['Type_encoded'] = self.typeEncoder.fit_transform(self.df['Type'])
        self.df['BodyPart_encoded'] = self.bodyPartEncoder.fit_transform(self.df['BodyPart'])
        self.df['Level_encoded'] = self.levelEncoder.fit_transform(self.df['Level'])


    def validatePayload(self, payload):
        hasError = False
        errorMessages = {}

        if payload['type'] not in self.rawDf['Type'].unique():
            hasError = True
            errorMessages['Type'] = f"{payload['type']} is not a valid type"

        if payload['bodyPart'] not in self.rawDf['BodyPart'].unique():
            hasError = True
            errorMessages['BodyPart'] = f"{payload['bodyPart']} is not a valid body part"

        if payload['level'] not in self.rawDf['Level'].unique():
            hasError = True
            errorMessages['Level'] = f"{payload['level']} is not a valid level"

        return hasError, errorMessages
    

    def get_top_youtube_videos(self, exerciseTitle, max_results=5):
        # Replace with your YouTube Data API key
        api_key = "AIzaSyB3ZWzahpXKXTiaw2rXalPNxcGcO3hgTuU"

        # Create a service object for YouTube Data API v3
        youtube = googleapiclient.discovery.build(
            "youtube", "v3", developerKey=api_key)

        # Define the search request parameters
        request = youtube.search().list(
            part="snippet",
            q=exerciseTitle,
            maxResults=max_results,
            type="video"
        )

        # Execute the search request
        response = request.execute()

        # Extract video links from the response
        links = []
        for item in response['items']:
            video_id = item['id']['videoId']
            link = video_id
            links.append(link)

        return links


    def recommend_exercises(self, userId, type, bodyPart, level, top_n=3):
        input_encoded = [
           self.typeEncoder.transform([type])[0],
           self.bodyPartEncoder.transform([bodyPart])[0],
           self.levelEncoder.transform([level])[0]
        ]

        calculate_similarity = lambda row: jaccard_score(row, input_encoded, average='macro')

        # Apply the function to each row and store the result in the 'similarity' column
        self.df['similarity'] = self.df[['Type_encoded', 'BodyPart_encoded', 'Level_encoded']].apply(
            lambda row: calculate_similarity(row),
            axis=1
        )
        
        self.df = self.df.sort_values(by=['similarity', 'Rating'], ascending=[False, False])
        topExercises = self.df.head(top_n)
        topExercises = topExercises.drop(columns=['BodyPart_encoded', 'Level_encoded', 'Type_encoded']).to_dict(orient='records')
        
        for record in topExercises:
            record['youtube_links'] = self.get_top_youtube_videos(record['Title'])

        addLatestExercises(userId, topExercises)

        self.load_data()
        self.preprocess_data()

        return topExercises
    

    def update_rating(self, ratingData):
        user = getUser(ratingData["userId"])
        if not user.isTrainer:
            return False, "User doesn't have permission"
        
        self.rawDf.loc[self.rawDf['Title'].str.strip() == ratingData['title'].strip(), 'Rating'] = ratingData['rating']

        self.rawDf.to_csv(self.filePath, index=False)

        self.load_data()
        self.preprocess_data()

        return True, f"Successfully changed rating of {ratingData['title'].strip()}"
    

    def get_all_exercises(self):
        return self.rawDf['Title'].unique().tolist()


exerciseRecommender = ExerciseRecommender()
