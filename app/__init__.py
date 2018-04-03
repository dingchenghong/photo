from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    print('dingdingding......................')
    app.config.from_object(config_name)
    # json返回的中文不是编码后的
    app.config['JSON_AS_ASCII'] = False

    @app.before_request
    def before_request():
        print('==== 在请求前 ====')

    @app.after_request
    def after_request(response):
        print('========== after request =======')
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

    from app.user.api import init_api
    init_api(app)

    from app.demo.api import init_demo
    init_demo(app=app)

    return app

