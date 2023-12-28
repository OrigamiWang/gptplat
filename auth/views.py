# _*_ coding : utf-8 _*_
# @Time : 2023/9/9 10:26
# @Author : Origami
# @File : views
# @Project : gptplat
from common import wrappers, redis_util, exception
from auth.helpers import crud
from auth import auth_api
from flask import render_template, request, jsonify, session, current_app


@auth_api.route('/login/', methods=['GET', 'POST'])  # 登录
def login():
    """login
    @@@
    ### 用户登录接口
    @@@
    """
    try:
        if request.method == 'POST':
            req_args = request.args
            username = req_args.get('username')
            password = req_args.get('password')
            user_info = crud.query_user(username)
            if user_info is not None and user_info[2] == password:
                # 将用户名存入session以便获取,保存在client侧
                session['username'] = user_info[1]
                session['userid'] = user_info[0]
                # redis保持登录状态保持一小时
                redis_util.set_kv_with_expire(username + "_permission", user_info[3], 60 * 60)
                redis_util.set_kv_with_expire(username, username, 60 * 60)
                current_app.logger.info("userid: " + str(user_info[0]) + ", 登录了系统")
                return jsonify({
                    'status': 200,
                    'data': {
                        'userId': user_info[0],
                        'id': user_info[0],
                        'name': user_info[1],
                        'permission': user_info[3],
                    },
                })
            else:
                print("用户名或密码错误")
                return jsonify({'status': 500})
        return render_template("auth/login.html")
    except Exception:
        raise exception.ServerException("auth.login")





@auth_api.route('/current', methods=['GET'])  # 取当前登录者
def current():
    """current
    @@@
    ### 取当前用户
    @@@
    """
    try:
        return jsonify({
            'status': 200,
        })
    except Exception:
        raise exception.ServerException("auth.current")


@auth_api.route('/logout/')  # 登出
@wrappers.login_required
def logout():
    """log out
    @@@
    ### 用户退出登录
    @@@
    """
    try:
        print("logout")
        username = session['username']
        redis_util.del_k(username)
        userid = session['userid']
        current_app.logger.info("userid: " + str(userid) + ", 退出了系统")
        return jsonify({
            'status': 200
        })
    except Exception:
        raise exception.ServerException("auth.logout")

