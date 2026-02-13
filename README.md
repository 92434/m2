# 🏰 白昼数据要塞 - 来自白昼组织的数字堡垒

这是一个高度安全的数据防护系统，由白昼组织开发，灵感来源于《夜的命名术》中的数字堡垒概念。该系统提供了企业级的数据保护、监控和管理功能。

## 🌟 系统特性

### 🔐 核心安全功能
- **多层加密保护**: AES-256-GCM + ChaCha20-Poly1305双重加密
- **生物识别认证**: 双因子生物特征验证
- **智能防火墙**: 动态规则引擎和入侵检测
- **零信任架构**: 基于身份的访问控制

### 🛡️ 防护体系
- **主动防御**: 实时威胁检测和响应
- **数据分片**: 7+3纠删码存储策略
- **异地备份**: 多地域冗余备份机制
- **完整性校验**: SHA-256哈希链验证

### 📊 监控管理
- **实时监控**: 24/7系统健康状态监控
- **可视化控制台**: TUI图形界面管理
- **智能告警**: 异常行为自动检测和通知
- **性能分析**: 资源使用统计和优化建议

## 📁 目录结构

```
baizhou-fortress/
├── data_fortress_config.yaml    # 核心配置文件
├── fortress_guardian.py         # 守护进程主程序
├── fortress_console.py          # 控制台界面程序
├── deploy_fortress.sh           # 一键部署脚本
├── quick_start.py               # 快速启动脚本
├── requirements.txt             # 项目依赖
└── README.md                    # 系统文档
```

## 🚀 快速开始

### GitHub Actions 自动化测试

本项目已配置GitHub Actions工作流，可自动测试数据要塞系统：

#### 🧪 测试工作流
- **文件**: `.github/workflows/test-fortress.yml`
- **触发条件**: Push到main/develop分支或Pull Request
- **测试内容**:
  - 环境设置和依赖安装
  - 配置文件验证
  - 快速功能测试
  - 安全模块测试
  - 部署脚本验证

#### 🚀 部署工作流
- **文件**: `.github/workflows/fortress-deploy.yml`
- **支持环境**: test, staging, production
- **部署方式**: 手动触发或自动部署

### 本地快速体验

```bash
# 1. 克隆项目
git clone https://github.com/yourusername/baizhou-fortress.git
cd baizhou-fortress

# 2. 运行快速启动脚本
python quick_start.py
```

### 完整部署

```bash
# 1. 给予执行权限
chmod +x deploy_fortress.sh

# 2. 以root权限运行部署脚本
sudo ./deploy_fortress.sh
```

## ⚙️ 系统配置

### 主配置文件 (`data_fortress_config.yaml`)

```yaml
fortress:
  name: "白昼要塞"
  version: "1.0.0"
  codename: "白昼一号数据壁垒"
  organization: "白昼"

security:
  encryption_level: "AES-256-GCM"
  authentication:
    method: "biometric-dual-factor"
    timeout: 300

storage:
  data_shards: 7
  parity_shards: 3
  backup_locations:
    - "/backup/local"
    - "s3://night-fortress-backup"
```

### 环境变量配置

```bash
# 在 ~/.bashrc 或 ~/.zshrc 中添加
export FORTRESS_MASTER_KEY="your-master-key-here"
export BACKUP_KEY_1="backup-key-1"
export BACKUP_KEY_2="backup-key-2"
```

## 🎮 使用指南

### 启动和管理

```bash
# 启动要塞系统
/opt/baizhou-fortress/bin/start_fortress.sh

# 停止要塞系统
/opt/baizhou-fortress/bin/stop_fortress.sh

# 查看系统状态
/opt/baizhou-fortress/bin/status_fortress.sh
```

### 控制台操作

```bash
# 启动图形化控制台
python3 /opt/baizhou-fortress/bin/fortress_console.py
```

控制台快捷键：
- `1` - 仪表板视图
- `2` - 模块管理
- `3` - 安全监控
- `4` - 系统日志
- `Q` - 退出控制台

### 服务管理

```bash
# 查看服务状态
systemctl status fortress-guardian

# 重启服务
systemctl restart fortress-guardian

# 查看服务日志
journalctl -u fortress-guardian -f
```

## 🔧 高级配置

### 自定义防火墙规则

编辑 `/opt/night-fortress/config/firewall.rules`:

```bash
# 允许特定IP访问
allow from 192.168.1.0/24 to port 8443

# 限制访问频率
rate-limit 100 requests/minute

# 启用地理IP过滤
geoip block country CN,RU
```

### 性能调优

```bash
# 调整内存分配
echo 'vm.swappiness=10' >> /etc/sysctl.conf

# 优化网络参数
echo 'net.core.rmem_max=16777216' >> /etc/sysctl.conf

# 重启sysctl
sysctl -p
```

## 📈 监控和维护

### 日志文件位置

```
/var/log/fortress/              # 系统日志目录
/opt/baizhou-fortress/logs/     # 应用日志目录
/var/log/fortress-deploy.log    # 部署日志
```

### 定期维护任务

```bash
# 每日备份检查
0 2 * * * /opt/baizhou-fortress/scripts/daily_backup_check.sh

# 每周系统健康检查
0 3 * * 0 /opt/baizhou-fortress/scripts/weekly_health_check.sh

# 每月安全审计
0 4 1 * * /opt/night-fortress/scripts/monthly_security_audit.sh
```

### 性能监控

```bash
# 实时监控系统资源
htop

# 查看磁盘IO
iotop

# 网络连接状态
ss -tuln

# 系统负载
uptime
```

## 🔧 GitHub Actions 集成

### 测试配置

在仓库设置中添加以下Secrets：
```
FORTRESS_MASTER_KEY=your-master-key
BACKUP_KEY_1=your-backup-key-1
BACKUP_KEY_2=your-backup-key-2
```

### 手动触发测试

1. 访问仓库的Actions页面
2. 选择"白昼数据要塞测试"工作流
3. 点击"Run workflow"按钮
4. 选择测试模式（full/quick/security）

### 环境配置

工作流支持三种环境：
- **test**: 测试环境
- **staging**: 预发布环境  
- **production**: 生产环境

## 🔒 安全最佳实践

### 访问控制
- 使用最小权限原则
- 定期轮换密钥和证书
- 启用双因子认证
- 限制物理访问

### 网络安全
- 启用防火墙和入侵检测
- 使用VPN进行远程访问
- 定期更新安全补丁
- 监控异常网络流量

### 数据保护
- 启用全盘加密
- 实施数据备份策略
- 定期验证备份完整性
- 建立灾难恢复计划

## 🆘 故障排除

### 常见问题

**GitHub Actions测试失败**
```bash
# 检查工作流日志
# 在Actions页面查看详细的错误信息

# 本地重现问题
python -m pytest tests/ -v
```

**服务无法启动**
```bash
# 检查配置文件语法
python3 -m yaml data_fortress_config.yaml

# 查看详细错误日志
journalctl -u fortress-guardian --no-pager
```

**控制台无法连接**
```bash
# 检查端口是否开放
netstat -tlnp | grep 8443

# 验证防火墙规则
ufw status verbose
```

**性能问题**
```bash
# 检查系统资源使用
free -h
df -h
iostat -x 1

# 分析进程占用
ps aux --sort=-%cpu | head -10
```

### 紧急恢复

```bash
# 紧急停止所有服务
systemctl stop fortress-guardian
killall python3

# 从备份恢复配置
cp /backup/latest/config/* /opt/night-fortress/config/

# 重新启动系统
/opt/night-fortress/bin/start_fortress.sh
```

## 📞 技术支持

### 社区支持
- GitHub Issues: [项目问题跟踪](https://github.com/yourusername/night-fortress/issues)
- 讨论区: [社区论坛](https://github.com/yourusername/night-fortress/discussions)

### 商业支持
如需企业级技术支持，请联系: support@baizhou.org

## 📄 许可证

本项目采用MIT许可证，详情请参见 [LICENSE](LICENSE) 文件。

---

**来自白昼组织的数字堡垒** 🏰

*"在数字化的时代，我们守护着数据的光明"*

[![Test Status](https://github.com/yourusername/baizhou-fortress/actions/workflows/test-fortress.yml/badge.svg)](https://github.com/yourusername/baizhou-fortress/actions/workflows/test-fortress.yml)