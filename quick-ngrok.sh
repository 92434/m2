#!/bin/bash

# 快速ngrok远程访问脚本
echo "⚡ 快速启动ngrok远程访问..."

# 快速安装ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar -xzf ngrok-v3-stable-linux-amd64.tgz
chmod +x ngrok
sudo mv ngrok /usr/local/bin/

# 启动SSH
sudo systemctl start ssh

# 启动Web终端
sudo apt-get install -y ttyd
ttyd -p 8080 bash &

# 启动ngrok HTTP隧道
ngrok http 8080 &

# 显示连接信息
sleep 3
PUBLIC_URL=$(curl -s localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')
echo "🌐 Web终端地址: $PUBLIC_URL"
echo "🔑 SSH地址: ssh runner@$(curl -s ifconfig.me)"

echo "✅ ngrok远程访问已启动!"