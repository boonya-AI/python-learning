"""
使用 SelectSelector 实现的多客户端聊天服务器

SelectSelector 基于 select.select()，是跨平台的实现。
本示例展示:
- 显式使用 SelectSelector 而非 DefaultSelector
- 多客户端消息广播
- 非阻塞 I/O 处理

运行方式:
    python -m selectors_demo.servers.chat_server

然后用多个客户端连接:
    python -m selectors_demo.clients.chat_client
"""

import selectors
import socket
import sys

# 显式使用 SelectSelector（跨平台兼容）
sel = selectors.SelectSelector()

# 存储所有已连接的客户端
clients = {}  # {socket: address}


def accept(server_sock, mask):
    """接受新连接并广播通知"""
    conn, addr = server_sock.accept()
    conn.setblocking(False)
    clients[conn] = addr
    sel.register(conn, selectors.EVENT_READ, data="client")
    print(f"[加入] {addr}，当前在线: {len(clients)}")
    broadcast(f"[系统] {addr} 加入了聊天室\n".encode(), exclude=conn)


def read(conn, mask):
    """读取消息并广播给其他客户端"""
    try:
        data = conn.recv(4096)
        if data:
            addr = clients[conn]
            msg = f"[{addr[0]}:{addr[1]}] {data.decode().strip()}\n".encode()
            print(f"[消息] {addr}: {data.decode().strip()}")
            broadcast(msg, exclude=conn)
        else:
            disconnect(conn)
    except (ConnectionResetError, ConnectionAbortedError):
        disconnect(conn)


def broadcast(message, exclude=None):
    """向所有客户端广播消息"""
    for client_sock in list(clients.keys()):
        if client_sock != exclude:
            try:
                client_sock.send(message)
            except (BrokenPipeError, OSError):
                disconnect(client_sock)


def disconnect(conn):
    """处理客户端断开"""
    addr = clients.pop(conn, None)
    try:
        sel.unregister(conn)
    except (KeyError, ValueError):
        pass
    conn.close()
    if addr:
        print(f"[离开] {addr}，当前在线: {len(clients)}")
        broadcast(f"[系统] {addr} 离开了聊天室\n".encode())


def main(host='localhost', port=9998):
    """启动聊天服务器"""
    print("=" * 50)
    print("SelectSelector 聊天服务器")
    print("=" * 50)
    print(f"\n使用的 Selector 类型: {type(sel).__name__}")
    print(f"(基于 select.select()，跨平台兼容)")

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((host, port))
    server_sock.listen(100)
    server_sock.setblocking(False)

    sel.register(server_sock, selectors.EVENT_READ, data="server")

    print(f"\n聊天服务器启动: {host}:{port}")
    print("等待客户端连接... (Ctrl+C 退出)\n")

    try:
        while True:
            events = sel.select(timeout=1)
            for key, mask in events:
                if key.data == "server":
                    accept(key.fileobj, mask)
                else:
                    read(key.fileobj, mask)
    except KeyboardInterrupt:
        print("\n\n服务器关闭")
    finally:
        # 关闭所有客户端连接
        for client_sock in list(clients.keys()):
            disconnect(client_sock)
        sel.unregister(server_sock)
        sel.close()
        server_sock.close()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9998
    main(port=port)
