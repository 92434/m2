# GitHub Actions Docker 镜像发布工具

这个仓库包含用于将Docker镜像发布到GitHub Packages的自动化工作流。

## 工作流说明

### 1. docker-publish.yml
完整的Docker镜像发布工作流，包含详细的步骤和验证。

**功能特性：**
- 拉取指定的源镜像
- 重新标记为目标格式
- 推送到GitHub Container Registry
- 创建时间戳版本备份
- 完整的状态报告

### 2. image-transfer.yml  
简化的镜像传输工作流，专注于核心功能。

**功能特性：**
- 快速拉取和推送镜像
- 自动时间戳标记
- 简洁的操作流程

## 使用方法

### 触发工作流

1. 访问仓库的 **Actions** 页面
2. 选择要运行的工作流
3. 点击 **Run workflow** 按钮
4. 根据需要配置参数：
   - `source_image`: 源镜像地址（默认：jiangrui1994/cloudsaver:latest）
   - `target_name`: 目标包名称（默认：cloudsaver）
   - `image_tag`: 镜像标签（默认：latest）

### 参数说明

| 参数 | 描述 | 默认值 |
|------|------|--------|
| source_image | 要拉取的源镜像地址 | jiangrui1994/cloudsaver:latest |
| target_name | 在GitHub Packages中的包名 | cloudsaver |
| image_tag | 镜像标签 | latest |

## 下载使用发布的镜像

工作流成功执行后，可以通过以下方式下载镜像：

```bash
# 登录到GitHub Container Registry
echo ${{ secrets.GITHUB_TOKEN }} | docker login ghcr.io -u $GITHUB_ACTOR --password-stdin

# 拉取最新版本
docker pull ghcr.io/YOUR_USERNAME/cloudsaver:latest

# 拉取特定时间戳版本
docker pull ghcr.io/YOUR_USERNAME/cloudsaver:20241219-143022
```

## 包访问地址

发布成功后，可以在以下位置查看和管理你的包：
- https://github.com/YOUR_USERNAME?tab=packages

## 注意事项

1. 确保仓库有适当的权限设置
2. GitHub Packages存储有容量限制
3. 建议定期清理旧版本以节省空间
4. 公开包任何人都可以下载，私有包需要认证

## 故障排除

如果遇到问题，请检查：
1. GitHub Actions日志输出
2. 是否有足够的存储空间
3. 网络连接是否正常
4. 源镜像是否存在且可访问