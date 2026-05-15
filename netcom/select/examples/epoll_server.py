#!/usr/bin/env python3
"""
使用 select.epoll() 实现的高性能服务器
支持边缘触发（ET）和水平触发（LT），适用于 Linux 高并发场景
注意：此示例仅适用于 Linux 系统
"""

import select
import socket
import sys
import os
from typing import Dict


class EpollServer:
    """基于 epoll 的高性能 TCP 服务器（仅 Linux）"""

    def __init__(self, host: str = 'localhost', port: int = 8888, edge_trigger: bool = False):
        self.host = host
        self.port = port
        self.edge_trigger = edge_trigger
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setblocking(False)

        # 创建 epoll 对象
        self.epoll = select.epoll()
        self.fd_to_socket: Dict[int, socket.socket] = {}

    def start(self):
        """启动 epoll 服务器"""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        # 注册服务器 socket
        events = select.EPOLLIN
        if self.edge_trigger:
            events |= select.EPOLLET  # 边缘触发模式
            print("使用边缘触发（ET）模式")
        else:
            print("使用水平触发（LT）模式")

        self.epoll.register(self.server_socket.fileno(), events)
        self.fd_to_socket[self.server_socket.fileno()] = self.server_socket

        print(f"Epoll 服务器监听 {self.host}:{self.port}")
        print("等待客户端连接...")

        try:
            while True:
                # 等待事件发生，超时 1 秒
                events = self.epoll.poll(1)

                for fd, event in events:
                    sock = self.fd_to_socket[fd]

                    # 处理错误事件
                    if event & (select.EPOLLERR | select.EPOLLHUP):
                        print(f"连接错误或挂起: {fd}")
                        self._close_connection(fd)
                        continue

                    # 新连接事件
                    if sock is self.server_socket:
                        self._handle_new_connection()
                    # 客户端数据事件
                    else:
                        # 可读事件
                        if event & select.EPOLLIN:
                            self._handle_client_read(fd)
                        # 可写事件（在边缘触发模式下需要注意）
                        if event & select.EPOLLOUT:
                            self._handle_client_write(fd)

        except KeyboardInterrupt:
            print("\n服务器关闭")
        finally:
            self._cleanup()

    def _handle_new_connection(self):
        """接受新连接"""
        try:
            while True:
                # 对于边缘触发，需要循环 accept 直到返回 EAGAIN
                client_sock, client_addr = self.server_socket.accept()
                client_sock.setblocking(False)

                # 为客户端存储待发送消息队列
                client_sock.message_queue = []

                # 注册客户端 socket
                events = select.EPOLLIN | select.EPOLLOUT if self.edge_trigger else select.EPOLLIN
                if self.edge_trigger:
                    events |= select.EPOLLET

                self.epoll.register(client_sock.fileno(), events)
                self.fd_to_socket[client_sock.fileno()] = client_sock

                print(f"新客户端连接: {client_addr}")
        except BlockingIOError:
            # 边缘触发模式下，所有连接已处理完
            pass
        except Exception as e:
            print(f"接受连接错误: {e}")

    def _handle_client_read(self, fd: int):
        """处理客户端数据读取"""
        sock = self.fd_to_socket[fd]

        try:
            if self.edge_trigger:
                # 边缘触发模式：需要循环读取直到 EAGAIN
                while True:
                    data = sock.recv(1024)
                    if not data:
                        # 连接关闭
                        print(f"客户端 {sock.getpeername()} 断开连接")
                        self._close_connection(fd)
                        return

                    message = data.decode('utf-8').strip()
                    print(f"收到 {sock.getpeername()}: {message}")

                    response = f"Echo: {message}".encode('utf-8')
                    sock.message_queue.append(response)
            else:
                # 水平触发模式：普通读取
                data = sock.recv(1024)
                if data:
                    message = data.decode('utf-8').strip()
                    print(f"收到 {sock.getpeername()}: {message}")
                    response = f"Echo: {message}".encode('utf-8')
                    sock.message_queue.append(response)
                else:
                    print(f"客户端 {sock.getpeername()} 断开连接")
                    self._close_connection(fd)

        except BlockingIOError:
            # 边缘触发下数据已读完
            pass
        except (ConnectionResetError, BrokenPipeError):
            print(f"客户端 {self.fd_to_socket[fd].getpeername()} 异常断开")
            self._close_connection(fd)

    def _handle_client_write(self, fd: int):
        """处理客户端数据发送"""
        sock = self.fd_to_socket[fd]

        try:
            # 发送所有待发送消息
            while sock.message_queue:
                next_msg = sock.message_queue.pop(0)
                sent = sock.send(next_msg)

                # 边缘触发下可能一次发送不完
                if sent < len(next_msg) and self.edge_trigger:
                    # 剩余数据放回队列
                    remaining = next_msg[sent:]
                    sock.message_queue.insert(0, remaining)
                    # 仍然关注 EPOLLOUT 事件
                    return

            # 所有消息发送完毕
            if self.edge_trigger:
                # 边缘触发模式下保持同时关注读写
                pass
        except (BrokenPipeError, ConnectionResetError):
            self._close_connection(fd)

    def _close_connection(self, fd: int):
        """关闭连接"""
        try:
            self.epoll.unregister(fd)
            sock = self.fd_to_socket[fd]
            del self.fd_to_socket[fd]
            sock.close()
        except:
            pass

    def _cleanup(self):
        """清理资源"""
        self.epoll.close()
        for sock in self.fd_to_socket.values():
            sock.close()
        self.server_socket.close()


if __name__ == "__main__":
    # 检测是否在 Linux 系统
    if not hasattr(select, 'epoll'):
        print("错误：epoll 仅支持 Linux 系统")
        sys.exit(1)

    use_edge = input("使用边缘触发模式？(y/n, 默认 n): ").lower() == 'y'
    server = EpollServer(edge_trigger=use_edge)
    server.start()