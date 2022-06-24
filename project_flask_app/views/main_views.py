
from flask import Blueprint, render_template, request

main_bp = Blueprint('main', __name__)

# 메인 페이지 렌더링
@main_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html'),200