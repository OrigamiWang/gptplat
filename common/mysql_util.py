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


def execute_sql(sql):
    with db.cursor() as cursor:
        cursor.execute(sql)
    return cursor.fetchall()


def insert_content_table(content_arr):
    with db.cursor() as cursor:
        sql = "INSERT INTO content(`session_id`, `role`, `sentence`) VALUES"
        sql_arr = []
        for content in content_arr:
            value = "(\'" + content['sessionId'] + "\'," + str(get_num_by_role(content['role'])) + ",\'" + content[
                'content'] + "\'),"
            sql_arr.append(value)
        sql += "".join(sql_arr)
        cursor.execute(sql[0:len(sql) - 1])
        db.commit()


def insert_message_table(message):
    with db.cursor() as cursor:
        name = message['name']
        sessionId = message['sessionId']
        sql = "INSERT INTO message(`name`, `session_id`) VALUE(\'" + name + "\', \'" + sessionId + "\');"
        cursor.execute(sql)
    db.commit()


def insert_user_msg_table():
    with db.cursor() as cursor:
        # 获取msg_id，最后一个
        get_msg_id_sql = 'SELECT m.`id` FROM message m ORDER BY m.`id` DESC'
        cursor.execute(get_msg_id_sql)
        msg_id = cursor.fetchone()
        # 获取user_id
        get_user_id_sql = "SELECT u.`id` FROM users u WHERE u.`username` = \'" + session['username'] + "\';"
        cursor.execute(get_user_id_sql)
        user_id = cursor.fetchone()
        sql = 'INSERT INTO user_msg(user_id, message_id) VALUE(' + str(user_id[0]) + ',' + str(msg_id[0]) + ');'
        cursor.execute(sql)
    db.commit()


def get_content(sessionId):
    sql = "SELECT * FROM content c WHERE c.`session_id` = \'" + sessionId + "\'"
    return execute_sql(sql)


def update_time(session_id):
    with db.cursor() as cursor:
        sql = "UPDATE message m SET m.`time` = NOW() WHERE m.`session_id` = \'" + str(session_id) + "\'"
        print(sql)
        cursor.execute(sql)
    db.commit()


def update_msg_name_by_id(msg_id, msg_name):
    with db.cursor() as cursor:
        sql = "UPDATE message m SET m.`name` = \'" + msg_name + "\' WHERE m.id = " + msg_id
        cursor.execute(sql)
    db.commit()


def del_content_by_msg_id(msg_id):
    with db.cursor() as cursor:
        sql = "DELETE FROM content WHERE `session_id` = (SELECT `session_id` FROM message WHERE `id` = " + msg_id + ")"
        print(sql)
        cursor.execute(sql)
    db.commit()


def del_message_by_msg_id(msg_id):
    with db.cursor() as cursor:
        sql = "DELETE FROM message  WHERE `id` = " + msg_id
        cursor.execute(sql)
    db.commit()


# 删除message以及对应的content
def del_fun(msg_id):
    # 删除content
    del_content_by_msg_id(msg_id)
    # 删除message
    del_message_by_msg_id(msg_id)


def query_history():
    username = session['username']
    sql = "select * from message m where m.`id` in " \
          "( select um.`message_id` from user_msg um where um.`user_id` = " \
          "( SELECT u.`id` FROM users u WHERE u.`username` = \'" + username + "\' )) " \
                                                                              "order by m.`time` desc limit 0, 7"
    return execute_sql(sql)


def query_content_list(id):
    sql = "SELECT * FROM content WHERE `session_id` = (SELECT m.`session_id` FROM message m WHERE m.`id` = " + \
          str(id) + ")"
    return execute_sql(sql)


def get_sessionId_by_msgId(id):
    sql = "SELECT m.`session_id` FROM message m WHERE m.`id` = " + str(id)
    return execute_sql(sql)


if __name__ == '__main__':
    history_list = (query_history())
    print(str(history_list))
