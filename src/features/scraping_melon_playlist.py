import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def scraping(url):
    # Melon Playlist 공유 링크에서 사용자마다 달라지는 Seq, Key값 추출
    url = url

    resp = requests.get(url)

    seq= resp.url.split('sId=')[1]
    seq = seq.split('&ref')[0]

    key = resp.url.split('uId=')[1]
    key = key.split('&sId')[0]

    # Selenium, BeutifulSoup을 사용해 동적으로 생성되는 Playlist 목록 받아오기
    url = f"https://www.melon.com/mymusic/playlist/mymusicplaylistview_inform.htm?plylstSeq={seq}&memberKey={key}&ref=copyurl&snsGate=Y"

    resp = requests.get(url,headers={"User-Agent":"Mozilla/5.0"}) # Melon Playlist는 headers 값이 없으면 제대로 받아오지 못한다

    service = Service('./chromedriver/chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(3)
 
    driver.get(url)

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    result = {} # 곡명, 가수명, 앨범명을 return 해주기 위한 dictionary
    song_names_list = [] # 곡명 list
    artist_names_list = [] # 가수명 list
    album_names_list = [] # album명 list

    # Playlist 곡명 추출
    song_names = soup.find_all(class_='fc_gray')
    for name in song_names:
        song_names_list.append(name.get_text())

    # Playlist 가수명 추출
    artist_names = soup.findChildren(id='artistName')
    for name in artist_names:
        artist_names_list.append(name.get_text().strip())

    # Playlist 앨범명 추출
    # 앨범명의 경우 id값이 없고 class도 다른 태그와 구별되지 않아 가수명 태그 활용
    for name in artist_names:
        album_names_list.append(name.parent.parent.next_sibling.next_sibling.select('.fc_mgray')[0].get_text())

    # 각 list result dictionary에 담기
    result['song_names'] = song_names_list
    result['artist_names'] = song_names_list
    result['album_names'] = album_names_list

    return result