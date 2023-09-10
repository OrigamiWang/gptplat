# _*_ coding : utf-8 _*_
# @Time : 2023/9/9 10:26
# @Author : Origami
# @File : views
# @Project : gptplat
from common import wrappers, mysql_util, redis_util
from auth import auth_api
from flask import render_template, request, jsonify, session, redirect, url_for


@auth_api.route('/login/', methods=['GET', 'POST'])  # 登录
def login():
    try:
        if request.method == 'POST':
            req_args = request.args
            username = req_args.get('username')
            password = req_args.get('password')
            user_info = query_user(username)
            if user_info is not None and user_info[2] == password:
                # 将用户名存入session以便获取,保存在client侧
                session['username'] = username
                # redis保持登录状态保持一小时
                # redis_util.set_kv_with_expire(username, user_info, 60 * 60)
                redis_util.set_kv_with_expire(username + "_permission", user_info[3], 60 * 60)
                redis_util.set_kv_with_expire(username, username, 60 * 60)
                return jsonify({'status': 200})
                # return redirect(url_for('admin.index'))
                # return redirect(request.args.get('next') or url_for('index'))
            else:
                print("用户名或密码错误")
                return jsonify({'status': 500})
        return render_template("auth/login.html")
    except Exception:
        raise exception.ServerException("auth.login")


def query_user(username: str):
    with mysql_util.db.cursor() as cursor:
        cursor.execute('SELECT * FROM users WHERE username=%s', (username,))
    user = cursor.fetchone()
    print(user)
    return user


@auth_api.route('/logout')  # 登出
@wrappers.login_required
def logout():
    try:
        print("logout")
        username = session['username']
        redis_util.del_k(username)
        return redirect(url_for('auth.login'))
    except Exception:
        raise exception.ServerException("auth.logout")


@auth_api.route('/pro')
@wrappers.login_required
@wrappers.permission_required(1)
def protect():
    try:
        return render_template('auth/protected.html')
    except Exception:
        raise exception.ServerException("auth.protect")


@auth_api.route('/super')
@wrappers.login_required
@wrappers.permission_required(2)
def super_permission():
    try:
        return "超级权限"
    except Exception:
        raise exception.ServerException("auth.super_permission")


@auth_api.route('/', methods=['GET'])
@wrappers.login_required
def index():
    try:
        print("index...")
        return render_template('auth/index.html')
        # return render_template('index.html', username=user_map.get('user')['username'])
    except Exception:
        raise exception.ServerException("auth.index")
