import os
import pymysql
from pymongo import MongoClient
from dotenv import load_dotenv

# Flask 앱에서 사용하기 위해 함수화
def save_mysql():
    load_dotenv()

    # MONGODB SETUP
    HOST = 'cluster0.jyiv0.mongodb.net'
    USER = 'Hyungjun'
    PASSWORD = os.environ.get('MONGODB_PASSWORD')
    DATABASE_NAME = 'hyungjunDB'
    MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

    client = MongoClient(MONGO_URI)

    database = client[DATABASE_NAME]

    # MySQL projectdb 연결
    conn = pymysql.connect(host='localhost', user='root', password= os.environ.get('MYSQL_PASSWORD'), db='projectdb', charset='utf8')
    cur = conn.cursor()

    with conn:
        # MongoDB project_scraping collection -> MySQL scraping_result
        cur.execute("DROP TABLE IF EXISTS scraping_result;") # 중복 실행시 오류 방지
        cur.execute("""CREATE TABLE scraping_result (
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            song_name TEXT,
            artist_name TEXT,
            album_name TEXT);""")

        collection = database['project_scraping']
        for d in collection.find():
            cur.execute("""INSERT INTO scraping_result (
                song_name,
                artist_name,
                album_name
                ) VALUES (%s, %s, %s);
                """,
                (d['song_names'], 
                d['artist_names'],
                d['album_names']))

        conn.commit()