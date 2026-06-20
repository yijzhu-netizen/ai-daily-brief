# Spark Hermes / Telegram 运维快照（无密钥）
# 生成: 2026-06-20

## Telegram
- Bot: https://t.me/spark_yijzhu_bot
- 凭据: ~/.hermes/profiles/spark/.env → TELEGRAM_BOT_TOKEN, TELEGRAM_ALLOWED_USERS, TELEGRAM_HOME_CHANNEL
- 允许用户 ID: 5919515095
- 依赖: pip install 'python-telegram-bot[webhooks]>=22.6,<23'
- Gateway: systemctl status hermes-gateway-spark
## 仅 Telegram（关闭 Photon）

- `plugins.disabled`: `photon-platform`
- `photon.enabled` / `platforms.photon.enabled`: false
- 活跃 `.env` 不含 `PHOTON_*`；恢复 iMessage 时从 `~/.hermes/profiles/spark/.env.photon.backup` 写回
- 重启后日志：`Gateway running with 1 platform(s)`，仅 `telegram connected`

## 主模型与 Fallback

- 主：`xai-oauth` + `grok-composer-2.5-fast`
- `fallback_providers`：`custom:Agnes` + `agnes-2.0-flash`（`hermes fallback list`）

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