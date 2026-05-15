#!/usr/bin/env python3
"""
通用的 TCP 客户端，用于测试 select 服务器
可以同时建立多个连接进行并发测试
"""

import socket
import threading
import time
from typing import List


class EchoClient:
    """简单的 TCP 客户端"""

    def __init__(self, host: str = 'localhost', port: int = 8888):
        self.host = host
        self.port = port
        self.sock = None
        self.running = False

    def connect(self) -> bool:
        """连接到服务器"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            print(f"已连接到 {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"连接失败: {e}")
            return False

    def send_and_receive(self, message: str) -> str:
        """发送消息并接收响应"""
        try:
            self.sock.sendall(message.encode('utf-8'))
            response = self.sock.recv(1024)
            return response.decode('utf-8')
        except Exception as e:
            print(f"通信错误: {e}")
            return ""

    def interactive_mode(self):
        """交互式模式"""
        if not self.connect():
            return

        print("输入消息发送 (输入 'quit' 退出)")
        try:
            while True:
                msg = input("你: ")
                if msg.lower() == 'quit':
                    break
                response = self.send_and_receive(msg)
                if response:
                    print(f"服务器: {response}")
        finally:
            self.close()

    def close(self):
        """关闭连接"""
        if self.sock:
            self.sock.close()


class MultiClientTest:
    """多客户端并发测试"""

    @staticmethod
    def run_test(host: str = 'localhost', port: int = 8888,
                 num_clients: int = 5, messages: List[str] = None):
        """同时运行多个客户端进行测试"""
        if messages is None:
            messages = ["Hello", "World", "Test", "Multi", "Client"]

        def client_worker(client_id: int, message: str):
            client = EchoClient(host, port)
            if client.connect():
                response = client.send_and_receive(message)
                print(f"客户端 {client_id}: '{message}' -> '{response}'")
                client.close()

        threads = []
        for i in range(min(num_clients, len(messages))):
            t = threading.Thread(target=client_worker, args=(i, messages[i % len(messages)]))
            threads.append(t)
            t.start()
            time.sleep(0.1)  # 稍微间隔，避免同时连接

        for t in threads:
            t.join()

        print("多客户端测试完成")


if __name__ == "__main__":
    print("=== Echo 客户端测试 ===")
    print("1. 单客户端交互模式")
    print("2. 多客户端并发测试")

    choice = input("请选择 (1-2): ")

    if choice == '1':
        client = EchoClient()
        client.interactive_mode()
    elif choice == '2':
        num = int(input("客户端数量 (默认5): ") or "5")
        MultiClientTest.run_test(num_clients=num)
    else:
        print("无效选择")