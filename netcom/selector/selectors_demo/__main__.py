"""
selectors 模块功能演示 - 主入口

运行方式:
    python -m selectors_demo

将列出所有可运行的演示模块
"""

import sys


def main():
    print("=" * 60)
    print("  selectors 模块功能演示")
    print("  基于 https://docs.python.org/zh-cn/3.14/library/selectors.html")
    print("=" * 60)

    print("""
包结构:
  selectors_demo/
  ├── basics/                    # 基础概念
  │   ├── event_constants.py     # EVENT_READ/EVENT_WRITE 常量
  │   ├── selector_key.py        # SelectorKey 命名元组
  │   └── context_manager.py     # 上下文管理器协议
  ├── methods/                   # 方法演示
  │   ├── register_demo.py       # register() 方法
  │   ├── unregister_demo.py     # unregister() 方法
  │   ├── modify_demo.py         # modify() 方法
  │   ├── select_demo.py         # select() 方法
  │   └── get_key_map_demo.py    # get_key()/get_map() 方法
  ├── servers/                   # 服务器示例
  │   ├── echo_server.py         # DefaultSelector 回声服务器
  │   ├── chat_server.py         # SelectSelector 聊天服务器
  │   └── selector_types.py      # Selector 类型检测
  └── clients/                   # 客户端工具
      ├── echo_client.py         # 回声服务器客户端
      ├── chat_client.py         # 聊天服务器客户端
      └── auto_test.py           # 自动化测试客户端

运行各演示:
  # 基础概念
  python -m selectors_demo.basics.event_constants
  python -m selectors_demo.basics.selector_key
  python -m selectors_demo.basics.context_manager

  # 方法演示
  python -m selectors_demo.methods.register_demo
  python -m selectors_demo.methods.unregister_demo
  python -m selectors_demo.methods.modify_demo
  python -m selectors_demo.methods.select_demo
  python -m selectors_demo.methods.get_key_map_demo

  # Selector 类型检测
  python -m selectors_demo.servers.selector_types

  # 服务器（需要另开终端运行客户端）
  python -m selectors_demo.servers.echo_server
  python -m selectors_demo.servers.chat_server

  # 客户端（需要先启动对应服务器）
  python -m selectors_demo.clients.echo_client
  python -m selectors_demo.clients.chat_client
  python -m selectors_demo.clients.auto_test
""")


if __name__ == "__main__":
    main()
