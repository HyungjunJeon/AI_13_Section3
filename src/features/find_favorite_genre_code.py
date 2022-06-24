import os
import pymysql
from pymongo import MongoClient
import pickle
import pandas as pd
from collections import Counter
from dotenv import load_dotenv

def find_genre_code():
    load_dotenv()

    # MySQL projectdb 연결
    conn = pymysql.connect(host='localhost', user='root', password= os.environ.get('MYSQL_PASSWORD'), db='projectdb', charset='utf8')
    cur = conn.cursor()

    # 피클 파일 읽어오기
    with open('pipeline.pkl', 'rb') as pickle_file:
            pipeline = pickle.load(pickle_file)

    pred_list = [] # playlist의 각 곡에 대한 장르코드 예측값을 담을 list

    with conn:
        # Scraping 결과 DB에서 읽어오기
        cur.execute("SELECT * FROM scraping_result;")

        scraping_data = cur.fetchall()

        # 읽어온 데이터로 장르코드를 예측해 list에 담기
        for data in scraping_data:
            test_dict = {
                "앨범명": data[3],
                "곡명": data[1],
                "가수명": data[2]
            }

            X_test = pd.DataFrame(test_dict, index=[0])

            pred = pipeline.predict(X_test)

            pred_list.append(pred[0])  

        # list에 담긴 예측값 중 가장 많은 값을 찾아 return
        cnt = Counter(pred_list)
        
        favorite_genre_code = cnt.most_common(1)[0][0]

        return favorite_genre_code
