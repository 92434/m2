#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据要塞控制台
夜的命名术·壹的指挥中心
"""

import curses
import json
import os
import subprocess
import sys
import threading
import time
from datetime import datetime
from typing import Dict, List


class FortressConsole:
    """数据要塞控制台主类"""

    def __init__(self):
        self.screen = None
        self.running = True
        self.current_view = "dashboard"
        self.system_stats = {}
        self.alerts = []
        self.selected_module = 0

    def initialize_curses(self):
        """初始化curses界面"""
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        curses.curs_set(0)

        # 设置颜色
        if curses.has_colors():
            curses.start_color()
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # 正常
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # 警告
            curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # 注意
            curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)  # 信息
            curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # 特殊

    def cleanup_curses(self):
        """清理curses环境"""
        if self.screen:
            curses.nocbreak()
            self.screen.keypad(False)
            curses.echo()
            curses.endwin()

    def draw_header(self):
        """绘制头部信息"""
        height, width = self.screen.getmaxyx()

        # 清空顶部区域
        for i in range(3):
            self.screen.addstr(i, 0, " " * width)

        # 绘制标题
        title = "夜幕要塞控制中心"
        title_x = (width - len(title)) // 2
        self.screen.addstr(0, title_x, title, curses.color_pair(1) | curses.A_BOLD)

        # 绘制状态栏
        status_text = (
            f"状态: OPERATIONAL | 时间: {datetime.now().strftime('%H:%M:%S')} |"
            f" 视图: {self.current_view.upper()}"
        )
        self.screen.addstr(1, 2, status_text[: width - 4], curses.color_pair(4))

        # 绘制菜单
        menu_items = ["[1]仪表板", "[2]模块管理", "[3]安全监控", "[4]系统日志", "[Q]退出"]
        menu_text = " | ".join(menu_items)
        menu_x = (width - len(menu_text)) // 2
        self.screen.addstr(2, menu_x, menu_text, curses.color_pair(3))

    def draw_dashboard(self):
        """绘制仪表板视图"""
        height, width = self.screen.getmaxyx()

        # 清空主显示区域
        for i in range(4, height - 1):
            self.screen.addstr(i, 0, " " * width)

        # 系统概览
        y_pos = 4
        self.screen.addstr(y_pos, 2, "系统概览", curses.color_pair(1) | curses.A_BOLD)
        y_pos += 2

        stats = self.get_system_stats()
        overview_items = [
            (
                "CPU使用率",
                f"{stats.get('cpu', 0):.1f}%",
                self.get_status_color(stats.get("cpu", 0)),
            ),
            (
                "内存使用率",
                f"{stats.get('memory', 0):.1f}%",
                self.get_status_color(stats.get("memory", 0)),
            ),
            (
                "磁盘使用率",
                f"{stats.get('disk', 0):.1f}%",
                self.get_status_color(stats.get("disk", 0)),
            ),
            ("网络状态", stats.get("network", "unknown"), curses.color_pair(1)),
            ("运行时间", stats.get("uptime", "00:00:00"), curses.color_pair(4)),
        ]

        for label, value, color in overview_items:
            self.screen.addstr(y_pos, 4, f"{label}:", curses.color_pair(4))
            self.screen.addstr(y_pos, 20, value, color)
            y_pos += 1

        # 模块状态
        y_pos += 1
        self.screen.addstr(y_pos, 2, "模块状态", curses.color_pair(1) | curses.A_BOLD)
        y_pos += 2

        modules = self.get_module_status()
        for module_name, status in modules.items():
            status_color = (
                curses.color_pair(1) if status == "active" else curses.color_pair(2)
            )
            self.screen.addstr(y_pos, 4, f"• {module_name}:", curses.color_pair(4))
            self.screen.addstr(y_pos, 25, status.upper(), status_color)
            y_pos += 1

        # 警报信息
        if self.alerts:
            y_pos += 1
            self.screen.addstr(
                y_pos, 2, "最新警报", curses.color_pair(2) | curses.A_BOLD
            )
            y_pos += 2
            for alert in self.alerts[-3:]:  # 显示最近3条警报
                self.screen.addstr(y_pos, 4, f"{alert}", curses.color_pair(2))
                y_pos += 1

    def get_system_stats(self) -> Dict:
        """获取系统统计信息"""
        return {
            "cpu": 45.2,
            "memory": 67.8,
            "disk": 34.1,
            "network": "connected",
            "uptime": "2d 14h 32m",
        }

    def get_module_status(self) -> Dict:
        """获取模块状态"""
        return {
            "数据核心": "active",
            "防御系统": "active",
            "传输通道": "operational",
            "监控系统": "standby",
        }

    def get_status_color(self, value: float) -> int:
        """根据数值返回状态颜色"""
        if value < 60:
            return curses.color_pair(1)  # 绿色 - 正常
        elif value < 80:
            return curses.color_pair(3)  # 黄色 - 警告
        else:
            return curses.color_pair(2)  # 红色 - 危险

    def draw_module_management(self):
        """绘制模块管理视图"""
        height, width = self.screen.getmaxyx()

        # 清空主显示区域
        for i in range(4, height - 1):
            self.screen.addstr(i, 0, " " * width)

        y_pos = 4
        self.screen.addstr(
            y_pos, 2, "模块管理系统", curses.color_pair(1) | curses.A_BOLD
        )
        y_pos += 2

        modules = [
            ("数据核心", "active", "critical"),
            ("防御系统", "active", "high"),
            ("传输通道", "operational", "medium"),
            ("监控系统", "standby", "low"),
        ]

        for i, (name, status, priority) in enumerate(modules):
            marker = "▶" if i == self.selected_module else " "
            status_color = (
                curses.color_pair(1) if status == "active" else curses.color_pair(3)
            )

            self.screen.addstr(y_pos, 4, f"{marker} {name}", curses.color_pair(4))
            self.screen.addstr(y_pos, 25, status.upper(), status_color)
            self.screen.addstr(y_pos, 35, f"[{priority.upper()}]", curses.color_pair(4))
            y_pos += 1

    def handle_input(self, key):
        """处理用户输入"""
        if key == ord("q") or key == ord("Q"):
            self.running = False
        elif key == ord("1"):
            self.current_view = "dashboard"
        elif key == ord("2"):
            self.current_view = "modules"
        elif key == ord("3"):
            self.current_view = "security"
        elif key == ord("4"):
            self.current_view = "logs"
        elif key == curses.KEY_UP and self.current_view == "modules":
            self.selected_module = max(0, self.selected_module - 1)
        elif key == curses.KEY_DOWN and self.current_view == "modules":
            self.selected_module = min(3, self.selected_module + 1)

    def simulate_alerts(self):
        """模拟警报生成"""
        alerts_list = [
            "检测到异常网络流量",
            "内存使用率超过阈值",
            "防火墙规则更新完成",
            "数据备份任务开始",
            "系统完整性检查通过",
        ]

        while self.running:
            if len(self.alerts) < 10:  # 限制警报数量
                import random

                alert = random.choice(alerts_list)
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.alerts.append(f"[{timestamp}] {alert}")
            time.sleep(30)  # 每30秒生成一次警报

    def run(self):
        """运行控制台主循环"""
        try:
            self.initialize_curses()

            # 启动警报模拟线程
            alert_thread = threading.Thread(target=self.simulate_alerts, daemon=True)
            alert_thread.start()

            while self.running:
                self.draw_header()

                if self.current_view == "dashboard":
                    self.draw_dashboard()
                elif self.current_view == "modules":
                    self.draw_module_management()
                # 其他视图可以后续添加

                self.screen.refresh()

                # 处理用户输入
                try:
                    key = self.screen.getch()
                    if key != -1:  # 有输入
                        self.handle_input(key)
                except:
                    pass

                time.sleep(0.1)  # 短暂延迟

        except KeyboardInterrupt:
            self.running = False
        finally:
            self.cleanup_curses()


def main():
    """主函数"""
    console = FortressConsole()
    console.run()


if __name__ == "__main__":
    main()