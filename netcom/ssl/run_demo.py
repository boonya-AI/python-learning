# 在 run_demo.py 的菜单中添加
def run_ssl_demo():
    """运行 SSL 示例"""
    from examples.ssl_demo import run_ssl_server, run_ssl_client
    print("\n1. 运行服务器")
    print("2. 运行客户端")
    choice = input("选择: ")
    if choice == '1':
        run_ssl_server()
    else:
        run_ssl_client()

# 在主菜单中添加选项
# print("7. SSL/TLS 加密通信")