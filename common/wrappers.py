# _*_ coding : utf-8 _*_
# @Time : 2023/9/9 10:24
# @Author : Origami
# @File : wrappers
# @Project : gptplat
from flask import session, url_for, redirect
from common import redis_util
from functools import wraps

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get('username') is not None and redis_util.exists_key(session['username']):
            return f(*args, **kwargs)
        return redirect(url_for('auth.login'))

    # wrapper.__name__ = f.__name__
    return wrapper


def permission_required(permission: int):
    def wrapper(f):
        @wraps(f)
        def inner_wrapper(*args, **kwargs):
            print("permission:", permission)
            if int(redis_util.get_v(session['username'] + "_permission")) >= permission:
                return f(*args, **kwargs)
            return "权限不够！"

        # inner_wrapper.__name__ = f.__name__
        return inner_wrapper

    return wrapper
