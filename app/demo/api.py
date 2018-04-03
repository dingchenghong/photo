from flask import jsonify, request
from app.user.model import Users
from app.common import resp


def init_demo(app):
    @app.route('/user/login', methods=['POST'])
    def dd():
        print('dfsfsdfsd=========sdfsdfs============sdfsdfds')
        user = dict()
        user['id'] = 12
        user['name'] = 'ding'
        data = dict()
        data['token'] = 'dfadfaf'
        data['user'] = user
        return jsonify(resp(data, '成功'))

    @app.route('/user/info', methods=['GET'])
    def info():
        roles = list()
        roles.append('admin')
        data = dict()
        data['role'] = roles
        data['name'] = 'admin'
        data['avatar'] = 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif'
        return jsonify(resp(data, '成功'))

