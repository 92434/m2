#!/bin/bash

# OpenWrt构建调试和修复脚本

echo "🔧 OpenWrt构建问题诊断和修复"

# 1. 清理构建环境
echo "🧹 清理旧的构建缓存..."
make clean
rm -rf tmp/

# 2. 更新feeds
echo "🔄 更新feeds..."
./scripts/feeds update -a

# 3. 检查特定包的状态
echo "🔍 检查问题包的状态..."
PROBLEM_PACKAGES=(
    "pango"
    "sdl2" 
    "sdl2-mixer"
    "seatd"
    "spirv-headers"
    "spirv-tools"
    "vulkan-headers"
    "vulkan-loader"
    "wayland-utils"
    "wpebackend-fdo"
    "wpewebkit"
    "xkeyboard-config"
    "kmscube"
    "vkmark"
)

for pkg in "${PROBLEM_PACKAGES[@]}"; do
    echo "检查包: $pkg"
    if ./scripts/feeds search "$pkg" | grep -q "$pkg"; then
        echo "  ✓ 包存在"
    else
        echo "  ✗ 包不存在，可能需要额外的feed"
    fi
done

# 4. 尝试单独安装问题包
echo "📦 尝试安装问题包..."
for pkg in "${PROBLEM_PACKAGES[@]}"; do
    echo "安装: $pkg"
    ./scripts/feeds install "$pkg" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "  ✓ 安装成功"
    else
        echo "  ✗ 安装失败"
    fi
done

# 5. 重新生成配置
echo "⚙️ 重新生成配置..."
make defconfig

# 6. 检查配置冲突
echo "📋 检查配置选项..."
make menuconfig 2>/dev/null

echo "✅ 诊断完成，请检查上述输出确定具体问题"