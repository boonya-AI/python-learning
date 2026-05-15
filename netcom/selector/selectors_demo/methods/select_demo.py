"""
演示 selectors 的 select() 方法

select(timeout=None)
- 等待已注册的文件对象就绪或超时
- 返回 (key, events) 元组的列表
  - key: SelectorKey 实例
  - events: 就绪的事件位掩码
- timeout 参数:
  - timeout > 0: 最多等待 timeout 秒
  - timeout <= 0: 非阻塞，立即返回
  - timeout is None: 一直阻塞直到有事件就绪
"""

import selectors
import socket
import time
import threading


def demo_select_blocking():
    """演示阻塞式 select（timeout=None）"""
    print("=" * 50)
    print("select(timeout=None) 阻塞式等待")
    print("=" * 50)

    sel = selectors.DefaultSelector()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 0))
    server.listen(1)
    server.setblocking(False)
    port = server.getsockname()[1]

    sel.register(server, selectors.EVENT_READ, data="server")

    # 启动一个线程模拟客户端连接（1秒后连接）
    def delayed_connect():
        time.sleep(1)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', port))
        client.close()

    t = threading.Thread(target=delayed_connect)
    t.start()

    print(f"\n调用 select(timeout=None)，等待连接...")
    start = time.time()
    events = sel.select(timeout=None)  # 阻塞等待
    elapsed = time.time() - start

    print(f"等待了 {elapsed:.2f} 秒后返回")
    print(f"就绪事件数: {len(events)}")
    for key, mask in events:
        print(f"  key.data={key.data!r}, events_mask={mask}")

    t.join()
    # 接受并关闭连接
    conn, _ = server.accept()
    conn.close()

    sel.unregister(server)
    sel.close()
    server.close()
    print("资源已清理")


def demo_select_timeout():
    """演示带超时的 select"""
    print("\n" + "=" * 50)
    print("select(timeout=N) 超时等待")
    print("=" * 50)

    sel = selectors.DefaultSelector()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 0))
    server.listen(1)
    server.setblocking(False)

    sel.register(server, selectors.EVENT_READ, data="server")

    # 没有客户端连接，将超时返回
    print(f"\n调用 select(timeout=0.5)，等待0.5秒...")
    start = time.time()
    events = sel.select(timeout=0.5)
    elapsed = time.time() - start

    print(f"等待了 {elapsed:.2f} 秒后返回")
    print(f"就绪事件数: {len(events)} (超时返回空列表)")

    sel.unregister(server)
    sel.close()
    server.close()
    print("资源已清理")


def demo_select_nonblocking():
    """演示非阻塞 select（timeout=0 或负数）"""
    print("\n" + "=" * 50)
    print("select(timeout=0) 非阻塞轮询")
    print("=" * 50)

    sel = selectors.DefaultSelector()

    # 创建已连接的 socket 对
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 0))
    server.listen(1)
    port = server.getsockname()[1]

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', port))
    conn, _ = server.accept()
    conn.setblocking(False)

    # 注册连接的 socket 监听读事件
    sel.register(conn, selectors.EVENT_READ, data="connection")

    # 非阻塞轮询 - 此时没有数据可读
    print("\n1. 无数据时非阻塞轮询:")
    start = time.time()
    events = sel.select(timeout=0)
    elapsed = time.time() - start
    print(f"   耗时: {elapsed:.6f} 秒, 就绪事件数: {len(events)}")

    # 发送数据后再轮询
    client.send(b"Hello!")
    time.sleep(0.01)  # 短暂等待数据到达

    print("\n2. 有数据时非阻塞轮询:")
    start = time.time()
    events = sel.select(timeout=0)
    elapsed = time.time() - start
    print(f"   耗时: {elapsed:.6f} 秒, 就绪事件数: {len(events)}")
    for key, mask in events:
        data = key.fileobj.recv(1024)
        print(f"   收到数据: {data!r}")

    # 清理
    sel.unregister(conn)
    sel.close()
    conn.close()
    client.close()
    server.close()
    print("\n资源已清理")


def demo_select_multiple_events():
    """演示 select 返回多个就绪事件"""
    print("\n" + "=" * 50)
    print("select() 返回多个就绪事件")
    print("=" * 50)

    sel = selectors.DefaultSelector()

    # 创建服务端
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 0))
    server.listen(5)
    server.setblocking(False)
    port = server.getsockname()[1]

    sel.register(server, selectors.EVENT_READ, data="server_accept")

    # 创建多个客户端连接
    clients = []
    connections = []
    for i in range(3):
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect(('localhost', port))
        clients.append(c)

        conn, _ = server.accept()
        conn.setblocking(False)
        connections.append(conn)
        sel.register(conn, selectors.EVENT_READ, data=f"client_{i}")

    # 所有客户端同时发送数据
    for i, c in enumerate(clients):
        c.send(f"Message from client {i}".encode())

    time.sleep(0.05)  # 等待数据到达

    # select 应该返回多个就绪事件
    events = sel.select(timeout=1)
    print(f"\n有 {len(events)} 个就绪事件:")
    for key, mask in events:
        if key.data == "server_accept":
            continue
        data = key.fileobj.recv(1024)
        print(f"  {key.data}: 收到 {data!r}")

    # 清理
    for conn in connections:
        sel.unregister(conn)
        conn.close()
    sel.unregister(server)
    sel.close()
    for c in clients:
        c.close()
    server.close()
    print("\n资源已清理")


if __name__ == "__main__":
    demo_select_blocking()
    demo_select_timeout()
    demo_select_nonblocking()
    demo_select_multiple_events()
