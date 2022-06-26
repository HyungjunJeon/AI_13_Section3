import pandas as pd
import ast
import pymysql
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

# SQLite projectdb DB 생성 및 연결
sqconn = sqlite3.connect('data/projectdb.db')
sqcur = sqconn.cursor()

# MySQL projectdb DB 연결
myconn = pymysql.connect(host='localhost', user='root', password= os.environ.get('MYSQL_PASSWORD'), db='projectdb', charset='utf8')
mycur = myconn.cursor()

# MySQL song_meta 테이블 데이터 가져오기
mycur.execute("SELECT * FROM song_meta;")
result = mycur.fetchall()

sqcur.execute("DROP TABLE IF EXISTS song_meta;") # 중복 실행시 오류 방지

# 머신러닝 전처리 과정 후 내용을 담기위해 pandas로 동일한 작업 진행
df = pd.DataFrame(result)
columns = ['id', 'song_gn_dtl_gnr_basket', 'issue_date', 'album_name', 'album_id', 'artist_id_basket', 'song_name', 'song_gn_gnr_basket', 'artist_name_basket']
df.columns = columns

df = df.drop(['id', 'song_gn_dtl_gnr_basket', 'issue_date', 'album_id', 'artist_id_basket'], axis=1)
df['song_gn_gnr_basket'] = df['song_gn_gnr_basket'].apply(lambda x: ast.literal_eval(x))
df['artist_name_basket'] = df['artist_name_basket'].apply(lambda x: ast.literal_eval(x))
df['song_gn_gnr_basket'] = df['song_gn_gnr_basket'].apply(lambda x: None if len(x) > 1 else x)
df['artist_name_basket'] = df['artist_name_basket'].apply(lambda x: None if len(x) > 1 else x)
df = df.dropna(axis=0)
df['song_gn_gnr_basket'] = df['song_gn_gnr_basket'].apply(lambda x: "".join(x))
df['artist_name_basket'] = df['artist_name_basket'].apply(lambda x: "".join(x))
df.columns = ['album_name', 'song_name', 'genre_code', 'artist_name']

# pandas DataFrame -> SQLite song_meta 테이블
df.to_sql('song_meta', sqconn)

# MySQL genre_gn_all 테이블 -> SQLite genre_gn_all 테이블
sqcur.execute('DROP TABLE IF EXISTS genre_gn_all;')
sqcur.execute("""CREATE TABLE genre_gn_all (
    id INT NOT NULL  PRIMARY KEY,
    genre_code TEXT,
    genre_name TEXT);""")

with myconn:
        mycur.execute("SELECT * FROM genre_gn_all;")
        table = mycur.fetchall()
        for d in table:
            sqcur.execute("""INSERT INTO genre_gn_all (
                    id, genre_code, genre_name
                ) VALUES (?, ?, ?);
                """,
                (d[0], d[1], d[2]))
        sqconn.commit()