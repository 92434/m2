#!/bin/bash

# 专门修复包收集问题的脚本

echo "🔧 修复OpenWrt包收集问题"

# 1. 检查当前目录
if [ ! -f "Makefile" ] || [ ! -d "scripts" ]; then
    echo "❌ 错误: 请在OpenWrt源码根目录运行此脚本"
    exit 1
fi

# 2. 备份当前配置
echo "💾 备份当前配置..."
cp .config .config.backup 2>/dev/null || echo "无现有配置需要备份"

# 3. 清理环境
echo "🧹 清理构建环境..."
make dirclean
rm -rf tmp/ logs/ bin/

# 4. 更新feeds（详细模式）
echo "🔄 更新feeds（详细模式）..."
./scripts/feeds update -v

# 5. 检查video feed状态
echo "🔍 检查video feed..."
if [ -d "feeds/video" ]; then
    echo "✓ video feed存在"
    ls -la feeds/video/libs/ | head -10
else
    echo "✗ video feed不存在，尝试重新安装"
    ./scripts/feeds install video
fi

# 6. 单独处理问题包
PROBLEMATIC_PACKAGES=(
    "libs/pango"
    "libs/sdl2"
    "libs/sdl2-mixer"
    "libs/seatd"
    "libs/spirv-headers"
    "libs/spirv-tools"
    "libs/vulkan-headers"
    "libs/vulkan-loader"
    "libs/wayland-utils"
    "libs/wpebackend-fdo"
    "libs/wpewebkit"
    "libs/xkeyboard-config"
    "utils/kmscube"
    "utils/vkmark"
)

echo "📦 处理问题包..."
for pkg in "${PROBLEMATIC_PACKAGES[@]}"; do
    echo "处理: $pkg"
    if [ -d "feeds/video/$pkg" ]; then
        echo "  ✓ 包目录存在"
        # 检查Makefile
        if [ -f "feeds/video/$pkg/Makefile" ]; then
            echo "  ✓ Makefile存在"
        else
            echo "  ✗ Makefile缺失"
        fi
    else
        echo "  ✗ 包目录不存在"
    fi
done

# 7. 尝试最小化配置
echo "⚙️ 创建最小化配置..."
cat > .config << 'EOF'
# 基础系统配置
CONFIG_TARGET_x86=y
CONFIG_TARGET_x86_64=y
CONFIG_TARGET_x86_64_Generic=y

# 基础包
CONFIG_PACKAGE_busybox=y
CONFIG_PACKAGE_dropbear=y
CONFIG_PACKAGE_firewall=y
CONFIG_PACKAGE_dnsmasq=y
CONFIG_PACKAGE_ip6tables=y
CONFIG_PACKAGE_iptables=y
CONFIG_PACKAGE_ppp=y
CONFIG_PACKAGE_ppp-mod-pppoe=y

# 禁用问题包
# CONFIG_PACKAGE_libpango=n
# CONFIG_PACKAGE_libsdl2=n
# CONFIG_PACKAGE_libsdl2-mixer=n
EOF

# 8. 重新配置
echo "🔄 重新配置..."
make defconfig

# 9. 测试基本构建
echo "🧪 测试基本构建..."
timeout 300 make prepare 2>&1 | tee prepare.log

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo "✅ 基本配置成功"
else
    echo "❌ 基本配置失败，查看prepare.log了解详情"
fi

echo "🔧 修复脚本执行完成"
echo "💡 建议:"
echo "1. 查看prepare.log了解具体错误"
echo "2. 逐步添加需要的包到.config"
echo "3. 如果问题持续，考虑更新OpenWrt版本"