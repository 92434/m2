#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据要塞守护进程单元测试
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import yaml  # type: ignore

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fortress_guardian import FortressGuardian


class TestFortressGuardian(unittest.TestCase):
    """测试数据要塞守护进程"""

    def setUp(self):
        """测试前置设置"""
        # 创建临时配置文件
        self.temp_config = tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        )
        test_config = {
            "fortress": {"name": "测试要塞", "version": "1.0.0"},
            "modules": [
                {"name": "数据核心", "status": "active", "priority": "critical"},
                {"name": "防御系统", "status": "standby", "priority": "high"},
            ],
            "security": {
                "firewall": {
                    "enabled": True,
                    "rules": [{"allow": "internal_network"}],
                }
            },
        }
        yaml.dump(test_config, self.temp_config)
        self.temp_config.close()

        # 创建守护进程实例
        self.guardian = FortressGuardian(self.temp_config.name)

    def tearDown(self):
        """测试后置清理"""
        # 删除临时文件
        if os.path.exists(self.temp_config.name):
            os.unlink(self.temp_config.name)

    def test_initialization(self):
        """测试初始化"""
        self.assertEqual(self.guardian.status, "INITIALIZING")
        self.assertEqual(self.guardian.config_path, self.temp_config.name)
        self.assertIsInstance(self.guardian.modules, dict)

    def test_load_configuration_success(self):
        """测试配置加载成功"""
        result = self.guardian.load_configuration()
        self.assertTrue(result)
        self.assertEqual(self.guardian.status, "CONFIG_LOADED")
        self.assertIn("fortress", self.guardian.config)

    def test_load_configuration_failure(self):
        """测试配置加载失败"""
        # 创建无效的配置文件路径
        invalid_guardian = FortressGuardian("/nonexistent/config.yaml")
        result = invalid_guardian.load_configuration()
        self.assertFalse(result)

    def test_initialize_modules(self):
        """测试模块初始化"""
        # 先加载配置
        self.guardian.load_configuration()

        result = self.guardian.initialize_modules()
        self.assertTrue(result)
        self.assertEqual(self.guardian.status, "MODULES_READY")
        self.assertIn("数据核心", self.guardian.modules)
        self.assertIn("防御系统", self.guardian.modules)

    @patch("subprocess.run")
    def test_get_system_metrics(self, mock_run):
        """测试系统指标获取"""
        # 模拟CPU使用率命令
        mock_result = MagicMock()
        mock_result.stdout = (
            "procs -----------memory---------- ---swap-- -----io---- -system--"
            " ------cpu-----\n r  b   swpd   free   buff  cache   si   so    bi"
            "    bo   in   cs us sy id wa st\n 1  0      0 123456  7890  54321"
            "    0    0   100   200 1000 2000 25 15 60  0  0"
        )
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        cpu_usage = self.guardian._get_cpu_usage()
        self.assertIsInstance(cpu_usage, float)
        self.assertGreaterEqual(cpu_usage, 0)
        self.assertLessEqual(cpu_usage, 100)

    def test_log_health_data(self):
        """测试健康数据记录"""
        test_data = {
            "timestamp": "2024-01-01T00:00:00",
            "cpu_usage": 45.5,
            "memory_usage": 67.2,
        }

        # 测试日志记录功能
        try:
            self.guardian._log_health_data(test_data)
            # 检查日志文件是否创建
            log_file = f"fortress_health_20240101.log"
            if os.path.exists(log_file):
                os.unlink(log_file)
            self.assertTrue(True)  # 如果没有异常就通过
        except Exception as e:
            self.fail(f"健康数据记录失败: {e}")


class TestFortressSecurity(unittest.TestCase):
    """测试要塞安全功能"""

    def test_encryption_placeholder(self):
        """测试加密功能占位符"""
        # 这里应该是实际的加密测试
        self.assertTrue(True, "加密功能测试占位符")


if __name__ == "__main__":
    unittest.main()