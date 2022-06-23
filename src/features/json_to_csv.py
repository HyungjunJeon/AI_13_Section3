import json
import csv
"""
Json 형식으로 되어 있는 원본 데이터를 CSV로 변환
원본 데이터 용량 문제로 Github에 푸시가 진행되지 않아 Github에는 원본 데이터 제외하고 푸시
"""

# song_meta.json -> song_meta.csv 변환
file = open('./data/song_meta.json', encoding='UTF-8')
rawdata = json.loads(file.read())

with open('./src/data/song_meta.csv', 'w', encoding='UTF-8') as file:
    writer = csv.DictWriter(file, fieldnames=rawdata[0].keys())
    writer.writeheader()
    writer.writerows(rawdata)

# genre_gn_all.json -> genre_gn_all.csv 변환
# genre_gn_all.json 파일의 내용 형식이 song_meta.json과 달라 별도 함수 없이 구현
file = open('./data/genre_gn_all.json', encoding='UTF-8')
rawdata = [json.loads(file.read())]

with open('./src/data/genre_gn_all.csv', 'w', encoding='UTF-8') as file:
    writer = csv.writer(file)
    writer.writerow(['genre_code', 'genre_name'])
    for i in range(len(rawdata[0])):
        writer.writerow([list(rawdata[0].keys())[i], list(rawdata[0].values())[i]])