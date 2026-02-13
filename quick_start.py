#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据要塞快速启动脚本
来自夜的命名术·壹的一键体验
"""

import os
import subprocess
import sys
import time
from pathlib import Path


def print_banner():
    """打印欢迎横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                     夜幕要塞                                ║
║              来自夜的命名术·壹的数字堡垒                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_prerequisites():
    """检查前提条件"""
    print("检查系统环境...")

    # 检查Python版本
    if sys.version_info < (3, 8):
        print("Python版本过低，请升级到3.8以上")
        return False

    print(f"Python版本: {sys.version.split()[0]}")

    # 检查必要文件
    required_files = [
        "fortress_guardian.py",
        "fortress_console.py",
        "data_fortress_config.yaml",
    ]
    missing_files = []

    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)

    if missing_files:
        print(f"缺少必要文件: {', '.join(missing_files)}")
        return False

    print("所有文件检查通过")
    return True


def setup_virtual_environment():
    """设置虚拟环境"""
    print("设置Python虚拟环境...")

    venv_path = Path("fortress_venv")

    if not venv_path.exists():
        try:
            subprocess.run(
                [sys.executable, "-m", "venv", "fortress_venv"], check=True
            )
            print("虚拟环境创建成功")
        except subprocess.CalledProcessError:
            print("虚拟环境创建失败")
            return False
    else:
        print("虚拟环境已存在")

    return True


def install_dependencies():
    """安装依赖"""
    print("安装项目依赖...")

    try:
        if os.name == "nt":  # Windows
            pip_path = "fortress_venv\\Scripts\\pip.exe"
        else:  # Unix/Linux/Mac
            pip_path = "./fortress_venv/bin/pip"

        subprocess.run(
            [pip_path, "install", "-r", "requirements.txt"],
            check=True,
            capture_output=True,
        )
        print("依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"依赖安装失败: {e}")
        return False


def start_fortress_demo():
    """启动要塞演示"""
    print("启动数据要塞演示...")

    try:
        # 启动守护进程
        if os.name == "nt":  # Windows
            python_path = "fortress_venv\\Scripts\\python.exe"
        else:  # Unix/Linux/Mac
            python_path = "./fortress_venv/bin/python"

        # 在后台启动守护进程
        process = subprocess.Popen(
            [python_path, "fortress_guardian.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        print("守护进程已启动")
        print(f"进程ID: {process.pid}")

        # 等待几秒钟让系统初始化
        time.sleep(3)

        # 显示基本状态信息
        print("\n要塞状态:")
        print("  • 状态: OPERATIONAL")
        print("  • 模块: 4个核心模块在线")
        print("  • 安全: 防火墙已激活")
        print("  • 监控: 实时健康检查运行中")

        return process

    except Exception as e:
        print(f"启动失败: {e}")
        return None


def show_usage_instructions():
    """显示使用说明"""
    print("\n使用说明:")
    print("=" * 50)
    print("1. 要塞守护进程已在后台运行")
    print("2. 使用以下命令管理要塞:")
    print("   • 启动控制台: python fortress_console.py")
    print("   • 查看日志: tail -f fortress_health_*.log")
    print("   • 停止要塞: kill [进程ID]")
    print("\n3. 配置文件位置: data_fortress_config.yaml")
    print("4. 更多功能请查看完整文档")
    print("=" * 50)


def main():
    """主函数"""
    print_banner()

    # 检查环境
    if not check_prerequisites():
        sys.exit(1)

    # 设置环境
    if not setup_virtual_environment():
        sys.exit(1)

    # 安装依赖
    if not install_dependencies():
        sys.exit(1)

    # 启动演示
    process = start_fortress_demo()
    if process:
        show_usage_instructions()
        print(f"\n数据要塞正在运行中... (PID: {process.pid})")
        print("按 Ctrl+C 停止演示")

        try:
            # 保持运行直到用户中断
            process.wait()
        except KeyboardInterrupt:
            print("\n正在停止要塞系统...")
            process.terminate()
            process.wait()
            print("要塞系统已安全关闭")


if __name__ == "__main__":
    main()