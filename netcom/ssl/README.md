## 使用说明

### 安装依赖（无需额外包，使用标准库）：

bash
```
仅需 Python 3.7+，无需安装第三方包
```

### 生成测试证书（首次运行会自动生成，或手动执行）：


bash
```
python -c "from netcom.ssl.ssl_wrapper.cert_utils import generate_self_signed_cert; generate_self_signed_cert()"
```

### 运行 SSL 演示：

bash
```
python examples/ssl_demo.py
```

### 测试加密连接：

* 选择模式 2（交互式聊天）
* 在一个终端运行服务器（模式1）
* 在另一个终端运行客户端（模式2）

## 核心知识点展示
这些文件演示了 Python SSL 模块的关键功能：

* ✅ 创建 SSL 上下文（服务端/客户端）
* ✅ 加载证书和私钥
* ✅ 将普通 socket 升级为 SSL socket
* ✅ 验证对端证书
* ✅ 获取 TLS 版本和加密套件信息
* ✅ 处理 SSL 错误

所有代码都是完整且可运行的，您可以直接使用它们来学习 Python 的 SSL/TLS 编程。