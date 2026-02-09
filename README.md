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

### 3. package-release.yml
**ZIP包发布工作流**，将整个项目打包成ZIP并创建GitHub Release。

**功能特性：**
- 自动打包项目文件为ZIP格式
- 创建带时间戳的版本号
- 生成GitHub Release并附加ZIP文件
- 提供30天的artifact保留期
- 完整的发布说明和元数据

### 4. quick-zip.yml
**快速ZIP打包工作流**，简洁高效的打包方案。

**功能特性：**
- 快速创建项目ZIP包
- 自动时间戳命名
- 上传为GitHub Artifact
- 可选创建Release

### 5. image-export.yml ⭐ **主要功能**
**Docker镜像导出工作流**，将Docker镜像打包成压缩包供下载。

**功能特性：**
- 自动拉取指定的Docker镜像
- 导出为.tar.gz格式
- 创建完整的使用说明包
- 生成GitHub Release
- 包含镜像元数据信息
- 简化的时间戳格式

### 6. simple-image-export.yml
**简化版镜像导出**，快速导出镜像的核心功能。

**功能特性：**
- 最小化操作步骤
- 快速导出和压缩
- 直接上传artifact
- 简洁的使用说明

### 7. tar-export.yml ⭐ **新功能**
**Tar格式镜像导出**，专门用于导出未压缩的tar格式镜像文件。

**功能特性：**
- 导出原始tar格式镜像文件
- 不进行额外压缩
- 包含详细的使用说明
- 生成GitHub Release
- 提供30天artifact保留期

### 8. simple-tar.yml
**简化版tar导出**，最基础的tar格式导出功能。

**功能特性：**
- 最简化的操作流程
- 直接导出tar文件
- 上传为artifact
- 无额外包装

## 使用方法

### 触发工作流

1. 访问仓库的 **Actions** 页面
2. 选择要运行的工作流
3. 点击 **Run workflow** 按钮
4. 根据需要配置参数

### 镜像导出参数说明

| 参数 | 描述 | 默认值 |
|------|------|--------|
| image_name | 要导出的镜像名称 | jiangrui1994/cloudsaver |
| image_tag | 镜像标签 | latest |
| package_name | 导出包名称 | cloudsaver-image |
| image | 完整镜像标识(名称:标签) | jiangrui1994/cloudsaver:latest |
| filename | 输出文件名(不含扩展名) | cloudsaver-image |

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

## 下载导出的镜像包

### 方法1：从GitHub Release下载
1. 访问仓库的 **Releases** 页面
2. 找到对应的image release
3. 下载附加的ZIP或.tar.gz文件

### 方法2：从Actions Artifacts下载
1. 访问 **Actions** 页面
2. 找到成功的workflow运行记录
3. 在右上角找到 **Artifacts** 部分
4. 下载对应的镜像包文件

## 使用导出的镜像包

### Tar格式镜像使用方法
```bash
# 加载tar格式镜像
docker load -i cloudsaver-image-20241219.tar

# 验证镜像
docker images | grep cloudsaver
```

### 压缩包格式使用方法
```bash
# 方法1：直接加载压缩包
docker load -i exported-image-20241219.tar.gz

# 方法2：先解压再加载
gunzip exported-image-20241219.tar.gz
docker load -i exported-image-20241219.tar
```

### 完整包使用方法
```bash
# 解压完整包
unzip cloudsaver-image-package.zip

# 查看内容
cd package_contents
cat README.md
cat image-info.txt

# 加载镜像
docker load -i *.tar.gz
```

## 包访问地址

- **Docker镜像**: https://github.com/YOUR_USERNAME?tab=packages
- **Release页面**: https://github.com/YOUR_USERNAME/REPO_NAME/releases
- **Packages页面**: https://github.com/YOUR_USERNAME?tab=packages&repo_name=PACKAGE_NAME

## 注意事项

1. 确保仓库有适当的权限设置
2. GitHub Packages存储有容量限制
3. 建议定期清理旧版本以节省空间
4. 公开包任何人都可以下载，私有包需要认证
5. ZIP包会自动排除.git等不需要的文件
6. 镜像包可能较大，请确保有足够的下载带宽

## 故障排除

### 常见问题及解决方案

#### 1. 时间戳不一致错误
**问题**: `cp: cannot stat 'filename': No such file or directory`

**原因**: 工作流中不同步骤使用了不同的时间戳变量

**解决方案**: 
- 已在最新版本中修复此问题
- 确保使用统一的时间戳变量
- 检查文件是否正确创建后再进行复制操作

#### 2. 文件未找到错误
**问题**: 导出的文件不存在

**解决方案**:
- 检查Docker镜像拉取是否成功
- 验证镜像名称和标签是否正确
- 查看工作流执行日志确认每步执行状态

#### 3. 权限不足错误
**问题**: 无法创建Release或上传artifact

**解决方案**:
- 确保仓库具有适当的GitHub Actions权限
- 检查工作流中的permissions设置
- 验证GitHub Token权限

#### 4. 存储空间不足
**问题**: 包文件过大无法上传

**解决方案**:
- 清理旧的artifacts和releases
- 考虑压缩级别优化
- 分批处理大型镜像

如果遇到其他问题，请检查：
1. GitHub Actions日志输出
2. 是否有足够的存储空间
3. 网络连接是否正常
4. 源镜像是否存在且可访问
5. 权限设置是否正确
6. Docker服务是否正常运行