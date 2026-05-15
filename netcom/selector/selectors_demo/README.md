
## 测试说明

```
# 查看所有演示列表
python -m selectors_demo

# 单独运行各功能演示
python -m selectors_demo.basics.event_constants
python -m selectors_demo.methods.select_demo
python -m selectors_demo.servers.selector_types

# 服务器+客户端联调
python -m selectors_demo.servers.echo_server    # 终端1
python -m selectors_demo.clients.auto_test      # 终端2
```