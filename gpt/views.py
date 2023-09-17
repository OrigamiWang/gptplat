# _*_ coding : utf-8 _*_
# @Time : 2023/9/2 15:04
# @Author : Origami
# @File : views
# @Project : gptplat

from gpt import gpt_api
from flask import render_template, request, make_response, jsonify, Response, url_for, redirect
from gpt.helpers.chat import chat_stream, load_his, cache_persistent_fun, get_content_list_fun, chatgpt_fun
from common.mysql_util import del_fun
from common.util import get_session_id
from common import exception, wrappers
import gpt.helpers.voice as v


@gpt_api.route('/session_id')
@wrappers.login_required
@wrappers.permission_required(1)
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


@gpt_api.route('/loadHistory', methods=["POST", "GET"])
@wrappers.login_required
@wrappers.permission_required(1)
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


@gpt_api.route('/content/<msg_id>', methods=["GET", "POST"])
@wrappers.login_required
@wrappers.permission_required(1)
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


@gpt_api.route("/")
@gpt_api.route("/<sessionId>", methods=["POST", "GET"])
@wrappers.login_required
@wrappers.permission_required(1)
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


@gpt_api.route('/cache/<sessionId>', methods=["POST", "GET"])
@wrappers.login_required
@wrappers.permission_required(1)
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


@gpt_api.route('/del/<msg_id>', methods=["GET", "POST"])
@wrappers.login_required
@wrappers.permission_required(1)
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


@gpt_api.route('/voice/<sessionId>', methods=['GET', 'POST'])
@wrappers.login_required
@wrappers.permission_required(1)
def voice_recognition(sessionId=None):
    """voice_recognition
    @@@
    ### 语音识别
    - 注意，此接口需要起一个asrserver_http的服务才能起作用
    - 此接口的完整效果，需要前端录制wav文件，传给后端，然后转成文字。
    @@@
    """
    try:
        # get file
        # voice_file = request.files['voice_file']
        # process file
        voice_file = ''
        text_res = v.handle_voice(voice_file)
        # return redirect(url_for('gpt.chatgpt', sessionId=sessionId, question=text_res))
    except Exception:
        raise exception.ServerException("gpt.voice_recognition")
