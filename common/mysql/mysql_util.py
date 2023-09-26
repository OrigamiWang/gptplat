import pymysql as mysql
from flask import g, Flask, session
from common.util import read_yaml, get_num_by_role


def get_db():
    if not hasattr(g, 'db'):
        db = mysql.connect(host=read_yaml('database.mysql.host'),
                           user=read_yaml('database.mysql.username'),
                           password=read_yaml('database.mysql.password'),
                           db=read_yaml('database.mysql.db'),
                           port=read_yaml('database.mysql.port'),
                           charset='utf8')
    return db


app = Flask(__name__)
with app.app_context():
    db = get_db()




if __name__ == '__main__':
    history_list = (query_history())
    print(str(history_list))
