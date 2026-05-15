"""
演示 selectors 的 modify() 方法

modify(fileobj, events, data=None)
- 修改已注册文件对象的监听事件或关联数据
- 等效于 unregister(fileobj) + register(fileobj, events, data)，但更高效
- 返回一个新的 SelectorKey
- 如果 fileobj 未注册会抛出 KeyError
- 如果 events 无效会抛出 ValueError
"""

import selectors
import socket


def demo_modify_events():
    """演示修改监听事件"""
    print("=" * 50)
    print("modify() 修改监听事件演示")
    print("=" * 50)

    sel = selectors.DefaultSelector()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 0))
    sock.listen(1)
    sock.setblocking(False)

    # 初始注册为读事件
    key = sel.register(sock, selectors.EVENT_READ, data="initial")
    print(f"\n初始注册: events={key.events} (EVENT_READ), data={key.data!r}")

    # 修改为写事件
    key = sel.modify(sock, selectors.EVENT_WRITE, data="initial")
    print(f"修改后:   events={key.events} (EVENT_WRITE), data={key.data!r}")

    # 修改为读+写事件
    key = sel.modify(sock, selectors.EVENT_READ | selectors.EVENT_WRITE, data="initial")
    print(f"再修改:   events={key.events} (READ|WRITE), data={key.data!r}")

    # 清理
    sel.unregister(sock)
    sel.close()
    sock.close()
    print("\n资源已清理")


def demo_modify_data():
    """演示修改关联数据"""
    print("\n" + "=" * 50)
    print("modify() 修改关联数据演示")
    print("=" * 50)

    sel = selectors.DefaultSelector()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 0))
    sock.listen(1)
    sock.setblocking(False)

    # 初始注册
    def on_accept(s, mask):
        pass

    def on_read(s, mask):
        pass

    key = sel.register(sock, selectors.EVENT_READ, data=on_accept)
    print(f"\n初始: data={key.data.__name__}")

    # 修改 data（回调函数从 accept 换成 read）
    key = sel.modify(sock, selectors.EVENT_READ, data=on_read)
    print(f"修改后: data={key.data.__name__}")

    # 修改 data 为字典
    key = sel.modify(sock, selectors.EVENT_READ, data={"state": "connected", "buffer": b""})
    print(f"再修改: data={key.data}")

    # 清理
    sel.unregister(sock)
    sel.close()
    sock.close()
    print("\n资源已清理")


def demo_modify_vs_reregister():
    """对比 modify 与 unregister+register"""
    print("\n" + "=" * 50)
    print("modify() vs unregister()+register() 对比")
    print("=" * 50)

    sel = selectors.DefaultSelector()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 0))
    sock.listen(1)
    sock.setblocking(False)

    sel.register(sock, selectors.EVENT_READ, data="v1")

    # 方式1: 使用 modify（推荐，更高效）
    print("\n方式1 - 使用 modify():")
    key = sel.modify(sock, selectors.EVENT_WRITE, data="v2")
    print(f"  结果: events={key.events}, data={key.data!r}")

    # 方式2: 先 unregister 再 register（等效但效率较低）
    print("\n方式2 - unregister() + register():")
    sel.unregister(sock)
    key = sel.register(sock, selectors.EVENT_READ, data="v3")
    print(f"  结果: events={key.events}, data={key.data!r}")

    print("\n结论: 两种方式效果相同，但 modify() 是原子操作且更高效")

    # 清理
    sel.unregister(sock)
    sel.close()
    sock.close()
    print("\n资源已清理")


def demo_modify_errors():
    """演示 modify 的错误情况"""
    print("\n" + "=" * 50)
    print("modify() 错误处理演示")
    print("=" * 50)

    sel = selectors.DefaultSelector()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 0))
    sock.listen(1)
    sock.setblocking(False)

    # 修改未注册的文件对象
    print("\n1. 修改未注册的 socket:")
    try:
        sel.modify(sock, selectors.EVENT_READ)
    except KeyError as e:
        print(f"   KeyError: {e}")

    # 使用无效事件掩码
    sel.register(sock, selectors.EVENT_READ)
    print("\n2. 使用无效事件掩码 (events=0):")
    try:
        sel.modify(sock, 0)
    except ValueError as e:
        print(f"   ValueError: {e}")

    # 清理（modify 失败时注册可能仍然存在）
    try:
        sel.unregister(sock)
    except KeyError:
        pass
    sel.close()
    sock.close()
    print("\n资源已清理")


if __name__ == "__main__":
    demo_modify_events()
    demo_modify_data()
    demo_modify_vs_reregister()
    demo_modify_errors()
