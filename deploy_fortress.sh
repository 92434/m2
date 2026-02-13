#!/bin/bash
# ================================
# 🚀 数据要塞一键部署脚本
# 来自夜的命名术·壹的自动化部署
# ================================

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 全局变量
FORTRESS_HOME="/opt/night-fortress"
LOG_FILE="/var/log/fortress-deploy.log"
START_TIME=$(date +%s)

# 日志函数
log() {
    echo -e "${CYAN}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}[SUCCESS] $1${NC}" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}" | tee -a "$LOG_FILE"
}

# 检查root权限
check_root() {
    if [[ $EUID -ne 0 ]]; then
        error "此脚本需要root权限运行"
        exit 1
    fi
    success "权限检查通过"
}

# 检查系统环境
check_environment() {
    log "🔍 检查系统环境..."
    
    # 检查操作系统
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        log "操作系统: $NAME $VERSION"
    else
        warning "无法确定操作系统版本"
    fi
    
    # 检查Python版本
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        log "Python版本: $PYTHON_VERSION"
    else
        error "未找到Python3，请先安装Python3"
        exit 1
    fi
    
    # 检查必要软件包
    local required_packages=("curl" "wget" "git" "vim")
    for package in "${required_packages[@]}"; do
        if ! command -v "$package" &> /dev/null; then
            warning "缺少软件包: $package"
        fi
    done
    
    success "环境检查完成"
}

# 创建要塞目录结构
create_directory_structure() {
    log "📁 创建要塞目录结构..."
    
    mkdir -p "$FORTRESS_HOME"/{bin,config,data,logs,backup,scripts,tmp}
    mkdir -p /var/log/fortress
    
    # 设置权限
    chown -R root:root "$FORTRESS_HOME"
    chmod 755 "$FORTRESS_HOME"
    chmod 700 "$FORTRESS_HOME"/config
    chmod 700 "$FORTRESS_HOME"/backup
    
    success "目录结构创建完成"
    log "要塞根目录: $FORTRESS_HOME"
}

# 安装Python依赖
install_python_dependencies() {
    log "🐍 安装Python依赖..."
    
    # 创建虚拟环境
    python3 -m venv "$FORTRESS_HOME/venv"
    
    # 激活虚拟环境并安装依赖
    source "$FORTRESS_HOME/venv/bin/activate"
    
    pip install --upgrade pip
    pip install pyyaml cryptography psutil
    
    deactivate
    success "Python依赖安装完成"
}

# 部署配置文件
deploy_config_files() {
    log "⚙️ 部署配置文件..."
    
    # 复制配置文件
    if [[ -f "data_fortress_config.yaml" ]]; then
        cp data_fortress_config.yaml "$FORTRESS_HOME/config/"
        success "主配置文件部署完成"
    else
        warning "未找到主配置文件 data_fortress_config.yaml"
    fi
    
    # 创建系统服务配置
    cat > /etc/systemd/system/fortress-guardian.service << EOF
[Unit]
Description=Night Fortress Guardian
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$FORTRESS_HOME
ExecStart=$FORTRESS_HOME/venv/bin/python3 fortress_guardian.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    success "系统服务配置完成"
}

# 部署守护进程
deploy_guardian() {
    log "🛡️ 部署守护进程..."
    
    # 复制守护进程脚本
    if [[ -f "fortress_guardian.py" ]]; then
        cp fortress_guardian.py "$FORTRESS_HOME/"
        chmod +x "$FORTRESS_HOME/fortress_guardian.py"
        success "守护进程部署完成"
    else
        error "未找到守护进程脚本 fortress_guardian.py"
        exit 1
    fi
    
    # 复制控制台脚本
    if [[ -f "fortress_console.py" ]]; then
        cp fortress_console.py "$FORTRESS_HOME/bin/"
        chmod +x "$FORTRESS_HOME/bin/fortress_console.py"
        success "控制台程序部署完成"
    fi
}

# 配置防火墙
configure_firewall() {
    log "🔥 配置防火墙规则..."
    
    if command -v ufw &> /dev/null; then
        # UFW防火墙配置
        ufw allow 8443/tcp  # 主要访问端口
        ufw allow 2222/tcp  # 管理端口
        ufw --force enable
        success "UFW防火墙配置完成"
    elif command -v firewall-cmd &> /dev/null; then
        # Firewalld配置
        firewall-cmd --permanent --add-port=8443/tcp
        firewall-cmd --permanent --add-port=2222/tcp
        firewall-cmd --reload
        success "Firewalld防火墙配置完成"
    else
        warning "未检测到支持的防火墙工具"
    fi
}

# 启动服务
start_services() {
    log "🚀 启动要塞服务..."
    
    # 重新加载systemd配置
    systemctl daemon-reload
    
    # 启动守护进程
    systemctl enable fortress-guardian
    systemctl start fortress-guardian
    
    # 检查服务状态
    if systemctl is-active --quiet fortress-guardian; then
        success "要塞守护进程启动成功"
    else
        error "要塞守护进程启动失败"
        systemctl status fortress-guardian
        exit 1
    fi
}

# 创建管理脚本
create_management_scripts() {
    log "🔧 创建管理脚本..."
    
    # 创建启动脚本
    cat > "$FORTRESS_HOME/bin/start_fortress.sh" << 'EOF'
#!/bin/bash
systemctl start fortress-guardian
echo "要塞系统已启动"
EOF
    
    # 创建停止脚本
    cat > "$FORTRESS_HOME/bin/stop_fortress.sh" << 'EOF'
#!/bin/bash
systemctl stop fortress-guardian
echo "要塞系统已停止"
EOF
    
    # 创建状态检查脚本
    cat > "$FORTRESS_HOME/bin/status_fortress.sh" << 'EOF'
#!/bin/bash
echo "=== 数据要塞状态报告 ==="
echo "时间: $(date)"
echo "守护进程状态: $(systemctl is-active fortress-guardian)"
echo "运行时间: $(systemctl show fortress-guardian -p ActiveEnterTimestamp --value)"
echo ""
echo "系统资源使用:"
echo "CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%"
echo "内存: $(free | grep Mem | awk '{printf("%.1f%%", $3/$2 * 100.0)}')"
echo "磁盘: $(df -h / | awk 'NR==2{print $5}')"
EOF
    
    # 设置执行权限
    chmod +x "$FORTRESS_HOME"/bin/*.sh
    success "管理脚本创建完成"
}

# 显示部署完成信息
show_completion_info() {
    local END_TIME=$(date +%s)
    local DURATION=$((END_TIME - START_TIME))
    
    echo
    echo -e "${PURPLE}================================${NC}"
    echo -e "${PURPLE}     🏰 数据要塞部署完成 🏰${NC}"
    echo -e "${PURPLE}================================${NC}"
    echo
    echo -e "${GREEN}部署位置: $FORTRESS_HOME${NC}"
    echo -e "${GREEN}部署耗时: ${DURATION}秒${NC}"
    echo
    echo -e "${YELLOW}管理命令:${NC}"
    echo "  启动要塞: $FORTRESS_HOME/bin/start_fortress.sh"
    echo "  停止要塞: $FORTRESS_HOME/bin/stop_fortress.sh"
    echo "  查看状态: $FORTRESS_HOME/bin/status_fortress.sh"
    echo "  控制台界面: $FORTRESS_HOME/bin/fortress_console.py"
    echo
    echo -e "${BLUE}日志文件: /var/log/fortress-deploy.log${NC}"
    echo -e "${BLUE}服务状态: systemctl status fortress-guardian${NC}"
    echo
    echo -e "${CYAN}来自夜的命名术·壹的数字堡垒${NC}"
    echo
}

# 主函数
main() {
    clear
    echo -e "${PURPLE}"
    echo "================================"
    echo "   🏰 数据要塞自动部署系统 🏰"
    echo "    来自夜的命名术·壹"
    echo "================================"
    echo -e "${NC}"
    
    # 检查参数
    if [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
        echo "用法: $0 [选项]"
        echo "选项:"
        echo "  --help, -h    显示帮助信息"
        echo "  --dry-run     预演模式，不实际执行"
        exit 0
    fi
    
    # 如果是预演模式
    if [[ "$1" == "--dry-run" ]]; then
        echo -e "${YELLOW}预演模式 - 将显示将要执行的操作${NC}"
        echo "要塞将被部署到: $FORTRESS_HOME"
        echo "需要安装的软件包: python3, pyyaml, cryptography, psutil"
        echo "将创建的服务: fortress-guardian"
        exit 0
    fi
    
    # 执行部署步骤
    check_root
    check_environment
    create_directory_structure
    install_python_dependencies
    deploy_config_files
    deploy_guardian
    configure_firewall
    create_management_scripts
    start_services
    show_completion_info
}

# 错误处理
trap 'error "部署过程中发生错误，查看日志: $LOG_FILE"' ERR

# 执行主函数
main "$@"