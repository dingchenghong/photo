from flask import jsonify, request
from app.user.model import Users
from app.auth.auths import Auth
from .. import common


def init_api(app):
    @app.route('/')
    @app.route('/index')
    def index():
        return 'hello ding...'

    @app.route('/register', methods=['POST'])
    def register():
        """
        用户注册
        :return: json
        """
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        print(username)
        print(password)
        print(email)
        user = Users(email=email, username=username, password=Users.set_password(Users, password))
        result = Users.add(Users, user)
        print(result)
        if user.id:
            return_user = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'login_time': user.login_time
            }
            return jsonify(common.true_return(return_user, "用户注册成功"))
        else:
            return jsonify(common.false_return('', '用户注册失败'))

    @app.route('/login', methods=['POST'])
    def login():
        """
        用户登录
        :return: json
        """
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            return jsonify(common.false_return('', '用户名和密码不能为空'))
        else:
            return Auth.authenticate(Auth, username, password)

    @app.route('/user', methods=['GET'])
    def get():
        """
        获取用户信息
        :return: json
        """
        result = Auth.identify(Auth, request)
        if result['status'] and result['data']:
            user = Users.get(Users, result['data'])
            return_user = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'login_time': user.login_time
            }
            result = common.true_return(return_user, "请求成功")
        return jsonify(result)

