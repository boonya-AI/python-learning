"""
演示 selectors 的 register() 方法

register(fileobj, events, data=None)
- 注册一个文件对象以监控 I/O 事件
- 返回一个 SelectorKey 实例
- events 是 EVENT_READ 和/或 EVENT_WRITE 的位掩码组合
- data 是可选的用户数据（如回调函数）
- 如果 fileobj 已注册会抛出 KeyError
- 如果 fileobj 无效会抛出 ValueError
"""

import selectors
import socket


def demo_register_basic():
    """基本注册演示"""
    print("=" * 50)
    print("register() 基本用法演示")
    print("=" * 50)

    sel = selectors.DefaultSelector()

    # 创建 socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 0))
    sock.listen(1)
    sock.setblocking(False)

    # 注册监听读事件
    print("\n1. 注册监听 EVENT_READ:")
    key = sel.register(sock, selectors.EVENT_READ)
    print(f"   返回 SelectorKey: fd={key.fd}, events={key.events}, data={key.data}")

    sel.unregister(sock)

    # 注册监听写事件
    print("\n2. 注册监听 EVENT_WRITE:")
    key = sel.register(sock, selectors.EVENT_WRITE)
    print(f"   返回 SelectorKey: fd={key.fd}, events={key.events}, data={key.data}")

    sel.unregister(sock)

    # 注册监听读+写事件
    print("\n3. 注册监听 EVENT_READ | EVENT_WRITE:")
    key = sel.register(sock, selectors.EVENT_READ | selectors.EVENT_WRITE)
    print(f"   返回 SelectorKey: fd={key.fd}, events={key.events}, data={key.data}")

    sel.unregister(sock)

    # 带 data 参数注册
    print("\n4. 带 data 参数注册:")

    def my_callback(sock, mask):
        pass

    key = sel.register(sock, selectors.EVENT_READ, data=my_callback)
    print(f"   返回 SelectorKey: fd={key.fd}, events={key.events}, data={key.data.__name__}")

    # 清理
    sel.unregister(sock)
    sel.close()
    sock.close()
    print("\n资源已清理")


def demo_register_errors():
    """演示注册时可能发生的错误"""
    print("\n" + "=" * 50)
    print("register() 错误处理演示")
    print("=" * 50)

    sel = selectors.DefaultSelector()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 0))
    sock.listen(1)
    sock.setblocking(False)

    # 正常注册
    sel.register(sock, selectors.EVENT_READ)

    # 错误1: 重复注册同一个文件对象
    print("\n1. 重复注册同一 socket:")
    try:
        sel.register(sock, selectors.EVENT_READ)
    except KeyError as e:
        print(f"   KeyError: {e}")

    # 错误2: 无效的事件掩码
    sel.unregister(sock)
    print("\n2. 无效的事件掩码 (events=0):")
    try:
        sel.register(sock, 0)
    except ValueError as e:
        print(f"   ValueError: {e}")

    # 错误3: 无效的文件对象
    print("\n3. 无效的文件对象 (fd=-1):")
    try:
        sel.register(-1, selectors.EVENT_READ)
    except (ValueError, OSError) as e:
        print(f"   {type(e).__name__}: {e}")

    # 清理
    sel.close()
    sock.close()
    print("\n资源已清理")


def demo_register_multiple():
    """演示注册多个文件对象"""
    print("\n" + "=" * 50)
    print("注册多个文件对象演示")
    print("=" * 50)

    sel = selectors.DefaultSelector()
    sockets = []

    # 创建并注册多个 socket
    for i in range(3):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('localhost', 0))
        sock.listen(1)
        sock.setblocking(False)
        sockets.append(sock)

        key = sel.register(sock, selectors.EVENT_READ, data=f"socket_{i}")
        print(f"  注册 socket_{i}: fd={key.fd}, port={sock.getsockname()[1]}")

    print(f"\n当前已注册 {len(sel.get_map())} 个文件对象")

    # 清理
    for sock in sockets:
        sel.unregister(sock)
        sock.close()
    sel.close()
    print("资源已清理")


if __name__ == "__main__":
    demo_register_basic()
    demo_register_errors()
    demo_register_multiple()
