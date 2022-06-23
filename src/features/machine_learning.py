import os
import pymysql
import ast
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from category_encoders import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
import pickle
from dotenv import load_dotenv

load_dotenv()

#MySQL projectdb DB 연결
conn = pymysql.connect(host='localhost', user='root', password= os.environ.get('MYSQL_PASSWORD'), db='projectdb', charset='utf8')
cur = conn.cursor()

# song_meta table DataFrame으로 가져오기
cur.execute("SELECT * FROM song_meta;")

result = cur.fetchall()

df = pd.DataFrame(result)
columns = ['id', 'song_gn_dtl_gnr_basket', 'issue_date', 'album_name', 'album_id', 'artist_id_basket', 'song_name', 'song_gn_gnr_basket', 'artist_name_basket']
df.columns = columns

# EDA
df = df.drop(['id', 'song_gn_dtl_gnr_basket', 'issue_date', 'album_id', 'artist_id_basket'], axis=1) # 불필요한 features 제거
# 2개 이상의 값이 list 형태로 묶여 있는 데이터 제거
df['song_gn_gnr_basket'] = df['song_gn_gnr_basket'].apply(lambda x: ast.literal_eval(x))
df['artist_name_basket'] = df['artist_name_basket'].apply(lambda x: ast.literal_eval(x))
df['song_gn_gnr_basket'] = df['song_gn_gnr_basket'].apply(lambda x: None if len(x) > 1 else x)
df['artist_name_basket'] = df['artist_name_basket'].apply(lambda x: None if len(x) > 1 else x)
df = df.dropna(axis=0)
df['song_gn_gnr_basket'] = df['song_gn_gnr_basket'].apply(lambda x: "".join(x))
df['artist_name_basket'] = df['artist_name_basket'].apply(lambda x: "".join(x))
# column명 한글로 변경 및 순서 변경
df.columns = ['앨범명', '곡명', '장르코드', '가수명']
df = df[['장르코드', '앨범명', '곡명', '가수명']]

# 총 데이터 개수가 약 71만개로 모델 학습 시 메모리 부족 문제로 1%만 샘플링
df = df.sample(frac=0.01, random_state=42)
df = df.reset_index(drop=True)

target = "장르코드" # 장르 추천 서비스를 개발하기 위해 target은 장르코드로 설정

# train, val, test 데이터셋 나누기
train, test = train_test_split(df, train_size=0.80, test_size=0.20, random_state=42)
train, val = train_test_split(train, train_size=0.75, random_state=42)

features = train.drop(columns=[target]).columns

X_train = train[features]
y_train = train[target]
X_val = val[features]
y_val = val[target]
X_test = test[features]

# 기준모델 설정 (최빈값)
major = y_val.mode()[0]
y_pred = [major] * len(y_val)

print(f"기준 정확도 : {accuracy_score(y_val, y_pred)}") # 기준모델 정확도 확인

# 파이프라인 구축
pipe = make_pipeline(
    OneHotEncoder(use_cat_names=True), 
    RandomForestClassifier(n_jobs=-1, random_state=42, oob_score=True)
)

pipe.fit(X_train, y_train) # 모델 학습 진행
print(f"검증 정확도: {pipe.score(X_val, y_val)}") # 학습 결과 정확도 확인

# 테스트 데이터
test_dict = {
    "앨범명": "Viva La Vida Or Death And All His Friends",
    "곡명": "Viva La Vida",
    "가수명": "Coldplay"
}

X_test = pd.DataFrame(test_dict, index=[0])

# 피클링 전 테스트 데이터로 예상값 확인
pred = pipe.predict(X_test)

print(pred[0])

# 모델학습 파이프라인 피클링
with open('pipeline.pkl', 'wb') as pickle_file:
    pickle.dump(pipe, pickle_file)

# 피클링한 파일 읽어오기
with open('pipeline.pkl', 'rb') as pickle_file:
    pipeline = pickle.load(pickle_file)



# 피클링 후 테스트 데이터로 예상값 확인
pred = pipeline.predict(X_test)

print(pred[0])
