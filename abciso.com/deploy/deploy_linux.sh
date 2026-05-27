#!/bin/bash
set -e
SERVER="161.153.39.190"
SITE_DIR="/var/www/abciso"
DESIGN_DIR="/root/GEO文章/abciso.com/design"
NGINX_CONF="/root/GEO文章/abciso.com/deploy/nginx.conf"
SSH_OPTS="-o StrictHostKeyChecking=no"

echo "🚀 开始部署 abciso.com → $SERVER"

echo "📁 创建远程目录..."
ssh $SSH_OPTS root@$SERVER "mkdir -p $SITE_DIR"

echo "📦 同步文件..."
rsync -avz --delete -e "ssh $SSH_OPTS" \
    "$DESIGN_DIR/" \
    "root@$SERVER:$SITE_DIR/" \
    --exclude='*.png' \
    --exclude='*.py'

echo "🔧 配置 nginx..."
scp $SSH_OPTS "$NGINX_CONF" root@$SERVER:/etc/nginx/sites-available/abciso.com
ssh $SSH_OPTS root@$SERVER "ln -sf /etc/nginx/sites-available/abciso.com /etc/nginx/sites-enabled/ && nginx -t && systemctl reload nginx"

echo "✅ 部署完成！"
echo "   访问: http://$SERVER"
