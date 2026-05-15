"""
证书生成辅助工具 - 用于快速生成测试用自签名证书
生产环境请使用正规 CA 签发的证书
"""

import subprocess
import os
from pathlib import Path


def generate_self_signed_cert(cert_dir: str = 'certs',
                              common_name: str = 'localhost'):
    """
    生成自签名证书（仅用于开发测试）

    需要系统安装 openssl 命令
    """
    Path(cert_dir).mkdir(parents=True, exist_ok=True)

    cert_path = os.path.join(cert_dir, 'server.crt')
    key_path = os.path.join(cert_dir, 'server.key')

    # openssl 命令生成私钥和证书
    cmd = [
        'openssl', 'req', '-x509', '-newkey', 'rsa:4096',
        '-keyout', key_path, '-out', cert_path,
        '-days', '365', '-nodes',
        '-subj', f'/CN={common_name}'
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"自签名证书已生成:")
        print(f"  证书: {cert_path}")
        print(f"  私钥: {key_path}")
        return cert_path, key_path
    except subprocess.CalledProcessError as e:
        print(f"证书生成失败: {e}")
        print("请确保已安装 openssl 命令")
        return None, None
    except FileNotFoundError:
        print("未找到 openssl 命令，请安装 openssl 或手动提供证书")
        return None, None


def verify_certificate(cert_path: str):
    """验证证书信息"""
    cmd = ['openssl', 'x509', '-in', cert_path, '-text', '-noout']
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"验证失败: {e}")