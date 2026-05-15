#!/usr/bin/env python3
"""
使用 select.select() 实现简单的非阻塞服务器
演示同时处理多个客户端连接
"""

import select
import socket
import sys
from typing import List


class SimpleSelectServer:
    """基于 select 的单线程 TCP 服务器"""

    def __init__(self, host: str = 'localhost', port: int = 8888):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setblocking(False)  # 设置为非阻塞模式

        self.inputs: List[socket.socket] = []  # 需要监听的读列表
        self.outputs: List[socket.socket] = []  # 需要监听的写列表
        self.message_queues = {}  # 每个客户端的待发送消息队列

    def start(self):
        """启动服务器"""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.inputs.append(self.server_socket)

        print(f"Select 服务器监听 {self.host}:{self.port}")
        print("等待客户端连接...")

        try:
            while self.inputs:
                # select() 调用：监听读、写、异常列表
                readable, writable, exceptional = select.select(
                    self.inputs, self.outputs, self.inputs
                )

                # 处理可读的 socket
                for sock in readable:
                    if sock is self.server_socket:
                        # 新的客户端连接
                        client_sock, client_addr = sock.accept()
                        client_sock.setblocking(False)
                        self.inputs.append(client_sock)
                        self.message_queues[client_sock] = []
                        print(f"新客户端连接: {client_addr}")
                    else:
                        # 已有客户端发送数据
                        self._handle_client_read(sock)

                # 处理可写的 socket
                for sock in writable:
                    self._handle_client_write(sock)

                # 处理异常 socket
                for sock in exceptional:
                    self._handle_client_exception(sock)

        except KeyboardInterrupt:
            print("\n服务器关闭")
        finally:
            self._cleanup()

    def _handle_client_read(self, sock: socket.socket):
        """处理客户端可读事件"""
        try:
            data = sock.recv(1024)
            if data:
                # 有数据，打印并准备回显
                message = data.decode('utf-8').strip()
                print(f"收到 {sock.getpeername()}: {message}")

                # 将响应加入发送队列
                response = f"Echo: {message}".encode('utf-8')
                self.message_queues[sock].append(response)

                # 如果 socket 不在 outputs 列表中，添加它以便发送
                if sock not in self.outputs:
                    self.outputs.append(sock)
            else:
                # 空数据表示客户端关闭连接
                print(f"客户端 {sock.getpeername()} 断开连接")
                self._close_connection(sock)
        except ConnectionResetError:
            print(f"客户端 {sock.getpeername()} 异常断开")
            self._close_connection(sock)

    def _handle_client_write(self, sock: socket.socket):
        """处理客户端可写事件"""
        try:
            # 从队列中取出待发送的消息
            next_msg = self.message_queues[sock].pop(0)
            if next_msg:
                sock.send(next_msg)
        except (BrokenPipeError, ConnectionResetError):
            self._close_connection(sock)

        # 如果没有更多消息要发送，从 outputs 列表中移除
        if not self.message_queues[sock]:
            self.outputs.remove(sock)

    def _handle_client_exception(self, sock: socket.socket):
        """处理异常事件"""
        print(f"客户端 {sock.getpeername()} 发生异常")
        self._close_connection(sock)

    def _close_connection(self, sock: socket.socket):
        """关闭连接并清理资源"""
        if sock in self.outputs:
            self.outputs.remove(sock)
        if sock in self.inputs:
            self.inputs.remove(sock)
        if sock in self.message_queues:
            del self.message_queues[sock]
        sock.close()

    def _cleanup(self):
        """清理所有连接"""
        for sock in self.inputs:
            sock.close()
        for sock in self.outputs:
            sock.close()
        self.inputs.clear()
        self.outputs.clear()
        self.message_queues.clear()


if __name__ == "__main__":
    server = SimpleSelectServer()
    server.start()