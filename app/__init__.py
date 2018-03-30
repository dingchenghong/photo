from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers
        return response

    from app.user.model import db
    db.init_app(app)
    # 要加上create_all，要不不会自动创建表
    db.create_all(app=app)
    print('================ 1111111111111 ==============')

    from app.user.api import init_api
    init_api(app)
    print('================ 2222222222222 ==============')

    return app
