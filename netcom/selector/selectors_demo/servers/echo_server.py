"""
使用 DefaultSelector 实现的回声(Echo)服务器

这是 selectors 模块文档中的经典示例:
- 使用 DefaultSelector（当前平台最高效的实现）
- 非阻塞 I/O
- 基于回调的事件驱动模型
- 支持多个客户端同时连接

运行方式:
    python -m selectors_demo.servers.echo_server

然后用客户端连接:
    python -m selectors_demo.clients.echo_client
"""

import selectors
import socket
import sys

# 使用 DefaultSelector - 自动选择当前平台最高效的实现
sel = selectors.DefaultSelector()


def accept(sock, mask):
    """接受新的客户端连接"""
    conn, addr = sock.accept()
    print(f"[新连接] {addr}")
    conn.setblocking(False)
    # 注册新连接，监听读事件，回调为 read 函数
    sel.register(conn, selectors.EVENT_READ, read)


def read(conn, mask):
    """读取客户端数据并回送"""
    try:
        data = conn.recv(4096)
        if data:
            print(f"[收到] {conn.getpeername()}: {data!r}")
            conn.send(data)  # 回送数据
            print(f"[回送] {conn.getpeername()}: {data!r}")
        else:
            # 客户端关闭连接
            print(f"[断开] {conn.getpeername()}")
            sel.unregister(conn)
            conn.close()
    except ConnectionResetError:
        print(f"[断开] 连接被重置")
        sel.unregister(conn)
        conn.close()


def main(host='localhost', port=9999):
    """启动回声服务器"""
    print("=" * 50)
    print("DefaultSelector 回声服务器")
    print("=" * 50)
    print(f"\n当前使用的 Selector 类型: {type(sel).__name__}")
    print(f"(DefaultSelector 在当前平台的底层实现)")

    # 创建服务端 socket
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((host, port))
    server_sock.listen(100)
    server_sock.setblocking(False)

    # 注册服务端 socket，监听读事件（新连接到来时可读）
    sel.register(server_sock, selectors.EVENT_READ, accept)

    print(f"\n服务器启动: {host}:{port}")
    print("等待客户端连接... (Ctrl+C 退出)\n")

    try:
        while True:
            # select() 阻塞等待事件
            events = sel.select()
            for key, mask in events:
                # key.data 是注册时绑定的回调函数
                callback = key.data
                callback(key.fileobj, mask)
    except KeyboardInterrupt:
        print("\n\n服务器关闭")
    finally:
        sel.unregister(server_sock)
        sel.close()
        server_sock.close()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9999
    main(port=port)
