#!/bin/bash
# abciso.com 部署脚本
# 用法：在 VPS 上执行
set -e

SITE_DIR="/var/www/abciso.com"
DESIGN_SRC="/mnt/e/GEO文章/abciso.com/design"
NGINX_CONF="/etc/nginx/sites-available/abciso.com"

echo "=== 部署 abciso.com ==="

# 1. 创建目录
sudo mkdir -p $SITE_DIR

# 2. 复制文件（排除原始PNG备份）
sudo rsync -av --exclude='*.png' "$DESIGN_SRC/" "$SITE_DIR/"

# 3. 设置权限
sudo chown -R www-data:www-data $SITE_DIR
sudo find $SITE_DIR -type f -exec chmod 644 {} \;

# 4. Nginx配置
sudo cp /mnt/e/GEO文章/abciso.com/abciso.nginx.conf $NGINX_CONF
sudo ln -sf $NGINX_CONF /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# 5. SSL证书（需要先解析域名到本机）
if ! [ -f /etc/letsencrypt/live/abciso.com/fullchain.pem ]; then
    echo "→ 请先解析域名到本机，然后执行："
    echo "  sudo certbot --nginx -d abciso.com -d www.abciso.com"
fi

echo ""
echo "✅ 部署完成！"
echo "   站点: https://abciso.com"
echo "   目录: $SITE_DIR"
