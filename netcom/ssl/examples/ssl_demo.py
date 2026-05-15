#!/usr/bin/env python3
"""
SSL/TLS 加密通信完整演示
演示服务端和客户端之间的安全通信
"""

import sys
import os
import threading
import time

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ssl.ssl_wrapper.ssl_server import SSLServer
from ssl.ssl_wrapper.ssl_client import SSLClient
from ssl.ssl_wrapper.cert_utils import generate_self_signed_cert


def run_ssl_server():
    """运行 SSL 服务器"""
    # 确保证书存在
    cert_dir = os.path.join(os.path.dirname(__file__), '..', 'certs')
    cert_path = os.path.join(cert_dir, 'server.crt')
    key_path = os.path.join(cert_dir, 'server.key')

    if not (os.path.exists(cert_path) and os.path.exists(key_path)):
        print("未找到证书，正在生成自签名证书...")
        generate_self_signed_cert(cert_dir)

    server = SSLServer(port=8443, cert_path=cert_path, key_path=key_path)
    print("=== SSL 加密服务器启动 ===")
    print("等待客户端连接...")
    server.start()


def run_ssl_client():
    """运行 SSL 客户端"""
    cert_dir = os.path.join(os.path.dirname(__file__), '..', 'certs')
    cert_path = os.path.join(cert_dir, 'server.crt')

    client = SSLClient(port=8443, ca_cert_path=cert_path)

    if client.connect():
        # 发送测试消息
        client.send("Hello, SSL Server!")
        client.close()
    else:
        print("SSL 连接失败")


def run_interactive_chat():
    """交互式加密聊天演示（需要同时运行服务端和客户端）"""
    mode = input("选择模式 (1: 服务器, 2: 客户端): ")

    cert_dir = os.path.join(os.path.dirname(__file__), '..', 'certs')
    cert_path = os.path.join(cert_dir, 'server.crt')
    key_path = os.path.join(cert_dir, 'server.key')

    if mode == '1':
        # 服务器模式
        if not (os.path.exists(cert_path) and os.path.exists(key_path)):
            generate_self_signed_cert(cert_dir)

        def on_message(message, addr, sock):
            print(f"收到来自 {addr} 的消息: {message}")
            # 可以在这里添加自定义响应逻辑

        server = SSLServer(port=8443, cert_path=cert_path, key_path=key_path)
        server.message_callback = on_message
        print("加密聊天服务器启动，等待连接...")
        server.start()

    elif mode == '2':
        # 客户端模式
        client = SSLClient(port=8443, ca_cert_path=cert_path)
        if client.connect():
            print("连接成功！输入消息发送（输入 'quit' 退出）")
            try:
                while True:
                    msg = input("你: ")
                    if msg.lower() == 'quit':
                        break
                    client.send(msg)
            except KeyboardInterrupt:
                pass
            finally:
                client.close()
    else:
        print("无效选择")


if __name__ == "__main__":
    print("=== SSL/TLS 加密通信演示 ===")
    print("1. 基础连接演示")
    print("2. 交互式加密聊天")
    print("3. 仅启动服务器")
    print("4. 仅启动客户端")

    choice = input("请选择 (1-4): ")

    if choice == '1':
        # 自动运行服务器和客户端演示
        print("启动服务器...")
        server_thread = threading.Thread(target=run_ssl_server, daemon=True)
        server_thread.start()
        time.sleep(1)
        print("\n启动客户端...")
        run_ssl_client()
        time.sleep(2)
        print("\n演示完成")
    elif choice == '2':
        run_interactive_chat()
    elif choice == '3':
        run_ssl_server()
    elif choice == '4':
        run_ssl_client()
    else:
        print("无效选择")