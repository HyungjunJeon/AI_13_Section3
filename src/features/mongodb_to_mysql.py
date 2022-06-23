import os
import pymysql
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

# MySQL DB 생성
conn = pymysql.connect(host='localhost', user='root', password= os.environ.get('MYSQL_PASSWORD'), charset='utf8')
cur = conn.cursor()

with conn:
    cur.execute('DROP DATABASE IF EXISTS projectdb;') # 중복 실행시 오류 방지
    cur.execute('CREATE DATABASE projectdb;')
    conn.commit()

# 생성된 projectdb 연결
conn = pymysql.connect(host='localhost', user='root', password= os.environ.get('MYSQL_PASSWORD'), db='projectdb', charset='utf8')
cur = conn.cursor()

with conn:
    # MongoDB project_song collection -> MySQL song_meta table
    cur.execute("DROP TABLE IF EXISTS song_meta;") # 중복 실행시 오류 방지
    cur.execute("""CREATE TABLE song_meta (
    id INT NOT NULL PRIMARY KEY,
    song_gn_dtl_gnr_basket TEXT,
    issue_date TEXT,
    album_name TEXT,
    album_id TEXT,
    artist_id_basket TEXT,
    song_name TEXT,
    song_gn_gnr_basket TEXT,
    artist_name_basket TEXT);""")

    collection = database['project_song']
    for d in collection.find():
        cur.execute("""INSERT INTO song_meta (
        id, song_gn_dtl_gnr_basket,
        issue_date, album_name,
        album_id, artist_id_basket,
        song_name, song_gn_gnr_basket,
        artist_name_basket
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """,
        (d['id'], d['song_gn_dtl_gnr_basket'],
        d['issue_date'], d['album_name'],
        d['album_id'], d['artist_id_basket'],
        d['song_name'], d['song_gn_gnr_basket'],
        d['artist_name_basket']))

    cur.execute("DROP TABLE IF EXISTS genre_gn_all;") # 중복 실행시 오류 방지
    cur.execute("""CREATE TABLE genre_gn_all (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        genre_code TEXT,
        genre_name TEXT);""")

    # MongoDB project_genre collection -> MySQL genre_gn_all table
    collection = database['project_genre']
    for d in collection.find():
        cur.execute("""INSERT INTO genre_gn_all (
            genre_code, genre_name
        ) VALUES (%s, %s);
        """,
        (d['genre_code'], d['genre_name']))
    conn.commit()