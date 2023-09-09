# _*_ coding : utf-8 _*_
# @Time : 2023/9/2 15:04
# @Author : Origami
# @File : views
# @Project : gptplat

from gpt import gpt_api
from flask import render_template, request, make_response, jsonify, Response
from gpt.helpers.chat import chat_stream, load_his, cache_persistent_fun, get_content_list_fun, chatgpt_fun
from common.mysql_util import del_fun
from common.util import get_session_id
from common import exception, wrappers


@gpt_api.route('/session_id')
@wrappers.login_required
@wrappers.permission_required(1)
def session_id():
    try:
        resp = make_response()
        resp.headers['session_id'] = get_session_id()
        return resp
    except Exception:
        raise exception.ServerException("gpt.session_id")


@gpt_api.route('/loadHistory', methods=["POST", "GET"])
@wrappers.login_required
@wrappers.permission_required(1)
def load_history():
    try:
        return load_his()
    except Exception:
        raise exception.ServerException("gpt.load_history")


@gpt_api.route("/")
@gpt_api.route("/<sessionId>", methods=["POST", "GET"])
@wrappers.login_required
@wrappers.permission_required(1)
def chatgpt(sessionId=None):
    try:
        question = request.args.get("question", "")
        resp = make_response(render_template('gpt/chatpgt.html'))
        if question:
            content_arr = chatgpt_fun(sessionId, question)
            return Response(chat_stream(content_arr, sessionId), mimetype="text/event-stream")
        return resp
    except Exception:
        raise exception.ServerException("gpt.chatgpt")


@gpt_api.route('/content/<msg_id>', methods=["GET", "POST"])
@wrappers.login_required
@wrappers.permission_required(1)
def get_content_list(msg_id):
    try:
        session_id, content_list = get_content_list_fun(msg_id)
        return jsonify(session_id=session_id, content_list=content_list)
    except Exception:
        raise exception.ServerException("gpt.get_content_list")


@gpt_api.route('/cache/<sessionId>', methods=["POST", "GET"])
@wrappers.login_required
@wrappers.permission_required(1)
def cache_persistent(sessionId):
    try:
        cache_persistent_fun(sessionId)
        return "cache"
    except Exception:
        raise exception.ServerException("gpt.cache_persistent")


@gpt_api.route('/del/<msg_id>', methods=["GET", "POST"])
@wrappers.login_required
@wrappers.permission_required(1)
def del_by_msg_id(msg_id):
    try:
        del_fun(msg_id)
        return jsonify("del success!")
    except Exception:
        raise exception.ServerException("gpt.del_by_msg_id")
