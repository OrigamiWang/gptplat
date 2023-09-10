# _*_ coding : utf-8 _*_
# @Time : 2023/9/9 16:49
# @Author : Origami
# @File : views
# @Project : gptplat


from manage import crud, manage_api
from flask import jsonify, request
from common import wrappers


@manage_api.route('/user', methods=['GET'])
@manage_api.route('/user/<user_id>', methods=['GET'])
@wrappers.login_required
@wrappers.permission_required(2)
def get_users(user_id=None):
    try:
        req_args = request.args
        pageNum = req_args.get("pageNum")
        pageSize = req_args.get("pageSize")
        if user_id is not None:
            user = crud.get_user_by_id(user_id)
            return jsonify({'user': user})
        elif pageNum is not None and pageSize is not None:
            users = crud.get_user_by_pages(pageNum, pageSize)
            return jsonify({'users': users})
        else:
            users = crud.get_all_user()
            return jsonify({'users': users})
    except Exception:
        raise exception.ServerException("manage.get_users")


@manage_api.route('/user', methods=['POST'])
@wrappers.login_required
@wrappers.permission_required(2)
def add_user():
    try:
        req_json = request.json
        crud.add_users(req_json['users'])
        return jsonify({"status": 200})
    except Exception:
        raise exception.ServerException("manage.add_user")


@manage_api.route('/user/<username>', methods=['PUT'])
@wrappers.login_required
@wrappers.permission_required(2)
def update_user(username):
    try:
        req_json = request.json
        crud.update_user(username, req_json['user'])
        return jsonify({"status": 200})
    except Exception:
        raise exception.ServerException("manage.update_users")


@manage_api.route('/user/<user_id>', methods=["DELETE"])
@wrappers.login_required
@wrappers.permission_required(2)
def delete_user(user_id):
    try:
        crud.delete_user_by_id(user_id)
        return jsonify({"status": 200})
    except Exception:
        raise exception.ServerException("manage.delete_users")
