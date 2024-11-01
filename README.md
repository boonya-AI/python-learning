
### Python 丰富的学习资源

https://wiki.python.org/moin/BeginnersGuide/Programmers

### Python pip 安装模块

`pip install {yor_required_lib_name}`


### Python packages 

- <some folder present in the sys.path>/
    - world/
        - __init__.py
        - asia/
            - __init__.py
            - india/
                - __init__.py
                - foo.py
        - africa/
            - __init__.py
            - madagascar/
                - __init__.py
                - bar.py

### Git token 登录和克隆代码问题

#### github token

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  2024-08-20


#### 不出登录框 ，删除windows凭据

https://blog.csdn.net/weixin_45606415/article/details/115473297

git config --system --unset credential.helper


####  unable to access  OpenSSL SSL_read: Connection was reset, errno 10054


git config --global http.sslVerify "false"

### venv 虚拟环境添加

1. PyCharm IDE 右上角 找到设置
2. 找到Settings 
3. 找到Project: python-learning 
4. Add Interpreter 即可

### Python 换源

#### 临时换源

###### 清华源
pip install markdown -i https://pypi.tuna.tsinghua.edu.cn/simple
###### 阿里源
pip install markdown -i https://mirrors.aliyun.com/pypi/simple/
###### 腾讯源
pip install markdown -i http://mirrors.cloud.tencent.com/pypi/simple
###### 豆瓣源
pip install markdown -i http://pypi.douban.com/simple/


#### 永久换源

###### 清华源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
###### 阿里源
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
###### 腾讯源
pip config set global.index-url http://mirrors.cloud.tencent.com/pypi/simple
###### 豆瓣源
pip config set global.index-url http://pypi.douban.com/simple/
###### 换回默认源
pip config unset global.index-url


# VS代码提示

https://zhuanlan.zhihu.com/p/112431369


## 写代码语法提示
pip install flake8 

## 自动格式化代码
pip install yapf

