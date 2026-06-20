# Spark Hermes / Telegram 运维说明（无密钥）

> 最后更新: 2026-06-20 · Profile: `spark` · 主机: Spark VPS

## Telegram

- Bot: https://t.me/spark_yijzhu_bot
- 凭据: `~/.hermes/profiles/spark/.env` → `TELEGRAM_BOT_TOKEN`, `TELEGRAM_ALLOWED_USERS`, `TELEGRAM_HOME_CHANNEL`
- 允许用户 ID: **5919515095**
- 依赖: `pip install --break-system-packages 'python-telegram-bot[webhooks]>=22.6,<23'`
- 服务: `systemctl status hermes-gateway-spark`

## Gateway：仅 Telegram

| 项 | 值 |
|----|-----|
| `plugins.disabled` | `photon-platform` |
| `photon.enabled` / `platforms.photon.enabled` | `false` |
| `telegram.enabled` | `true` |
| 活跃 `.env` | **不含** `PHOTON_*` |
| Photon 凭据备份 | `~/.hermes/profiles/spark/.env.photon.backup` |

重启后日志应出现：`Gateway running with **1** platform(s)`，且仅有 `telegram connected`。

**恢复 iMessage（以后）**

1. 将 `.env.photon.backup` 中的 `PHOTON_*` 写回 `.env`
2. `hermes config set` 去掉 `plugins.disabled` 中的 `photon-platform`（或 `plugins.disabled: []`）
3. `photon.enabled` / `platforms.photon.enabled` → `true`
4. `sudo systemctl restart hermes-gateway-spark`

## 主模型与 Fallback

| 角色 | Provider | Model |
|------|----------|-------|
| 主（CLI + Gateway） | `xai-oauth` | `grok-composer-2.5-fast` |
| Fallback 链 | `custom:Agnes` | `agnes-2.0-flash` |

```bash
export HERMES_PROFILE=spark
hermes fallback list
```

配置写在 `config.yaml` 顶层 `fallback_providers`（Grok 限流/5xx 时自动切 Agnes）。

## Hermes 技能（Spark）

- 统一入口: **`hermes-agent-configuration`**（已合并原 `xai-grok-oauth-setup`、`hermes-xai-grok-setup`）
- VPS 快照: **`spark-vps-ops`**
- 站更: **`website-update-system`**、`abciso-knowledgebase-sync`

## 定时任务

- Hermes cron `81ed944b1972`：北京 **09:00 / 21:00** 运维简报 → `telegram:5919515095`
- 脚本: `/usr/local/bin/spark_vps_ops_report.sh`（`HERMES_PROFILE=spark`）

## 常用命令

```bash
export HERMES_PROFILE=spark
hermes gateway status --system
hermes config show | grep -iE 'telegram|fallback|photon'
sudo systemctl restart hermes-gateway-spark
tail -f ~/.hermes/profiles/spark/logs/gateway.log
```

## 日志

- `~/.hermes/profiles/spark/logs/gateway.log`
- `~/.hermes/profiles/spark/logs/errors.log`

## 备份包（无 Token）

Spark 上生成：

```bash
# 站更 + skills
bash ~/.hermes/profiles/spark/skills/devops/website-update-system/scripts/spark_publish.sh
# Hermes ops 快照（config-show 脱敏、systemd、本说明）
# 见 /root/网站备份/hermes-spark-ops_*.tar.gz
```

凭据 **不** 进 Git / tarball；恢复机器需保留本机 `.env` 或 BotFather 重新取 Token。