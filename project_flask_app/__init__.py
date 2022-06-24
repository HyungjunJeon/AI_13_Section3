import os
from flask import Flask

# Application Factory Pattern 적용
def create_app():
    app = Flask(__name__)

    from project_flask_app.views.main_views import main_bp
    from project_flask_app.views.result_views import result_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(result_bp)

    return app