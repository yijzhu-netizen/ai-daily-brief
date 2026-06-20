# Spark → Sage / 本地 同步说明

> 最后更新: 2026-06-20

## Spark 上发布

改 **skill**、**站更脚本** 或 **本目录 ops 文档** 后，在 Spark VPS 执行：

```bash
bash /root/.hermes/profiles/spark/skills/devops/website-update-system/scripts/spark_publish.sh
```

### 产物

| 路径 | 内容 |
|------|------|
| `/root/网站备份/website-update-system_publish_*.tar.gz` | `website-update-system`、`abciso-knowledgebase-sync` 等 skill + `abciso.com/ops/` 快照 |
| `/root/网站备份/hermes-spark-ops_*.tar.gz` | Hermes 运维包：`HERMES_TELEGRAM_SPARK.md`、`config-show.txt`（脱敏）、`fallback-list.txt`、`hermes-gateway-spark.service`、`spark_vps_ops_report.sh` |
| `/mnt/e/网站备份/` | 若挂载 E 盘，与 Windows `E:\网站备份\` 对齐（发布脚本会尝试拷贝） |
| `abciso.com/ops/` | 进 **GEO git**；Sage `git pull` 可得 |

**密钥**：`.env`、Bot Token、API Key **不** 打入 tarball；仅保留在 `~/.hermes/profiles/spark/.env`。

## Sage 本机（在 Sage shell，非 Spark）

```bash
cd /path/to/GEO文章 && git pull

# skill 覆盖（从 E 盘或 VPS scp 的 tarball 解压）
cp -a /mnt/e/网站备份/website-update-system ~/.hermes/profiles/sage/skills/devops/
cp -a /mnt/e/网站备份/abciso-knowledgebase-sync ~/.hermes/profiles/sage/skills/web/
```

## 生产边界

- **站更 cron** 只在 Spark（见 `ops/spark_root_crontab.txt`）
- **不要**在 Sage / Windows 再开并行日更 cron
- **Telegram Gateway** 只在 Spark；Bot Token 单实例轮询

## 相关文档

- `HERMES_TELEGRAM_SPARK.md` — Telegram + Grok + fallback + 仅 Telegram Gateway
- `spark_root_crontab.txt` — root crontab 快照