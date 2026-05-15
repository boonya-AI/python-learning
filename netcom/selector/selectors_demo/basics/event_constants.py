"""
演示 selectors 模块的事件常量: EVENT_READ 和 EVENT_WRITE

EVENT_READ - 表示可读事件（值为1）
EVENT_WRITE - 表示可写事件（值为2）
这两个常量可以通过位运算组合使用
"""

import selectors
import socket


def demo_event_constants():
    """演示事件常量的值和位运算"""
    print("=" * 50)
    print("selectors 事件常量演示")
    print("=" * 50)

    # 查看常量值
    print(f"\nEVENT_READ  = {selectors.EVENT_READ} (二进制: {bin(selectors.EVENT_READ)})")
    print(f"EVENT_WRITE = {selectors.EVENT_WRITE} (二进制: {bin(selectors.EVENT_WRITE)})")

    # 位运算组合：同时监听读和写
    both = selectors.EVENT_READ | selectors.EVENT_WRITE
    print(f"\nEVENT_READ | EVENT_WRITE = {both} (二进制: {bin(both)})")

    # 判断事件中是否包含读/写
    print(f"\n检测事件掩码中是否包含读事件: {bool(both & selectors.EVENT_READ)}")
    print(f"检测事件掩码中是否包含写事件: {bool(both & selectors.EVENT_WRITE)}")


def demo_event_with_socket():
    """演示在实际 socket 中使用事件常量"""
    print("\n" + "=" * 50)
    print("在 socket 中使用事件常量")
    print("=" * 50)

    sel = selectors.DefaultSelector()

    # 创建一对连接的 socket 用于演示
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('localhost', 0))  # 绑定到随机可用端口
    server_sock.listen(1)
    port = server_sock.getsockname()[1]
    print(f"\n服务端监听端口: {port}")

    # 注册服务端 socket 监听读事件（有新连接时可读）
    sel.register(server_sock, selectors.EVENT_READ, data="server")
    print(f"已注册服务端 socket，监听事件: EVENT_READ ({selectors.EVENT_READ})")

    # 创建客户端连接
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('localhost', port))

    # 注册客户端 socket 监听写事件（连接建立后可写）
    sel.register(client_sock, selectors.EVENT_WRITE, data="client_write")
    print(f"已注册客户端 socket，监听事件: EVENT_WRITE ({selectors.EVENT_WRITE})")

    # 执行一次非阻塞 select
    events = sel.select(timeout=1)
    print(f"\nselect() 返回了 {len(events)} 个就绪事件:")
    for key, mask in events:
        event_names = []
        if mask & selectors.EVENT_READ:
            event_names.append("EVENT_READ")
        if mask & selectors.EVENT_WRITE:
            event_names.append("EVENT_WRITE")
        print(f"  文件对象: {key.data}, 就绪事件: {' | '.join(event_names)} (mask={mask})")

    # 清理
    sel.unregister(server_sock)
    sel.unregister(client_sock)
    sel.close()
    client_sock.close()
    server_sock.close()
    print("\n资源已清理")


if __name__ == "__main__":
    demo_event_constants()
    demo_event_with_socket()
