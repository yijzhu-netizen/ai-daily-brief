# Spark → Sage / 本地 同步说明（2026-06-20）

Spark 上改 skill 或站更脚本后，在 VPS 执行：

```bash
bash /root/.hermes/profiles/spark/skills/devops/website-update-system/scripts/spark_publish.sh
```

产物：
- `/root/网站备份/website-update-system`（最新 skill）
- `/mnt/e/网站备份/`（若 VPS 挂载了 E 盘，与 Windows `E:\网站备份\` 对齐）
- `abciso.com/ops/` 本目录进 GEO git，Sage `git pull` 可得

Sage 本机（在 **Sage** shell，非 Spark）：

```bash
# 若从 GitHub 拉 ops
cd /path/to/GEO文章 && git pull

# skill 覆盖（从 E 盘备份或从 VPS scp tarball 解压）
cp -a /mnt/e/网站备份/website-update-system ~/.hermes/profiles/sage/skills/devops/
cp -a /mnt/e/网站备份/abciso-knowledgebase-sync ~/.hermes/profiles/sage/skills/web/
```

**不要**在 Sage 再开站更 cron；生产只在 Spark `ops/spark_root_crontab.txt`。