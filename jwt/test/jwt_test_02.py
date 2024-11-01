# https://www.jianshu.com/p/03ad32c1586c

import jwt
import time
import json
import base64
import hashlib
import hmac

headers = {
    "typ": "JWT",
    "alg": "HS256"
}
salt = "asgfdgerher"
exp = time.time() + 1
payload = {
  "name": "dawsonenjoy",
  "exp": exp
}

token = jwt.encode(payload=payload, key=salt, algorithm='HS256', headers=headers).decode('utf-8')
# 实际生成
first = base64.urlsafe_b64encode(json.dumps(headers, separators=(',', ':')).encode('utf-8').replace(b'=', b'')).decode('utf-8').replace('=', '')
# 模拟第一部分生成
second = base64.urlsafe_b64encode(json.dumps(payload, separators=(',', ':')).encode('utf-8').replace(b'=', b'')).decode('utf-8').replace('=', '')
# 模拟第二部分生成
first_second = f"{first}.{second}"
# 拼接前两部分
third = base64.urlsafe_b64encode(hmac.new(salt.encode('utf-8'), first_second.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8').replace('=', '')
# 模拟第三部分生成
my_token = ".".join([first, second, third])
print(token)
print(my_token)
print(token == my_token)
# 可以看出结果是一样的

# # 结果：
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiZGF3c29uZW5qb3kiLCJleHAiOjE1Nzg1NTQxMjcuOTkwNDQ0N30.0XYnGgXXb3HrJzfoYsu-9IfqJs4GwTvf6H8uYIH78LY
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiZGF3c29uZW5qb3kiLCJleHAiOjE1Nzg1NTQxMjcuOTkwNDQ0N30.0XYnGgXXb3HrJzfoYsu-9IfqJs4GwTvf6H8uYIH78LY
# True