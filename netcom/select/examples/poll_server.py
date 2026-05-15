#!/usr/bin/env python3
"""
使用 select.poll() 实现的高效服务器
poll() 比 select() 性能更好，没有文件描述符数量上限
"""

import select
import socket
import sys
from typing import Dict


class PollServer:
    """基于 poll 的单线程 TCP 服务器"""

    def __init__(self, host: str = 'localhost', port: int = 8888):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setblocking(False)

        # 创建 poll 对象
        self.poller = select.poll()
        self.fd_to_socket: Dict[int, socket.socket] = {}  # 文件描述符到 socket 的映射

        # poll 事件常量
        self.READ_ONLY = select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR
        self.READ_WRITE = self.READ_ONLY | select.POLLOUT

    def start(self):
        """启动服务器"""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        # 注册服务器 socket，关注读事件
        self.poller.register(self.server_socket, self.READ_ONLY)
        self.fd_to_socket[self.server_socket.fileno()] = self.server_socket

        print(f"Poll 服务器监听 {self.host}:{self.port}")
        print("等待客户端连接...")

        try:
            while True:
                # 等待事件发生（1000ms 超时）
                events = self.poller.poll(1000)

                for fd, event in events:
                    sock = self.fd_to_socket[fd]

                    # 处理错误或挂起事件
                    if event & (select.POLLHUP | select.POLLERR):
                        print(f"连接 {sock.getpeername()} 异常")
                        self._close_connection(sock)
                        continue

                    # 服务器 socket 的事件：新的连接
                    if sock is self.server_socket:
                        self._handle_new_connection()
                    # 客户端 socket 的事件
                    else:
                        # 可读事件
                        if event & select.POLLIN:
                            self._handle_client_read(sock)
                        # 可写事件
                        if event & select.POLLOUT:
                            self._handle_client_write(sock)

        except KeyboardInterrupt:
            print("\n服务器关闭")
        finally:
            self._cleanup()

    def _handle_new_connection(self):
        """接受新的客户端连接"""
        try:
            client_sock, client_addr = self.server_socket.accept()
            client_sock.setblocking(False)

            # 注册新客户端，只关注读事件
            self.poller.register(client_sock, self.READ_ONLY)
            self.fd_to_socket[client_sock.fileno()] = client_sock

            # 存储待发送消息的队列（简单使用属性）
            client_sock.message_queue = []

            print(f"新客户端连接: {client_addr}")
        except Exception as e:
            print(f"接受连接失败: {e}")

    def _handle_client_read(self, sock: socket.socket):
        """处理客户端数据读取"""
        try:
            data = sock.recv(1024)
            if data:
                message = data.decode('utf-8').strip()
                print(f"收到 {sock.getpeername()}: {message}")

                # 准备响应消息
                response = f"Echo: {message}".encode('utf-8')
                sock.message_queue.append(response)

                # 修改关注事件：同时关注读和写
                self.poller.modify(sock, self.READ_WRITE)
            else:
                # 客户端关闭连接
                print(f"客户端 {sock.getpeername()} 断开连接")
                self._close_connection(sock)
        except ConnectionResetError:
            print(f"客户端 {sock.getpeername()} 异常断开")
            self._close_connection(sock)

    def _handle_client_write(self, sock: socket.socket):
        """处理客户端数据发送"""
        try:
            # 发送所有待发送消息
            while sock.message_queue:
                next_msg = sock.message_queue.pop(0)
                sock.send(next_msg)

            # 消息发送完毕，改回只关注读事件
            self.poller.modify(sock, self.READ_ONLY)
        except (BrokenPipeError, ConnectionResetError):
            self._close_connection(sock)

    def _close_connection(self, sock: socket.socket):
        """关闭连接并清理资源"""
        try:
            self.poller.unregister(sock)
            del self.fd_to_socket[sock.fileno()]
            sock.close()
        except Exception as e:
            print(f"关闭连接时出错: {e}")

    def _cleanup(self):
        """清理所有资源"""
        for sock in self.fd_to_socket.values():
            try:
                self.poller.unregister(sock)
                sock.close()
            except:
                pass
        self.fd_to_socket.clear()


if __name__ == "__main__":
    server = PollServer()
    server.start()