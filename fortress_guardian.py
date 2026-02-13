#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏰 数据要塞守护进程
来自夜的命名术·壹的数字守护者
"""

import json
import logging
import os
import subprocess
import sys
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional


class FortressGuardian:
    """数据要塞守护者核心类"""

    def __init__(self, config_path: str = "data_fortress_config.yaml"):
        self.config_path = config_path
        self.status = "INITIALIZING"
        self.modules = {}
        self.logger = self._setup_logger()
        self.encryption_key = None

    def _setup_logger(self) -> logging.Logger:
        """设置日志系统"""
        logger = logging.getLogger("FortressGuardian")
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def load_configuration(self) -> bool:
        """加载要塞配置"""
        try:
            import yaml

            with open(self.config_path, "r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f)

            self.logger.info("✅ 配置文件加载成功")
            self.status = "CONFIG_LOADED"
            return True

        except Exception as e:
            self.logger.error(f"❌ 配置加载失败: {e}")
            return False

    def initialize_modules(self) -> bool:
        """初始化要塞模块"""
        try:
            modules = self.config.get("modules", [])
            for module in modules:
                module_name = module["name"]
                self.modules[module_name] = {
                    "status": module["status"],
                    "priority": module["priority"],
                    "last_check": datetime.now().isoformat(),
                }

            self.logger.info(f"✅ 初始化了 {len(modules)} 个核心模块")
            self.status = "MODULES_READY"
            return True

        except Exception as e:
            self.logger.error(f"❌ 模块初始化失败: {e}")
            return False

    def start_defense_system(self) -> bool:
        """启动防御系统"""
        try:
            self.logger.info("🛡️ 启动防御系统...")

            # 模拟防火墙启动
            firewall_status = self._activate_firewall()
            if not firewall_status:
                raise Exception("防火墙激活失败")

            # 启动入侵检测
            ids_status = self._start_intrusion_detection()
            if not ids_status:
                raise Exception("入侵检测系统启动失败")

            self.modules["防御系统"]["status"] = "active"
            self.logger.info("✅ 防御系统启动完成")
            return True

        except Exception as e:
            self.logger.error(f"❌ 防御系统启动失败: {e}")
            return False

    def _activate_firewall(self) -> bool:
        """激活防火墙规则"""
        try:
            # 模拟防火墙规则应用
            rules = (
                self.config.get("security", {})
                .get("firewall", {})
                .get("rules", [])
            )
            self.logger.info(f"🔥 应用 {len(rules)} 条防火墙规则")
            time.sleep(2)  # 模拟处理时间
            return True
        except:
            return False

    def _start_intrusion_detection(self) -> bool:
        """启动入侵检测系统"""
        try:
            self.logger.info("👁️ 启动入侵检测系统")
            # 模拟IDS启动
            time.sleep(1)
            return True
        except:
            return False

    def monitor_system_health(self):
        """持续监控系统健康状态"""
        while self.status != "SHUTDOWN":
            try:
                health_data = {
                    "timestamp": datetime.now().isoformat(),
                    "cpu_usage": self._get_cpu_usage(),
                    "memory_usage": self._get_memory_usage(),
                    "disk_usage": self._get_disk_usage(),
                    "network_status": self._check_network(),
                    "module_status": self.modules.copy(),
                }

                # 检查异常状态
                if health_data["cpu_usage"] > 85:
                    self.logger.warning(
                        f"⚠️ CPU使用率过高: {health_data['cpu_usage']}%"
                    )

                if health_data["memory_usage"] > 80:
                    self.logger.warning(
                        f"⚠️ 内存使用率过高: {health_data['memory_usage']}%"
                    )

                self._log_health_data(health_data)
                time.sleep(60)  # 每分钟检查一次

            except Exception as e:
                self.logger.error(f"❌ 健康监控异常: {e}")
                time.sleep(10)

    def _get_cpu_usage(self) -> float:
        """获取CPU使用率"""
        try:
            result = subprocess.run(
                ["vmstat", "1", "2"], capture_output=True, text=True
            )
            lines = result.stdout.strip().split("\n")
            if len(lines) >= 4:
                # 解析最后一行的idle列
                idle = int(lines[-1].split()[15])
                return 100 - idle
            return 0.0
        except:
            return 0.0

    def _get_memory_usage(self) -> float:
        """获取内存使用率"""
        try:
            with open("/proc/meminfo", "r") as f:
                lines = f.readlines()
                mem_total = int(lines[0].split()[1])  # KB
                mem_free = int(lines[1].split()[1])
                mem_available = int(lines[2].split()[1])
                used = mem_total - mem_available
                return (used / mem_total) * 100
        except:
            return 0.0

    def _get_disk_usage(self) -> float:
        """获取磁盘使用率"""
        try:
            result = subprocess.run(["df", "/"], capture_output=True, text=True)
            lines = result.stdout.strip().split("\n")
            if len(lines) >= 2:
                usage_percent = lines[1].split()[4]  # 第5列是使用百分比
                return float(usage_percent.rstrip("%"))
            return 0.0
        except:
            return 0.0

    def _check_network(self) -> str:
        """检查网络状态"""
        try:
            result = subprocess.run(
                ["ping", "-c", "1", "8.8.8.8"],
                capture_output=True,
                timeout=5,
            )
            return "connected" if result.returncode == 0 else "disconnected"
        except:
            return "unknown"

    def _log_health_data(self, data: Dict):
        """记录健康数据"""
        try:
            log_file = f"fortress_health_{datetime.now().strftime('%Y%m%d')}.log"
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(data, ensure_ascii=False) + "\n")
        except Exception as e:
            self.logger.error(f"❌ 健康数据记录失败: {e}")

    def start(self):
        """启动要塞守护进程"""
        self.logger.info("🏰 数据要塞守护进程启动")
        self.logger.info("来自夜的命名术·壹的数字堡垒")

        # 加载配置
        if not self.load_configuration():
            return False

        # 初始化模块
        if not self.initialize_modules():
            return False

        # 启动防御系统
        if not self.start_defense_system():
            return False

        self.status = "OPERATIONAL"
        self.logger.info("✅ 数据要塞已进入运行状态")

        # 启动健康监控线程
        monitor_thread = threading.Thread(
            target=self.monitor_system_health, daemon=True
        )
        monitor_thread.start()

        return True

    def shutdown(self):
        """关闭要塞系统"""
        self.logger.info("🌙 开始关闭数据要塞...")
        self.status = "SHUTDOWN"
        time.sleep(2)
        self.logger.info("✅ 数据要塞已安全关闭")


def main():
    """主函数"""
    guardian = FortressGuardian()

    try:
        if guardian.start():
            # 保持运行
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        guardian.shutdown()
    except Exception as e:
        print(f"_fatal error: {e}")
        guardian.shutdown()


if __name__ == "__main__":
    main()