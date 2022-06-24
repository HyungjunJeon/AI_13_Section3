import os
import pymysql
from src.features.find_favorite_genre_code import find_genre_code
from dotenv import load_dotenv

def convert_genre_code_to_genre_name():
    load_dotenv()

    # MySQL projectdb 연결
    conn = pymysql.connect(host='localhost', user='root', password= os.environ.get('MYSQL_PASSWORD'), db='projectdb', charset='utf8')
    cur = conn.cursor()

    # playlist에서 가장 많이 예측된 장르코드
    favorite_genre_code = find_genre_code() 

    # DB에서 가장 많이 예측된 장르코드에 해당하는 장르명 찾아서 return
    cur.execute(f"SELECT genre_name FROM genre_gn_all WHERE genre_code = '{favorite_genre_code}'")

    favorite_genre_name = cur.fetchall()[0][0]

    return favorite_genre_name
