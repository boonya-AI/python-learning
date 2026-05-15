"""
演示 selectors.SelectorKey 命名元组

SelectorKey 是一个 namedtuple，包含以下属性:
- fileobj: 已注册的文件对象
- fd: 底层文件描述符
- events: 等待的事件位掩码
- data: 与文件对象关联的可选数据
"""

import selectors
import socket


def demo_selector_key():
    """演示 SelectorKey 的属性"""
    print("=" * 50)
    print("SelectorKey 命名元组演示")
    print("=" * 50)

    sel = selectors.DefaultSelector()

    # 创建一个 socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 0))
    sock.listen(1)
    sock.setblocking(False)

    # register 返回一个 SelectorKey
    key = sel.register(sock, selectors.EVENT_READ, data="my_server_socket")

    print(f"\nSelectorKey 类型: {type(key)}")
    print(f"SelectorKey 内容: {key}")
    print()
    print("各属性详解:")
    print(f"  key.fileobj = {key.fileobj}")
    print(f"    -> 类型: {type(key.fileobj)}")
    print(f"  key.fd      = {key.fd}")
    print(f"    -> 底层文件描述符(整数)")
    print(f"  key.events  = {key.events}")
    print(f"    -> 事件掩码 (EVENT_READ={selectors.EVENT_READ})")
    print(f"  key.data    = {key.data!r}")
    print(f"    -> 用户关联的自定义数据")

    # 验证 fd 与 socket.fileno() 一致
    print(f"\n验证: key.fd == sock.fileno() -> {key.fd == sock.fileno()}")

    # SelectorKey 是 namedtuple，支持索引访问
    print(f"\n通过索引访问: key[0]={key[0]}, key[1]={key[1]}, key[2]={key[2]}, key[3]={key[3]!r}")

    # 解包
    fileobj, fd, events, data = key
    print(f"解包: fileobj={fileobj}, fd={fd}, events={events}, data={data!r}")

    # 清理
    sel.unregister(sock)
    sel.close()
    sock.close()
    print("\n资源已清理")


def demo_selector_key_with_data():
    """演示使用 data 属性存储回调函数或会话信息"""
    print("\n" + "=" * 50)
    print("SelectorKey.data 实际用途演示")
    print("=" * 50)

    sel = selectors.DefaultSelector()

    # 创建 socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 0))
    sock.listen(1)
    sock.setblocking(False)

    # 用途1: data 存储回调函数
    def on_accept(sock, mask):
        print(f"  回调被调用: 接受新连接, mask={mask}")

    key1 = sel.register(sock, selectors.EVENT_READ, data=on_accept)
    print(f"\n用途1 - 存储回调函数:")
    print(f"  key.data = {key1.data}")
    print(f"  key.data.__name__ = {key1.data.__name__}")

    sel.unregister(sock)

    # 用途2: data 存储字典（会话信息）
    session_info = {
        "role": "server",
        "address": sock.getsockname(),
        "max_connections": 100,
    }
    key2 = sel.register(sock, selectors.EVENT_READ, data=session_info)
    print(f"\n用途2 - 存储会话信息字典:")
    print(f"  key.data = {key2.data}")

    # 清理
    sel.unregister(sock)
    sel.close()
    sock.close()
    print("\n资源已清理")


if __name__ == "__main__":
    demo_selector_key()
    demo_selector_key_with_data()
