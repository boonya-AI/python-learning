
import time

from functools import wraps
from flask import Flask, request, jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired

app = Flask(__name__)

max_time = 60
refresh_max_time = 120
token_secret = "This is a secret"


def verify_token(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            token = request.headers["token"]
            print(token)
            s = Serializer(token_secret)
            data = s.loads(token)
            now = int(time.time())
            time_interval = now - data['time']

            if time_interval >= max_time:
                # create new token
                token, refresh_token = creat_token()
                return jsonify({"token": token, "refresh_token": refresh_token})

        except SignatureExpired:
            return "Token expired"
        except Exception as ex:
            print(ex)
            return "Log in again"

        return func(*args, **kwargs)

    return decorator


def creat_token(uid):
    now = int(time.time())
    s = Serializer(token_secret, expires_in=max_time)
    token = s.dumps({"uid": uid, "time": now}).decode("ascii")
    refresh_s = Serializer(token_secret, expires_in=refresh_max_time)
    refresh_token = refresh_s.dumps({"uid": uid, "time": now}).decode("ascii")

    return token, refresh_token


@app.route('/token', methods=["POST"])
def token():
    user_name = request.values.get('user_name')
    password = request.values.get('password')
    # @TODO 根据user_name和password 获取唯一的uid
    uid = 10
    token, refresh_token = creat_token(uid=uid)
    return jsonify({"token": token, "refresh_token": refresh_token})


@app.route('/test', methods=['GET'])
@verify_token
def test():
    return 'hello world'


if __name__ == "__main__":
    app.run(host="0.0.0.0")