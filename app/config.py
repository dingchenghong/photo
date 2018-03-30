DB_USER = 'root'
DB_PASSWORD = 'root123'
DB_HOST = 'localhost'
DB_DB = 'db_mine'
DB_PORT = '3306'

DEBUG = True
PORT = 3333
HOST = "192.168.1.216"
SECRET_KEY = "ding.photo_key"


SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + ':' + DB_PORT + '/' + DB_DB