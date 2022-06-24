from src.features.scraping_melon_playlist import scraping
import os
from pymongo import MongoClient
from dotenv import load_dotenv

def save_mongodb(url):
    load_dotenv()

    # MONGODB SETUP
    HOST = 'cluster0.jyiv0.mongodb.net'
    USER = 'Hyungjun'
    PASSWORD = os.environ.get('MONGODB_PASSWORD')
    DATABASE_NAME = 'hyungjunDB'
    MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

    client = MongoClient(MONGO_URI)

    database = client[DATABASE_NAME]

    # scraping result -> MongoDB
    collection = database['project_scraping']

    collection.delete_many({}) # 중복 실행시 데이터 누적 방지

    result = scraping(url)

    for i in range(len(result['song_names'])):
        collection.insert_one({
                "song_names": result['song_names'][i],
                "artist_names": result['artist_names'][i],
                "album_names": result['album_names'][i]
            })