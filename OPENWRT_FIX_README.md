# 🛠️ OpenWrt构建问题修复指南

## 问题描述
在OpenWrt构建过程中遇到以下错误：
```
Collecting package info: feeds/video/libs/pango
...
Error: Process completed with exit code 1.
```

## 解决方案

### 方案1：使用自动化修复脚本

```bash
# 下载并运行修复脚本
chmod +x fix-package-collection.sh
./fix-package-collection.sh
```

### 方案2：通过GitHub Actions诊断

1. 推送代码到GitHub
2. 在Actions页面运行"🛠️ OpenWrt构建调试与修复"工作流
3. 查看详细的构建日志和诊断信息

### 方案3：手动修复步骤

```bash
# 1. 清理环境
make dirclean
rm -rf tmp/ logs/ bin/

# 2. 更新feeds
./scripts/feeds update -a
./scripts/feeds install -a

# 3. 检查问题包
find feeds/ -name "*pango*" -o -name "*sdl2*"

# 4. 创建最小化配置
make menuconfig  # 手动禁用问题包

# 5. 重新构建
make defconfig
make V=s
```

## 常见原因

1. **包依赖冲突** - 某些包之间存在版本冲突
2. **Feed配置问题** - video feed可能未正确配置
3. **网络问题** - 包下载失败
4. **配置错误** - .config文件包含冲突选项

## 调试技巧

```bash
# 查看详细构建日志
make V=s 2>&1 | tee build.log

# 检查特定包
make package/feeds/video/pango/compile V=s

# 验证配置
make prereq
```

## 预防措施

1. 定期更新feeds
2. 使用稳定的OpenWrt版本
3. 逐步添加包而不是一次性配置很多包
4. 保持良好的版本控制习惯

---
如需进一步帮助，请提供完整的构建日志。