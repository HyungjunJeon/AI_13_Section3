# AI_13_Section3

---

## 코드스테이츠 Section3 프로젝트

### 사용자의 Melon Playlist 및 Melon Playlist 데이터를 통한 음악 장르 추천 서비스

### Crawling

#### 메인 페이지에서 결과 페이지로 넘어가는 과정에 동작해서 사용자 Melon Playlist 데이터 수집

### DB (MySQL, MongoDB, SQLite3)

#### src/features에 DB 관련 코드가 작성되어 있음

#### NOSQL과 SQL 모두 활용해보기 위해 MongoDB에 적재 후 MySQL에도 적재

#### SQLite3는 Metabase 연동을 위해 활용

### Modeling

#### Recommend => Randomforest 를 사용해 음악 장르 추천


### Flask(WAS)

#### - HTML, CSS, Views.py 별도 분리 작성

#### - DB와 연동


# 동작 예시
![음악 장르 추천 서비스 시연](https://user-images.githubusercontent.com/65811799/200488131-6ad33df1-07a1-4718-9f2c-4e12e9a5abe3.gif)

# Web 소개

### 1. Main : Melon Playlist 공유 링크 입력

### 2. Result : 입력받은 Melon Playlist에서 데이터 수집 후 ML모델을 통해 음악 장르 추천 + DashBoard 확인 가능
