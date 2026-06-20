# Spark Hermes / Telegram 运维快照（无密钥）
# 生成: 2026-06-20

## Telegram
- Bot: https://t.me/spark_yijzhu_bot
- 凭据: ~/.hermes/profiles/spark/.env → TELEGRAM_BOT_TOKEN, TELEGRAM_ALLOWED_USERS, TELEGRAM_HOME_CHANNEL
- 允许用户 ID: 5919515095
- 依赖: pip install 'python-telegram-bot[webhooks]>=22.6,<23'
- Gateway: systemctl status hermes-gateway-spark

## 主模型（与 CLI 一致）
- provider: xai-oauth
- model: grok-composer-2.5-fast
- base_url: https://api.x.ai/v1
- 勿将 Gateway 主模型改为 Agnes（仅 fallback/辅助）

## 常用
```bash
export HERMES_PROFILE=spark
hermes gateway status --system
hermes config show | grep -i telegram
sudo systemctl restart hermes-gateway-spark
tail -f ~/.hermes/profiles/spark/logs/gateway.log
```

## 日志
- gateway: ~/.hermes/profiles/spark/logs/gateway.log
- errors: ~/.hermes/profiles/spark/logs/errors.log