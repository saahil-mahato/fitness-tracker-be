import os
import time
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import jaccard_score
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class ExerciseRecommender():
    def __init__(self):
        self.filePath = os.path.abspath(os.getcwd()) + '/app/exercise_recommender/megaGymDataset.csv'
        self.features = ['Type', 'BodyPart', 'Level']

        self.load_data()
        self.preprocess_data()

        #chrome
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")  # Ensure GUI is off
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Set up the Chrome service
        self.service = Service(ChromeDriverManager().install())

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
        # Format the query to be URL-friendly
        exerciseTitle = exerciseTitle.replace(' ', '+')
        
        # URL for YouTube search
        url = f'https://www.youtube.com/results?search_query={exerciseTitle}'

        driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        
        # Load the page
        driver.get(url)
        
        # Wait for the page to load
        time.sleep(2)
        
        # Find all video links
        video_links = []
        videos = driver.find_elements(By.XPATH, '//a[@id="video-title"]')
        for video in videos[:max_results]:
            video_link = video.get_attribute('href')
            if video_link and '/watch?v=' in video_link:
                video_links.append(video_link)
        
        # Close the driver
        driver.quit()
        
        return video_links

    def recommend_exercises(self, type, bodyPart, level, top_n=3):
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
        
        self.df[['rating', 'title']] = self.rawDf.loc[self.df.index, ['Rating', 'Title']]
        self.df = self.df.sort_values(by=['similarity', 'rating'], ascending=[False, False])
        topExercises = self.df.head(top_n).to_dict(orient='records')

        for record in topExercises:
            record['youtube_links'] = self.get_top_youtube_videos(record['title'])

        self.load_data()
        self.preprocess_data()

        return topExercises


exerciseRecommender = ExerciseRecommender()
