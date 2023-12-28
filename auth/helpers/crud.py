from common.mysql import mysql_util


def query_user(username: str):
    with mysql_util.db.cursor() as cursor:
        cursor.execute('SELECT * FROM users WHERE username=%s', (username,))
    user = cursor.fetchone()
    print(user)
    return user
