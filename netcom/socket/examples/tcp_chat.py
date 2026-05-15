"""TCP 聊天室示例 - 多客户端聊天"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import threading
from netipc.tcp.server import TCPServer
from netipc.tcp.client import TCPClient


class ChatServer(TCPServer):
    """支持多客户端的聊天服务器"""

    def __init__(self, host='localhost', port=8888):
        super().__init__(host, port)
        self.clients = []  # 存储所有客户端连接
        self.client_addresses = []

    def _handle_client(self, client_sock, addr):
        """处理客户端消息并广播给所有人"""
        self.clients.append(client_sock)
        self.client_addresses.append(addr)
        self._broadcast(f"用户 {addr} 加入了聊天室", client_sock)

        try:
            while True:
                data = client_sock.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print(f"[{addr}] {message}")
                self._broadcast(f"[{addr}] {message}", client_sock)
        except:
            pass
        finally:
            self.clients.remove(client_sock)
            self.client_addresses.remove(addr)
            self._broadcast(f"用户 {addr} 离开了聊天室", None)
            client_sock.close()

    def _broadcast(self, message, sender_sock=None):
        """广播消息给所有客户端"""
        for client in self.clients:
            if client != sender_sock:
                try:
                    client.sendall(message.encode('utf-8'))
                except:
                    pass


def run_chat_server():
    """运行聊天服务器"""
    server = ChatServer(port=9999)
    print("=== TCP 聊天服务器已启动 ===")
    print("按 Ctrl+C 退出")
    server.start()


def run_chat_client():
    """运行聊天客户端"""
    client = TCPClient(port=9999)
    client.connect()

    print("=== 已连接到聊天室 ===")
    print("输入消息并按回车发送，输入 'quit' 退出")

    # 启动接收线程
    def receive_messages():
        while True:
            try:
                data = client.sock.recv(1024)
                if data:
                    print(f"\n{data.decode('utf-8')}")
                    print("你: ", end="", flush=True)
            except:
                break

    receive_thread = threading.Thread(target=receive_messages, daemon=True)
    receive_thread.start()

    # 发送消息
    try:
        while True:
            msg = input("你: ")
            if msg.lower() == 'quit':
                break
            client.sock.sendall(msg.encode('utf-8'))
    except:
        pass
    finally:
        client.close()


if __name__ == "__main__":
    choice = input("选择模式 (1: 服务器, 2: 客户端): ")
    if choice == '1':
        run_chat_server()
    else:
        run_chat_client()