# _*_ coding : utf-8 _*_
# @Time : 2023/9/2 15:04
# @Author : Origami
# @File : views
# @Project : gptplat

from gpt import gpt_api
from flask import render_template, request, make_response, jsonify, Response, url_for, redirect
from gpt.helpers.chat import chat_stream, load_his, cache_persistent_fun, get_content_list_fun, chatgpt_fun
from gpt.helpers.customize_role import get_role_sentence, get_role_list, add_new_role
from gpt.helpers.star import get_star_list_by_id, update_star_name_by_name, create_star_by_id, delete_user_by_id
from common.mysql.gpt import del_fun
from common.util import get_session_id
from common import exception, wrappers
import gpt.helpers.voice as v
import common.status as status
import uuid


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


@gpt_api.route('/cache/<sessionId>/<user_id>', methods=["POST", "GET"])
@wrappers.login_required
@wrappers.permission_required(1)
def cache_persistent(sessionId, user_id):
    """redis to mysql
    @@@
    ### 将redis的对话缓存持久化到mysql
    @@@
    """
    try:
        cache_persistent_fun(sessionId, user_id)
        return "cache"
    except Exception:
        raise exception.ServerException("gpt.cache_persistent")


@gpt_api.route('/del/<msg_id>/<user_id>', methods=["GET", "POST"])
@wrappers.login_required
@wrappers.permission_required(1)
def del_by_msg_id(msg_id, user_id):
    """delete msg
    @@@
    ### 删除数据库中某一次对话的记录以及内容
    @@@
    """
    try:
        del_fun(user_id, msg_id)
        return jsonify("del success!")
    except Exception:
        raise exception.ServerException("gpt.del_by_msg_id")


@gpt_api.route('/voice/<sessionId>', methods=['POST'])
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
        voice_file = request.files.get('voice_file')
        file_path = str(uuid.uuid1()) + ".wav"
        voice_file.save(file_path)
        # process file
        text_res = v.handle_voice(file_path)
        return redirect(url_for('gpt.chatgpt', sessionId=sessionId, question=text_res))
    except Exception:
        raise exception.ServerException("gpt.voice_recognition")


@gpt_api.route('/role/<id>', methods=['GET'])
def choose_role(id):
    """choose_role
    @@@
    ### 选择角色进行对话
    @@@
    """
    sessionId = request.args.get("sessionId")
    print(sessionId)
    role_sentence = get_role_sentence(id)
    return redirect(url_for('gpt.chatgpt', sessionId=sessionId, question=role_sentence))


@gpt_api.route('/role/', methods=['GET'])
def get_all_role():
    """get_all_role
    @@@
    ### 获取角色列表（包括角色名和角色prompt）
    @@@
    """
    role_list = get_role_list()
    return jsonify(role_list)


@gpt_api.route('/role/', methods=['POST'])
def add_one_role():
    """add_a_role
    @@@
    ### 添加角色
    - 使用json添加
    ```json
    {
        "name": "Doctor",
        "sentence": "save the people"
    }
    ```
    @@@
    """
    json_str = request.get_json()
    add_new_role(json_str['name'], json_str['sentence'])
    return "add role successful!"


@gpt_api.route('/star/<user_id>', methods=['GET'])
# @wrappers.login_required
# @wrappers.permission_required(1)
def get_star_list(user_id):
    """get star list
    @@@
    ### 获取用户的收藏夹列表
    @@@
    """
    try:
        star_list = get_star_list_by_id(user_id)
        return jsonify(status=status.HTTP_OK, msg="success", data=star_list)
    except Exception:
        raise exception.ServerException("gpt.get_star_list")


@gpt_api.route('/star/<user_id>', methods=['PUT'])
# @wrappers.login_required
# @wrappers.permission_required(1)
def update_star(user_id):
    """update star
    @@@
    ### 判断并更新收藏夹名字
    @@@
    """
    try:
        new_name = request.args.get("newName")
        old_name = request.args.get("oldName")
        if new_name is None or old_name is None:
            return jsonify(status=status.HTTP_ARGS_ERR, msg="参数异常")
        update_star_name_by_name(user_id, old_name, new_name)
        return jsonify(status=status.HTTP_OK, msg="success")
    except Exception:
        raise exception.ServerException("gpt.get_star_list")


@gpt_api.route('/star/<user_id>', methods=['DELETE'])
@wrappers.login_required
@wrappers.permission_required(1)
def delete_star(user_id):
    """delete star
    @@@
    ### 删除收藏夹
    @@@
    """
    name = request.args.get("name")
    if name is None:
        return jsonify(status=status.HTTP_ARGS_ERR, msg="参数异常")
    delete_user_by_id(user_id, name)
    return jsonify(status=status.HTTP_OK, msg="success")


@gpt_api.route('/star/<user_id>', methods=['POST'])
@wrappers.login_required
@wrappers.permission_required(1)
def add_star(user_id):
    """add star
    @@@
    ### 新建收藏夹
    @@@
    """
    name = request.args.get("name")
    if name is None:
        return jsonify(status=status.HTTP_ARGS_ERR, msg="参数异常")
    create_star_by_id(user_id, name)
    return jsonify(status=status.HTTP_OK, msg="success")
