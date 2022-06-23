import csv
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# MONGODB SETUP
HOST = 'cluster0.jyiv0.mongodb.net'
USER = 'Hyungjun'
PASSWORD = os.environ.get('MONGODB_PASSWORD')
DATABASE_NAME = 'hyungjunDB'
MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)

database = client[DATABASE_NAME]

# song_meta.csv -> mongoDB
collection = database['project_song']

collection.delete_many({}) # 중복 실행시 데이터 누적 방지

with open('./src/data/song_meta.csv',  encoding='UTF-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if len(row) == 0: continue
        collection.insert_one({
            "song_gn_dtl_gnr_basket": row[0],
            "issue_date": row[1],
            "album_name": row[2],
            "album_id": row[3],
            "artist_id_basket": row[4],
            "song_name": row[5],
            "song_gn_gnr_basket": row[6],
            "artist_name_basket": row[7],
            "id": int(row[8])
        })

# genre_gn_all.csv -> mongoDB
collection = database['project_genre']

collection.delete_many({}) # 중복 실행시 데이터 누적 방지

with open('./src/data/genre_gn_all.csv', encoding='UTF-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if len(row) == 0: continue
        collection.insert_one({
            "genre_code": row[0],
            "genre_name": row[1]
        })