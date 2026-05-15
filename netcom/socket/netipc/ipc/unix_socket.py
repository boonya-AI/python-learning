"""Unix Domain Socket 实现（仅限 Unix/Linux/macOS）"""
import socket
import os
import threading
from typing import Optional, Callable


class UnixSocketServer:
    """Unix Domain Socket 服务器 - 本地进程间高效通信"""

    def __init__(self, socket_path: str = '/tmp/netipc.sock'):
        self.socket_path = socket_path
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.running = False
        self.message_callback: Optional[Callable] = None

    def start(self, callback: Optional[Callable] = None):
        """启动 Unix Socket 服务器"""
        # 删除已存在的 socket 文件
        if os.path.exists(self.socket_path):
            os.remove(self.socket_path)

        self.sock.bind(self.socket_path)
        self.sock.listen(5)
        self.running = True
        self.message_callback = callback
        print(f"Unix Socket 服务器监听: {self.socket_path}")

        try:
            while self.running:
                client_sock, client_addr = self.sock.accept()
                print(f"客户端已连接")
                thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_sock,)
                )
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            print("\n服务器关闭")
        finally:
            self.close()

    def _handle_client(self, client_sock):
        """处理客户端连接"""
        while self.running:
            try:
                data = client_sock.recv(4096)
                if not data:
                    break

                print(f"收到: {data.decode('utf-8')}")

                if self.message_callback:
                    self.message_callback(data)
                else:
                    client_sock.sendall(b"Echo: " + data)
            except (ConnectionResetError, BrokenPipeError):
                break

        client_sock.close()

    def close(self):
        """关闭服务器"""
        self.running = False
        self.sock.close()
        if os.path.exists(self.socket_path):
            os.remove(self.socket_path)


class UnixSocketClient:
    """Unix Domain Socket 客户端"""

    def __init__(self, socket_path: str = '/tmp/netipc.sock'):
        self.socket_path = socket_path
        self.sock = None

    def connect(self):
        """连接到 Unix Socket 服务器"""
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(self.socket_path)
        print(f"已连接到: {self.socket_path}")

    def send(self, message: str) -> bytes:
        """发送消息并接收响应"""
        self.sock.sendall(message.encode('utf-8'))
        response = self.sock.recv(4096)
        print(f"收到响应: {response.decode('utf-8')}")
        return response

    def close(self):
        """关闭连接"""
        if self.sock:
            self.sock.close()