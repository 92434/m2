#!/bin/bash

# ngrok远程访问完整解决方案
echo "🚇 ngrok远程访问系统启动中..."

# 安装必要组件
install_components() {
    echo "🔧 安装必要组件..."
    sudo apt-get update -qq
    sudo apt-get install -y \
        openssh-server \
        python3 python3-pip \
        curl wget jq \
        vim nano htop \
        net-tools
    
    # 安装Web终端
    sudo apt-get install -y ttyd
}

# 配置SSH服务
setup_ssh() {
    echo "🔐 配置SSH服务..."
    sudo systemctl start ssh
    sudo systemctl enable ssh
    
    # 显示SSH信息
    PUBLIC_IP=$(curl -s ifconfig.me)
    echo "🔑 SSH连接信息:"
    echo "  主机: $PUBLIC_IP"
    echo "  端口: 22"
    echo "  用户: $USER"
    echo "  命令: ssh $USER@$PUBLIC_IP"
}

# 安装和配置ngrok
setup_ngrok() {
    echo "🚇 安装ngrok..."
    
    # 下载ngrok
    if [ ! -f /usr/local/bin/ngrok ]; then
        wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
        tar -xzf ngrok-v3-stable-linux-amd64.tgz
        chmod +x ngrok
        sudo mv ngrok /usr/local/bin/
        rm ngrok-v3-stable-linux-amd64.tgz
    fi
    
    # 配置认证token（如果提供）
    if [ ! -z "$NGROK_AUTH_TOKEN" ]; then
        ngrok authtoken $NGROK_AUTH_TOKEN
        echo "✅ ngrok认证完成"
    fi
}

# 启动各种服务
start_services() {
    echo "🚀 启动服务..."
    
    # 启动Web终端 (ttyd)
    echo "🖥️ 启动Web终端..."
    ttyd -p 8080 bash > /tmp/ttyd.log 2>&1 &
    TTYD_PID=$!
    
    # 启动文件服务器
    echo "📁 启动文件服务器..."
    python3 -m http.server 8000 > /tmp/fileserver.log 2>&1 &
    FILE_PID=$!
    
    # 启动ngrok隧道
    echo "🚇 启动ngrok隧道..."
    ngrok start --all --config=./ngrok.yml > /tmp/ngrok-full.log 2>&1 &
    NGROK_PID=$!
    
    # 等待服务启动
    sleep 5
    
    # 获取访问地址
    get_access_urls
}

# 获取访问URL
get_access_urls() {
    echo "🌐 访问地址信息:"
    
    # 获取ngrok URLs
    sleep 3
    NGROK_API="http://localhost:4040/api/tunnels"
    
    if curl -s $NGROK_API > /dev/null 2>&1; then
        WEB_URL=$(curl -s $NGROK_API | jq -r '.tunnels[] | select(.name=="web-terminal") | .public_url')
        SSH_PORT=$(curl -s $NGROK_API | jq -r '.tunnels[] | select(.name=="ssh-access") | .public_url' | sed 's/tcp:\/\///')
        FILE_URL=$(curl -s $NGROK_API | jq -r '.tunnels[] | select(.name=="file-transfer") | .public_url')
        
        echo "  Web终端: $WEB_URL"
        echo "  SSH隧道: $SSH_PORT"
        echo "  文件传输: $FILE_URL"
    else
        echo "  ⚠️ 无法获取ngrok URL，请稍后手动检查"
        echo "  ngrok状态页面: http://localhost:4040"
    fi
    
    # 显示本地IP
    LOCAL_IP=$(hostname -I | awk '{print $1}')
    echo "  本地访问:"
    echo "    Web终端: http://$LOCAL_IP:8080"
    echo "    文件服务: http://$LOCAL_IP:8000"
}

# 显示系统信息
show_system_info() {
    echo "📋 系统信息:"
    echo "  CPU核心: $(nproc)"
    echo "  内存: $(free -h | awk '/^Mem:/ {print $2}')"
    echo "  磁盘可用: $(df -h / | awk 'NR==2 {print $4}')"
    echo "  当前目录: $(pwd)"
    echo "  用户: $(whoami)"
}

# 主函数
main() {
    echo "========================================"
    echo "🚇 ngrok远程访问系统"
    echo "========================================"
    
    install_components
    setup_ssh
    setup_ngrok
    start_services
    show_system_info
    
    echo "========================================"
    echo "✅ 远程访问系统已就绪!"
    echo "⏳ 系统将持续运行，按Ctrl+C退出"
    echo "========================================"
    
    # 保持脚本运行
    while true; do
        sleep 60
        # 可以在这里添加健康检查逻辑
    done
}

# 执行主函数
main