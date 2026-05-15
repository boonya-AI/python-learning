"""命名管道模拟（跨平台实现）"""
import socket
import tempfile
import os
from typing import Optional


class NamedPipe:
    """
    命名管道模拟 - 使用 socket 实现跨平台管道通信
    注意：Windows 上真正的命名管道需要使用 win32pipe
    """

    def __init__(self, pipe_name: str = 'netipc_pipe'):
        self.pipe_name = pipe_name
        self.socket_path = os.path.join(tempfile.gettempdir(), f"{pipe_name}.sock")
        self.server_sock = None
        self.client_sock = None

    class PipeServer:
        """管道服务端"""

        def __init__(self, parent):
            self.parent = parent

        def start(self):
            """启动管道服务器"""
            if os.path.exists(self.parent.socket_path):
                os.remove(self.parent.socket_path)

            self.parent.server_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.parent.server_sock.bind(self.parent.socket_path)
            self.parent.server_sock.listen(1)
            print(f"命名管道服务端已启动: {self.parent.pipe_name}")

            # 等待客户端连接
            self.parent.client_sock, addr = self.parent.server_sock.accept()
            print("客户端已连接")
            return self.parent.client_sock

        def write(self, data: bytes):
            """写入数据到管道"""
            if self.parent.client_sock:
                self.parent.client_sock.sendall(data)

        def read(self, buffer_size: int = 4096) -> bytes:
            """从管道读取数据"""
            if self.parent.client_sock:
                return self.parent.client_sock.recv(buffer_size)
            return b''

        def close(self):
            """关闭服务端"""
            if self.parent.client_sock:
                self.parent.client_sock.close()
            if self.parent.server_sock:
                self.parent.server_sock.close()

    class PipeClient:
        """管道客户端"""

        def __init__(self, parent):
            self.parent = parent

        def connect(self):
            """连接到管道服务器"""
            self.parent.client_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.parent.client_sock.connect(self.parent.socket_path)
            print(f"已连接到管道: {self.parent.pipe_name}")
            return self.parent.client_sock

        def write(self, data: bytes):
            """写入数据到管道"""
            if self.parent.client_sock:
                self.parent.client_sock.sendall(data)

        def read(self, buffer_size: int = 4096) -> bytes:
            """从管道读取数据"""
            if self.parent.client_sock:
                return self.parent.client_sock.recv(buffer_size)
            return b''

        def close(self):
            """关闭客户端"""
            if self.parent.client_sock:
                self.parent.client_sock.close()

    @property
    def server(self):
        """获取服务端接口"""
        return self.PipeServer(self)

    @property
    def client(self):
        """获取客户端接口"""
        return self.PipeClient(self)