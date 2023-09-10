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



@wrappers.login_required
@wrappers.permission_required(1)
@gpt_api.route('/session_id')
def session_id():
    """session id
    @@@
    ### 获取并保存session id
    - 将session id通过response header传回客户端并保存到浏览器
    @@@
    """
    try:
        resp = make_response()
        resp.headers['session_id'] = get_session_id()
        return resp
    except Exception:
        raise exception.ServerException("gpt.session_id")



@wrappers.login_required
@wrappers.permission_required(1)
@gpt_api.route('/loadHistory', methods=["POST", "GET"])
def load_history():
    """load history
    @@@
    ### 加载历史数据
    @@@
    """
    try:
        return load_his()
    except Exception:
        raise exception.ServerException("gpt.load_history")



@wrappers.login_required
@wrappers.permission_required(1)
@gpt_api.route("/")
@gpt_api.route("/<sessionId>", methods=["POST", "GET"])
def chatgpt(sessionId=None):
    """chat gpt
    @@@
    ### chatgpt模块核心代码
    - 访问 /
        - 返回chatgpt页面
    - 访问 /sessionId
        - 进行对话，内部调用gpt接口
    @@@
    """
    try:
        question = request.args.get("question", "")
        resp = make_response(render_template('gpt/chatpgt.html'))
        if question:
            content_arr = chatgpt_fun(sessionId, question)
            return Response(chat_stream(content_arr, sessionId), mimetype="text/event-stream")
        return resp
    except Exception:
        raise exception.ServerException("gpt.chatgpt")



@wrappers.login_required
@wrappers.permission_required(1)
@gpt_api.route('/content/<msg_id>', methods=["GET", "POST"])
def get_content_list(msg_id):
    """get content list
    @@@
    ### 通过msg_id获取一次对话的所有内容
    - msg_id
        - 某次对话的id
    - content
        - 对话内容
    @@@
    """
    try:
        session_id, content_list = get_content_list_fun(msg_id)
        return jsonify(session_id=session_id, content_list=content_list)
    except Exception:
        raise exception.ServerException("gpt.get_content_list")



@wrappers.login_required
@wrappers.permission_required(1)
@gpt_api.route('/cache/<sessionId>', methods=["POST", "GET"])
def cache_persistent(sessionId):
    """redis to mysql
    @@@
    ### 将redis的对话缓存持久化到mysql
    @@@
    """
    try:
        cache_persistent_fun(sessionId)
        return "cache"
    except Exception:
        raise exception.ServerException("gpt.cache_persistent")



@wrappers.login_required
@wrappers.permission_required(1)
@gpt_api.route('/del/<msg_id>', methods=["GET", "POST"])
def del_by_msg_id(msg_id):
    """delete msg
    @@@
    ### 删除数据库中某一次对话的记录以及内容
    @@@
    """
    try:
        del_fun(msg_id)
        return jsonify("del success!")
    except Exception:
        raise exception.ServerException("gpt.del_by_msg_id")
