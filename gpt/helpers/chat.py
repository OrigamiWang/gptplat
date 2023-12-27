import openai

from common.mysql.gpt import query_history, insert_message_table, update_time, insert_content_table, \
    query_content_list, get_sessionId_by_msgId, insert_user_msg_table
from common.redis_util import get_v, update_v, set_kv, exists_key, flush_cache
from common.util import read_yaml, process_history_datetime, tuple_to_list, list_to_dict


def get_name_by_question(question):
    str_len = len(question) if len(question) < 100 else 100
    name = str(question)[0:str_len]
    return name


def chat_stream(messages, sessionId):
    openai.api_key = read_yaml('gpt.key')
    openai.api_base = read_yaml('gpt.url')
    response = openai.ChatCompletion.create(
        model=read_yaml('gpt.model'),
        messages=messages,
        temperature=0.6,
        stream=True,
    )
    sentence_list = []
    for trunk in response:
        if trunk['choices'][0]['finish_reason'] is not None:
            data = '[DONE]'
        else:
            data = trunk['choices'][0]['delta'].get('content', '')

        sentence_list.append(data)

        yield "data: %s\n\n" % data.replace("\n", "<br>")
    sentence_list.pop()
    sentence = ''.join(sentence_list).strip().replace("'", "\\'").replace("\"", "\\\"")
    content_key = str(sessionId) + "_content"
    # 插入gpt回复的内容
    content_dict = {"sessionId": sessionId, "role": 'assistant', "content": sentence}
    # 获取redis缓存的content并将此次提问加入缓存
    content_arr = list(eval(get_v(content_key)))
    content_arr.append(content_dict)
    # 更新缓存
    update_v(content_key, str(content_arr))


def load_his():
    return process_history_datetime(tuple_to_list(query_history()))


def cache_persistent_fun(sessionId, user_id):
    message_key = str(sessionId) + "_message"
    content_key = str(sessionId) + "_content"
    content_num_key = str(sessionId) + "_content_num"
    if exists_key(message_key) and get_v(content_key) is not None:
        # 将redis缓存持久化到mysql数据库
        if get_v(content_num_key) is None:
            message_tuple = eval(get_v(message_key))
            message = dict(message_tuple)
            content_arr = list(eval(get_v(content_key)))
            insert_message_table(message, user_id)
            # 插入user_msg
            insert_user_msg_table()
        else:
            # 注意，如果是通过历史记录进行的对话，一部分对话已经保存到了mysql，只需保存新产生的content，不需要添加message以及历史的content
            # 但是，需要更新message的时间
            update_time(sessionId)
            content_arr = list(eval(get_v(content_key)))[int(get_v(content_num_key)):]
        insert_content_table(content_arr)
        # 清除缓存
        flush_cache(sessionId)


def get_content_list_fun(msg_id):
    content_list = tuple_to_list(query_content_list(msg_id))
    session_id = get_sessionId_by_msgId(msg_id)[0][0]
    # 将历史记录、以及历史记录的数量缓存在redis
    content_dict = list_to_dict(content_list)
    set_kv(session_id + "_content", str(content_dict))
    set_kv(session_id + "_content_num", str(len(content_list)))
    return session_id, content_list


def chatgpt_fun(sessionId, question):
    message_key = str(sessionId) + "_message"
    content_key = str(sessionId) + "_content"
    print(exists_key(content_key))
    if not exists_key(content_key):
        # 通过查看redis缓存中是否存在这个key，来判断是否是这个会话的第一次
        # 会话记录存入数据库
        role = 'system'
        name = get_name_by_question(question)
        message_dict = {'name': name, 'sessionId': sessionId}
        # message缓存
        set_kv(message_key, str(message_dict))
        # 初始化content缓存
        set_kv(content_key, str([]))
    else:
        if not exists_key(message_key):
            set_kv(message_key, '')
        role = 'user'
    content_dict = {"sessionId": sessionId, "role": role, "content": question}
    # 获取redis缓存的content并将此次提问加入缓存
    content_arr = list(eval(get_v(content_key)))
    content_arr.append(content_dict)
    # 更新缓存
    update_v(content_key, str(content_arr))

    # 删除一些无关数据(sessionId)
    for content in content_arr:
        content.pop('sessionId')
    return content_arr
