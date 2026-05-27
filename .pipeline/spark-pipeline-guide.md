# Spark GEO Pipeline — 文章推送规范

Spark（VPS Hermes）负责所有 GEO 文章的生产，本地不做。

## 文章格式

每篇 GEO 文章使用标准 Markdown + YAML frontmatter：

```yaml
---
layout: default
title: 文章标题
date: 2026-05-28
description: 文章摘要
tags:
  - ISO
permalink: /文章标题URL路径/
---
# 文章标题

正文内容...
```

**关键规则：**
1. **`permalink` 必填** — 必须是根路径 `/标题/` 格式，不要带目录前缀。Jekyll 会根据这个生成最终 URL
2. **`permalink` 末尾必须有 `/`** — 否则 Jekyll 处理成文件而非目录 URL
3. **`permalink` 不含文件路径前缀** — 例如 `permalink: /欧盟CBAM正式实施制造业能源数据管理体系升级路径/` 正确，`permalink: /iso50001/欧盟CBAM/` 错误（会导致双重路径）

## 文件存放规则

- 文章存在对应分类目录下：`ai-governance/`、`general/`、`iso9001/`、`iso14001/`、`iso27001/`、`iso45001/`、`iso50001/`
- 文件名 = 标题（不含特殊符号的简洁版），例如 `欧盟CBAM正式实施制造业能源数据管理体系升级路径.md`
- **文件名与 URL 无关** — URL 由 `permalink` 字段决定

## 推送流程

每写完一批文章后按顺序执行：

```bash
# 1. 生成 sitemap（必须！）
cd /path/to/ai-daily-brief-repo
python3 scripts/generate-sitemap.py

# 2. 提交 & 推送
git add -A
git commit -m "geo: 文章标题简述 [YYYY-MM-DD]"
git push origin master
```

## 验证

推送后验证 sitemap 所有 URL 是否 200：

```bash
python3 -c "
import re, urllib.request
with open('sitemap.xml') as f:
    urls = re.findall(r'<loc>(.*?)</loc>', f.read())
ok = sum(1 for u in urls if urllib.request.urlopen(urllib.request.Request(u), timeout=8).getcode() == 200)
print(f'OK: {ok}/{len(urls)}')
"
```

## 已知坑

- ❌ 不要自定义 frontmatter 的 `permalink` 中含目录路径（如 `/ai-governance/标题/`），Jekyll 会生成双重路径
- ❌ 不要漏掉 `permalink` 末尾的 `/`
- ❌ 不要把文件放根目录（根目录只放 index.md）
- ✅ Sitemap 生成脚本会自动读取每篇文章的 `permalink` 字段
