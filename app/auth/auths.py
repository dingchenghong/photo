import jwt, datetime, time
from flask import jsonify
from app.user.model import Users
from .. import config
from .. import common


class Auth:
    @staticmethod
    def encode_auth_token(user_id, login_time):
        """
        生成认证Token
        :param user_id: int
        :param login_time: int(timestamp)
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
                'iat': datetime.datetime.utcnow(),
                'iss': 'ken',
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
            # 取消过期时间验证
            payload = jwt.decode(auth_token, config.SECRET_KEY, options={'verify_exp': False})
            if 'data' in payload and 'id' in payload['data']:
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'

    def authenticate(self, user_name, password):
        """
        用户登录，登录成功返回token，写将登录时间写入数据库；登录失败返回失败原因
        :param user_name:
        :param password:
        :return: json
        """
        user_info = Users.query.filter_by(username=user_name).first()
        if user_info is None:
            return jsonify(common.false_return('', '找不到用户'))
        else:
            if Users.check_password(Users, user_info.password, password):
                login_time = int(time.time())
                user_info.login_time = login_time
                # Users.update(Users)
                token = self.encode_auth_token(user_info.id, login_time)
                return jsonify(common.true_return(token.decode(), '登录成功'))
            else:
                return jsonify(common.false_return('', '密码不正确'))

    def identify(self, request):
        """
        用户鉴权
        :return: list
        """
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token_arr = auth_header.split(" ")
            if not auth_token_arr or auth_token_arr[0] != 'JWT' or len(auth_token_arr) != 2:
                result = common.false_return('', '请传递正确的验证头信息')
            else:
                auth_token = auth_token_arr[1]
                payload = self.decode_auth_token(auth_token)
                if not isinstance(payload, str):
                    user = Users.get(Users, payload['data']['id'])
                    if user is None:
                        result = common.false_return('', '找不到该用户信息')
                    else:
                        if user.login_time == payload['data']['login_time']:
                            result = common.true_return(user.id, '请求成功')
                        else:
                            result = common.false_return('', 'Token已更改，请重新登录获取')
                else:
                    result = common.false_return('', payload)
        else:
            result = common.false_return('', '没有提供认证token')
        return result

