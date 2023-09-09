import redis

from common.util import read_yaml


def connect_redis():
    return redis.Redis(read_yaml('database.redis.host'), port=read_yaml('database.redis.port'))


conn = connect_redis()


def exists_key(key):
    print(conn)
    return conn.exists(key)


def set_kv(k, v):
    conn.set(k, v)


def set_kv_with_expire(k, v, t):
    conn.set(k, v)
    conn.expire(k, t)


def del_k(k):
    conn.delete(k)


def get_v(k):
    return conn.get(k)


def update_v(k, v):
    conn.set(k, v)


def flush_cache(sessionId):
    message_key = sessionId + "_message"
    content_key = sessionId + "_content"
    content_num_key = sessionId + "_content_num"
    conn.delete(message_key)
    conn.delete(content_key)
    conn.delete(content_num_key)


def load_history_cache():
    return get_v("history")


def get_content_by_conversationIdx_and_sessionId(conversation_id, session_id: str):
    content_list = eval(get_v(session_id + "_content"))
    return content_list[int(conversation_id)]['content']


if __name__ == '__main__':
    conn = connect_redis()
    print(conn)
