import traceback

from auth import auth_api
from gpt import gpt_api
from manage import manage_api
from flask import Flask, redirect, url_for, request
from common import exception, mysql_util

app = Flask(__name__, template_folder='templates')
# 设置密钥用于session
app.secret_key = 'ba3a1d17a1a6e9c4cbe3fbe2e6b7ca99a5b0983fe566a1dad8c3ad450d4bf1a1'
# 模块化
app.register_blueprint(gpt_api, url_prefix='/gpt')
app.register_blueprint(auth_api, url_prefix='/auth')
app.register_blueprint(manage_api, url_prefix='/manage')

with app.app_context():
    db = mysql_util.get_db()


@app.errorhandler(exception.ServerException)
def handle_server_exception(e):
    traceback.print_exc()
    return exception.ServerException.handler_err(e, e)


@app.errorhandler(exception.FileParseException)
def handle_file_parse_exception(e):
    traceback.print_exc()
    return exception.FileParseException.handler_err(e, e)


@app.errorhandler(404)
def catch_404_err(e):
    url = request.url
    return exception.PageNotFoundException.handler_err(e, e, url)


@app.route('/')
def redirect2gpt():
    try:
        return redirect(url_for('gpt.chatgpt'))
    except Exception:
        raise exception.ServerException("app.redirect2gpt")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
