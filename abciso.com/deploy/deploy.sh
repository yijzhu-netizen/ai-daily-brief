#!/bin/bash
# abciso.com 一键部署脚本
# 用法: ./deploy.sh [服务器IP]
# 需要: 远程服务器上已安装 nginx

set -e

SERVER="${1:-}"
if [ -z "$SERVER" ]; then
    echo "用法: ./deploy.sh <服务器IP>"
    echo "示例: ./deploy.sh 123.456.789.0"
    exit 1
fi

SITE_DIR="/var/www/abciso"
DESIGN_DIR="/mnt/e/GEO文章/abciso.com/design"
NGINX_CONF="/mnt/e/GEO文章/abciso.com/deploy/nginx.conf"

echo "🚀 开始部署 abciso.com → $SERVER"

# 1. 创建远程目录
echo "📁 创建远程目录..."
ssh root@$SERVER "mkdir -p $SITE_DIR"

# 2. 同步网站文件
echo "📦 同步文件..."
rsync -avz --delete \
    "$DESIGN_DIR/" \
    "root@$SERVER:$SITE_DIR/" \
    --exclude='*.png' \
    --exclude='*.py'

# 3. 上传 nginx 配置
echo "🔧 配置 nginx..."
scp "$NGINX_CONF" root@$SERVER:/etc/nginx/sites-available/abciso.com
ssh root@$SERVER "ln -sf /etc/nginx/sites-available/abciso.com /etc/nginx/sites-enabled/ && nginx -t && systemctl reload nginx"

# 4. 配置SSL (如果需要)
echo "🔒 如需HTTPS，运行:"
echo "    ssh root@$SERVER 'certbot --nginx -d abciso.com -d www.abciso.com'"

echo ""
echo "✅ 部署完成！"
echo "   访问: http://$SERVER"
echo "   如需域名解析，将 abciso.com A记录指向 $SERVER"
