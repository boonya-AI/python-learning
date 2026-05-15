#!/usr/bin/env python3
"""
使用 select 实现的多客户端聊天室服务器
展示广播消息、私聊等高级功能
"""

import select
import socket
import sys
from typing import Dict, Set


class ChatRoomServer:
    """基于 select 的聊天室服务器"""

    def __init__(self, host: str = 'localhost', port: int = 8888):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setblocking(False)

        self.inputs: Set[socket.socket] = set()
        self.outputs: Set[socket.socket] = set()
        self.client_names: Dict[socket.socket, str] = {}  # 用户名映射

    def start(self):
        """启动聊天室服务器"""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.inputs.add(self.server_socket)

        print(f"聊天室服务器启动在 {self.host}:{self.port}")
        print("等待用户连接...")

        try:
            while self.inputs:
                readable, writable, exceptional = select.select(
                    self.inputs, self.outputs, self.inputs
                )

                # 处理可读事件
                for sock in readable:
                    if sock is self.server_socket:
                        self._accept_new_client()
                    else:
                        self._handle_client_message(sock)

                # 处理可写事件
                for sock in writable:
                    self._send_queued_messages(sock)

                # 处理异常连接
                for sock in exceptional:
                    self._disconnect_client(sock, "连接异常")

        except KeyboardInterrupt:
            print("\n服务器关闭")
        finally:
            self._cleanup()

    def _accept_new_client(self):
        """接受新客户端连接"""
        try:
            client_sock, client_addr = self.server_socket.accept()
            client_sock.setblocking(False)

            self.inputs.add(client_sock)
            self.client_names[client_sock] = f"用户{client_addr[1]}"  # 临时名称

            # 发送欢迎消息
            welcome = f"欢迎加入聊天室！当前在线人数: {len(self.inputs) - 1}\n"
            client_sock.send(welcome.encode('utf-8'))

            # 广播新用户加入
            self._broadcast(f"【系统】{self.client_names[client_sock]} 加入聊天室\n", client_sock)

            print(f"新连接: {client_addr} -> {self.client_names[client_sock]}")

        except Exception as e:
            print(f"接受连接失败: {e}")

    def _handle_client_message(self, client_sock: socket.socket):
        """处理客户端消息"""
        try:
            data = client_sock.recv(1024)
            if data:
                message = data.decode('utf-8').strip()

                # 处理特殊命令
                if message.startswith('/'):
                    self._handle_command(client_sock, message)
                else:
                    # 普通消息广播
                    sender = self.client_names.get(client_sock, "匿名")
                    self._broadcast(f"[{sender}]: {message}\n", client_sock)
            else:
                # 客户端主动断开
                self._disconnect_client(client_sock, "客户端主动断开")

        except ConnectionResetError:
            self._disconnect_client(client_sock, "连接重置")
        except Exception as e:
            print(f"处理消息错误: {e}")
            self._disconnect_client(client_sock, f"错误: {e}")

    def _handle_command(self, client_sock: socket.socket, command: str):
        """处理客户端命令"""
        parts = command.split(' ', 2)
        cmd = parts[0].lower()

        if cmd == '/nick' and len(parts) >= 2:
            # 修改昵称
            new_name = parts[1]
            old_name = self.client_names[client_sock]
            self.client_names[client_sock] = new_name
            self._broadcast(f"【系统】{old_name} 改名为 {new_name}\n")
            client_sock.send(f"昵称已更改为 {new_name}\n".encode('utf-8'))

        elif cmd == '/quit' or cmd == '/exit':
            self._disconnect_client(client_sock, "用户主动退出")

        elif cmd == '/users':
            # 列出所有用户
            users = [name for name in self.client_names.values()]
            user_list = f"当前在线 ({len(users)}人): {', '.join(users)}\n"
            client_sock.send(user_list.encode('utf-8'))

        elif cmd == '/help':
            help_text = """
            可用命令:
            /nick <新昵称> - 修改昵称
            /users - 查看在线用户
            /quit - 退出聊天室
            /help - 显示帮助
            """
            client_sock.send(help_text.encode('utf-8'))
        else:
            client_sock.send(f"未知命令: {cmd}\n".encode('utf-8'))

    def _send_queued_messages(self, sock: socket.socket):
        """发送队列中的消息（简化实现，实际应用中需要消息队列）"""
        # 此示例中直接发送，实际可能需要队列管理
        pass

    def _broadcast(self, message: str, sender_sock: socket.socket = None):
        """广播消息给所有客户端"""
        dead_sockets = set()

        for sock in self.inputs:
            if sock is not self.server_socket and sock is not sender_sock:
                try:
                    sock.send(message.encode('utf-8'))
                except (BrokenPipeError, ConnectionResetError):
                    dead_sockets.add(sock)

        # 清理断开的连接
        for sock in dead_sockets:
            self._disconnect_client(sock, "发送消息失败")

    def _disconnect_client(self, client_sock: socket.socket, reason: str = ""):
        """断开客户端连接"""
        if client_sock in self.inputs:
            self.inputs.remove(client_sock)

        if client_sock in self.outputs:
            self.outputs.remove(client_sock)

        name = self.client_names.get(client_sock, "未知用户")
        print(f"断开连接: {name} ({reason})")

        # 广播离开消息
        if reason and reason != "客户端主动断开":
            self._broadcast(f"【系统】{name} 已离开 ({reason})\n")
        elif reason != "客户端主动断开":
            self._broadcast(f"【系统】{name} 已离开聊天室\n")

        if client_sock in self.client_names:
            del self.client_names[client_sock]

        try:
            client_sock.close()
        except:
            pass

    def _cleanup(self):
        """清理所有资源"""
        for sock in self.inputs:
            try:
                sock.close()
            except:
                pass
        self.inputs.clear()
        self.outputs.clear()
        self.client_names.clear()
        print("服务器已关闭")


if __name__ == "__main__":
    server = ChatRoomServer()
    server.start()