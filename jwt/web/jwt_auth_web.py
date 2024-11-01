# 基于jwt实现的用户校验
from flask import Flask, request
import jwt
from jwt import exceptions
import json
import time

app = Flask(__name__)

# 这里用全局字典模拟数据库：
# user_table表里存放用户名、密码用于用户登录校验
# 因为jwt校验无需在服务端存储，所以user_token表也就不需要
# user_info_table存放用户信息
db_source = {
    'user_table': {
        'dawsonenjoy': {
            'pwd': '111111'
        }
    }, 
    'user_info_table': {
        'dawsonenjoy': {
            'age': 18
        }
    }
}

SECRET_KEY = "asgfddasdasdasgerher"
# 定义签名密钥，用于校验jwt的有效、合法性

def create_token(name):
    '''基于jwt创建token的函数'''
    global SECRET_KEY
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    exp = int(time.time() + 20)
    payload = {
        "name": name,
        "exp": exp
    }
    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm='HS256', headers=headers).decode('utf-8')
    # 返回生成的token
    return token

def validate_token(token):
    '''校验token的函数，校验通过则返回解码信息'''
    global SECRET_KEY
    payload = None
    msg = None
    try:
        payload = jwt.decode(token, SECRET_KEY, True, algorithm='HS256')
        # jwt有效、合法性校验
    except exceptions.ExpiredSignatureError:
        msg = 'token已失效'
    except jwt.DecodeError:
        msg = 'token认证失败'
    except jwt.InvalidTokenError:
        msg = '非法的token'
    return (payload, msg)

@app.route('/login', methods=['POST'])
def login():
    '''用户登录，用户名密码验证成功将会生成对应token，但不需要在本地保存，直接返回给用户'''
    username = request.form.get('username', None)
    pwd = request.form.get('password', None)
    if (not username) or (not pwd):
        return json.dumps({'status': 1, 'code': '400', 'msg': '用户或密码不允许为空！'}, ensure_ascii=False)
    if not db_source['user_table'].get(username, None):
        return json.dumps({'status': 1, 'code': '401', 'msg': '用户不存在！'}, ensure_ascii=False)
    if db_source['user_table'][username]['pwd'] != pwd:
        return json.dumps({'status': 1, 'code': '402', 'msg': '用户名或密码错误！'}, ensure_ascii=False)
    # 当登录校验通过，则为用户创建并返回token
    token = create_token(username)
    # 注意这里不存入本地了
    return json.dumps({'status': 1, 'code': '200', 'data': {'token': token}})

@app.route('/user_info', methods=['GET'])
def user_info():
    '''查看用户信息，需要token校验'''
    token = request.args.get('token', None)
    if not token:
        return json.dumps({'status': 1, 'code': '500', 'msg': 'token不允许为空！'}, ensure_ascii=False)
    payload, msg = validate_token(token)
    # 直接对token进行合法性校验
    if msg:
        return json.dumps({'status': 1, 'code': '500', 'msg': msg}, ensure_ascii=False)
    username = payload['name']
    info = db_source['user_info_table'][username]
    return json.dumps({'status': 1, 'code': '200', 'data': {username: info}})

if __name__ == '__main__':
    app.run(debug=True, port=5000)