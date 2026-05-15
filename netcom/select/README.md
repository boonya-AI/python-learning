## 目录结构
```
├── select/
│   └── examples/           # 新增 select 模块示例
│       ├── __init__.py
│       ├── simple_select_server.py # 基础 select 服务器
│       ├── poll_server.py          # poll 服务器示例
│       ├── epoll_server.py         # epoll 服务器 (Linux)
│       ├── echo_client.py          # 通用测试客户端
│       └── multi_chat_server.py    # 多路聊天室服务器
├────────── run_select_demo.py      # 新增 select 演示入口
└── ...
```

## 平台兼容性

* Windows: 仅支持 select，不支持 poll/epoll/kqueue
* Linux: 支持 select、poll、epoll（推荐）
* macOS/BSD: 支持 select、poll、kqueue

## 性能优化建议

```
# 边缘触发模式下必须循环读取
while True:
    try:
        data = sock.recv(4096)
        if not data: break
        process(data)
    except BlockingIOError:
        break  # 数据已读完

# 使用更大的缓冲区
```