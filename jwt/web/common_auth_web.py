# 基于传统token实现用户校验
from flask import Flask, request
import json
import uuid

app = Flask(__name__)

# 这里用全局字典模拟数据库：
# user_table表里存放用户名、密码用于用户登录校验
# user_token表里存放token，用于token校验
# user_info_table存放用户信息
db_source = {
    'user_table': {
        'dawsonenjoy': {
            'pwd': '111111'
        }
    }, 
    'user_token': {},
    'user_info_table': {
        'dawsonenjoy': {
            'age': 18
        }
    }
}

@app.route('/login', methods=['POST'])
def login():
    '''用户登录，用户名密码验证成功将会生成对应token，并将token保存以及返回给用户'''
    username = request.form.get('username', None)
    pwd = request.form.get('password', None)
    if (not username) or (not pwd):
        return json.dumps({'status': 1, 'code': '400', 'msg': '用户或密码不允许为空！'}, ensure_ascii=False)
    if not db_source['user_table'].get(username, None):
        return json.dumps({'status': 1, 'code': '401', 'msg': '用户不存在！'}, ensure_ascii=False)
    if db_source['user_table'][username]['pwd'] != pwd:
        return json.dumps({'status': 1, 'code': '402', 'msg': '用户名或密码错误！'}, ensure_ascii=False)
    # 当登录校验通过，则为用户存入token，并返回token
    token = str(uuid.uuid4())
    db_source['user_token'][token] = username
    return json.dumps({'status': 1, 'code': '200', 'data': {'token': token}})

@app.route('/user_info', methods=['GET'])
def user_info():
    '''查看用户信息，需要和本地保存的token进行校验'''
    token = request.args.get('token', None)
    if not token:
        return json.dumps({'status': 1, 'code': '500', 'msg': 'token不允许为空！'}, ensure_ascii=False)
    if not db_source['user_token'].get(token, None):
        return json.dumps({'status': 1, 'code': '501', 'msg': 'token校验失败！'}, ensure_ascii=False)
    # 当token校验成功则返回用户信息
    username = db_source['user_token'][token]
    info = db_source['user_info_table'][username]
    return json.dumps({'status': 1, 'code': '200', 'data': {username: info}})

if __name__ == '__main__':
    app.run(debug=True, port=5000)