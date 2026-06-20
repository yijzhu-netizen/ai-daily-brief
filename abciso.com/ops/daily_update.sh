#!/bin/bash
# abcISO daily auto-update pipeline (optimized 2026-06-20)
# Steps: GEO convert → dedup → homepage → sync → git
# 行业动态新闻由 crontab 单独跑：北京 10:00、16:00（见 /var/log/abciso-news.log）
set -euo pipefail
cd /data/www/abciso.com
LOG="/var/log/abciso-daily.log"

log() { echo "[$(date '+%H:%M:%S')] $1" >> "$LOG"; }
echo "=== $(date) ===" >> "$LOG"

# 1. 转换GEO文章（仅今天新增的）
log "[1/6] convert_geo.py"
python3 convert_geo.py >> "$LOG" 2>&1 || log "  WARN: convert_geo failed"

# 3. GEO文章去重（删除相似度>0.6的旧文章）
log "[2/6] GEO dedup"
python3 -c "
import os, re, shutil
from datetime import datetime

def tokenize(text):
    return set(re.findall(r'[\u4e00-\u9fff]|[a-zA-Z]+', text.lower()))

def jaccard(a, b):
    sa, sb = tokenize(a), tokenize(b)
    if not sa or not sb: return 0.0
    return len(sa & sb) / len(sa | sb)

geo_dir = '/root/GEO文章/abciso.com/design/geo'
files = [f for f in os.listdir(geo_dir) if f.endswith('.html')]
titles = {}
for f in files:
    path = os.path.join(geo_dir, f)
    with open(path, encoding='utf-8', errors='ignore') as fh:
        head = fh.read(2000)
    m = re.search(r'<h1[^>]*>(.*?)</h1>', head)
    title = m.group(1).strip() if m else f.replace('.html','')
    titles[f] = title

dups = []
files_sorted = sorted(titles.keys(), key=lambda f: os.path.getmtime(os.path.join(geo_dir, f)))
seen = []
for f in files_sorted:
    t = titles[f]
    for s in seen:
        ratio = jaccard(t, titles[s])
        if ratio > 0.65:
            dups.append((f, s, ratio))
            break
    else:
        seen.append(f)

if dups:
    backup = '/root/geo-backup-' + datetime.now().strftime('%Y%m%d')
    os.makedirs(backup, exist_ok=True)
    for dup, kept, ratio in dups:
        src = os.path.join(geo_dir, dup)
        shutil.move(src, os.path.join(backup, dup))
        print(f'  DEDUP: {dup[:40]} (jaccard={ratio:.2f}, kept={kept[:40]})')
    print(f'  Removed {len(dups)} duplicates, backed up to {backup}')
else:
    print('  No duplicates found')
" >> "$LOG" 2>&1 || log "  WARN: dedup failed"

# 4. 更新首页精选文章（动态扫描最新3篇）
log "[3/6] update_index.py (dynamic)"
python3 /data/www/abciso.com/update_index.py >> "$LOG" 2>&1 || log "  WARN: update_index failed"

# 5. 同步文件到网站目录
log "[4/6] sync files to /data/www/abciso.com"
cp -r /root/GEO文章/abciso.com/design/geo/* /data/www/abciso.com/geo/ 2>> "$LOG" || true
cp /root/GEO文章/abciso.com/design/kb-list.html /data/www/abciso.com/kb-list.html 2>> "$LOG" || true
cp /root/GEO文章/abciso.com/design/news.html /data/www/abciso.com/news.html 2>> "$LOG" || true
cp /root/GEO文章/abciso.com/design/index.html /data/www/abciso.com/index.html 2>> "$LOG" || true
cp /root/GEO文章/abciso.com/design/sitemap.xml /data/www/abciso.com/sitemap.xml 2>> "$LOG" || true

# 6. 统计
GEO_COUNT=$(ls /data/www/abciso.com/geo/*.html 2>/dev/null | wc -l)
log "  GEO articles on site: $GEO_COUNT"

# 7. Git commit & push
log "[5/6] git push"
cd /root/GEO文章
git add -A
git commit -m "feat: daily update $(date +%Y%m%d)" --allow-empty >> "$LOG" 2>&1
git push origin master >> "$LOG" 2>&1 || log "  WARN: git push failed (PAT not configured?)"

log "[6/6] DONE"
echo "=== DONE ===" >> "$LOG"
