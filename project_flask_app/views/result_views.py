from flask import Blueprint, render_template, request
from src.features.scraping_result_to_mongodb import save_mongodb
from src.features.scraping_result_to_mysql import save_mysql
from src.features.convert_genre_code_to_genre_name import convert_genre_code_to_genre_name

result_bp = Blueprint('result', __name__)

@result_bp.route('/result', methods=['GET', 'POST'])
def result():
    # HTTP Method가 GET인 경우 result 페이지 렌더링
    if request.method == 'GET':
        return render_template('result.html')
    # HTTP Method가 POST인 경우 메인페이지에 입력된 Melon playlist 링크를 이용해 음악 장르 추천 후 result.html에 전달
    else:
        link = request.form["link"]
        save_mongodb(link)
        save_mysql()
        genre_name = convert_genre_code_to_genre_name()
        return render_template('result.html', genre_name=genre_name)