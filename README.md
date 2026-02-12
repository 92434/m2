# Docker镜像传输工具

这是一个用于将Docker镜像从任意仓库传输到GitHub Container Registry(GHCR)的自动化工具。

## 🌐 远程访问方案（ngrok）

### 为什么选择ngrok？

相比传统方案，ngrok提供：
- 更稳定的连接体验
- 支持多种协议（HTTP/TCP/WebSocket）
- 可自定义域名和认证
- 更好的性能和可靠性

### 使用方法

1. **快速启动**（推荐）：
```bash
chmod +x quick-ngrok.sh
./quick-ngrok.sh
```

2. **完整功能版**：
```bash
chmod +x ngrok-remote-access.sh
./ngrok-remote-access.sh
```

3. **手动配置**：
```bash
# 安装ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar -xzf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin/

# 启动服务
ttyd -p 8080 bash &  # Web终端
ngrok http 8080 &    # ngrok隧道
```

### 访问方式

启动后会显示：
- **Web终端**: 通过浏览器访问提供的HTTPS地址
- **SSH连接**: `ssh runner@[显示的IP地址]`
- **文件传输**: HTTP文件服务器

### 配置文件

`ngrok.yml` 支持：
```yaml
authtoken: YOUR_TOKEN
tunnels:
  web-terminal:
    addr: 8080
    proto: http
  ssh-access:
    addr: 22
    proto: tcp
```

## 🔒 安全提醒

- ngrok免费版有连接限制
- 建议使用认证token提高安全性
- 及时关闭不需要的远程访问
- 敏感操作完成后立即终止会话

## 🏗️ 架构设计

### 工作流分割策略："一分二，二分四"

#### 第一层：主协调器 (1个)
- `main-workflow.yml` - 主入口工作流
- 负责接收用户输入和初始化参数

#### 第二层：并行处理流程 (2个)  
- `auth-workflow.yml` - 认证流程
- `pull-workflow.yml` - 拉取流程

#### 第三层：具体操作单元 (4个)
- `tag-workflow.yml` - 标记操作
- `push-workflow.yml` - 推送操作
- `complete-coordinator.yml` - 完整协调流程

## 📁 文件结构

```
.github/workflows/
├── main-workflow.yml          # 主工作流入口
├── auth-workflow.yml          # 认证专用工作流
├── pull-workflow.yml          # 拉取专用工作流  
├── tag-workflow.yml           # 标记专用工作流
├── push-workflow.yml          # 推送专用工作流
└── complete-coordinator.yml   # 完整协调工作流
```

## 🔧 使用方法

### 方案一：使用完整协调工作流（推荐）
1. 在GitHub Actions页面选择 `complete-coordinator.yml`
2. 设置参数：
   - `source_image`: 源镜像地址（默认：`jiangrui1994/cloudsaver:latest`）
   - `target_name`: 目标包名称（默认：`cloudsaver`）
3. 点击运行

### 方案二：分步执行
1. 先运行 `main-workflow.yml` 触发主流程
2. 各个子工作流会自动按依赖关系执行

### ⚙️ 配置要求

### GitHub Secrets
- `GITHUB_TOKEN` - 需要 `packages: write` 权限

### 权限设置
确保仓库具有以下权限：
- 读取和写入包权限
- GitHub Actions执行权限

## 🎯 功能特点

- ✅ **模块化设计** - 每个功能独立成工作流
- ✅ **并行处理** - 认证和拉取可以同时进行
- ✅ **灵活组合** - 可根据需要选择执行路径
- ✅ **易于维护** - 单个组件故障不影响整体
- ✅ **可视化监控** - GitHub界面清晰显示各步骤状态

## 📊 执行流程

```
用户触发 ──→ 主协调器 ──→ 认证流程 ──→ Docker登录
                    │
                    └──→ 拉取流程 ──→ 镜像拉取
                    │
                    └──→ 标记流程 ──→ 镜像重标记
                    │
                    └──→ 推送流程 ──→ 发布到GHCR
```

## 🛠️ 故障排除

### 常见问题
1. **权限不足** - 检查GITHUB_TOKEN权限设置
2. **镜像拉取失败** - 确认源镜像是公开的或有访问权限
3. **推送失败** - 验证GitHub Packages存储空间
4. **ngrok连接失败**: 检查防火墙设置和token有效性
5. **Web终端无法访问**: 确认ttyd服务正常运行
6. **SSH连接被拒绝**: 检查SSH服务状态

### 调试建议
- 查看每个工作流的详细日志
- 检查依赖关系是否正确配置
- 验证环境变量和参数传递
- 对于远程访问问题，检查ngrok服务状态和网络配置

## 📝 注意事项

- 源镜像必须是公开的或配置了相应认证
- 目标仓库需要有足够的存储空间
- 建议定期清理旧的镜像版本