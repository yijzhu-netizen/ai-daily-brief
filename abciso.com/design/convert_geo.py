#!/usr/bin/env python3
"""Convert all GEO markdown articles to local HTML pages under geo/ dir."""

import os, re, sys, subprocess, glob
from datetime import datetime
import markdown

GEO_DIR = "/root/GEO文章"
DESIGN_DIR = "/root/GEO文章/abciso.com/design"
GEO_OUT = os.path.join(DESIGN_DIR, "geo")
VPS = "root@161.153.39.190:/var/www/abciso/"

NAVBAR_HTML = """\
    <div class="container">
      <div class="nav-inner">
        <a href="index.html" class="nav-logo">abcISO<span>.com</span></a>
        <button class="nav-toggle" aria-label="菜单" onclick="document.querySelector('.nav-links').classList.toggle('open')">☰</button>
        <ul class="nav-links">
          <li><a href="../index.html">首页</a></li>
          <li><a href="../news.html">行业动态</a></li>
          <li><a href="../course.html" class="cta">课程 →</a></li>
          <li><a href="../books/">著作</a></li>
          <li class="dropdown">
            <span class="dropdown-label">知识库</span>
            <div class="dropdown-menu">
              <a href="../kb-list.html#iso9001">ISO 9001 质量管理</a>
              <a href="../kb-list.html#iso14001">ISO 14001 环境管理</a>
              <a href="../kb-list.html#iso45001">ISO 45001 职业健康安全</a>
              <a href="../kb-list.html#iso50001">ISO 50001 能源管理</a>
              <a href="../kb-list.html#iso27001">ISO 27001 信息安全</a>
              <a href="../kb-list.html#food-safety">食品安全</a>
              <a href="../kb-list.html#iatf16949">IATF 16949 汽车质量</a>
              <a href="../kb-list.html#ai-governance">AI 治理与合规</a>
              <a href="../kb-list.html#general">综合管理</a>
            </div>
          </li>
          <li><a href="../download.html">资料下载</a></li>
          <li><a href="/chat/" target="_blank" style="color:#3B82F6;font-weight:600">🤖 AI助手</a></li>
        </ul>
      </div>
    </div>"""

FOOTER_HTML = """\
  <footer class="footer">
    <div class="container">
      <div class="footer-brand">abcISO<span>.com</span></div>
      <p>制造业管理与ISO认证体系实操知识库 · 让管理体系不再纸上谈兵</p>
    </div>
  </footer>"""

CSS_ARTICLE = """
/* ===== Reset & Base ===== */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{font-size:16px;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif;font-size:16px;line-height:1.6;color:#111827;background:#fff;}
h1,h2,h3,h4{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif;font-weight:600;color:#111827;line-height:1.25}
h1{font-size:2rem}h2{font-size:1.5rem}h3{font-size:1.25rem}h4{font-size:1rem}
.container{max-width:820px;margin:0 auto;padding:0 1.5rem}

/* Nav */
.nav{position:sticky;top:0;z-index:100;background:rgba(255,255,255,.96);backdrop-filter:blur(8px);border-bottom:1px solid #f0f0f0}
.nav-inner{display:flex;align-items:center;justify-content:space-between;height:3.5rem}
.nav-logo{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif;font-size:1.25rem;font-weight:700;color:#3B82F6;text-decoration:none;display:flex;align-items:center;gap:.5rem}
.nav-logo span{color:#8B5CF6}
.nav-links{display:flex;align-items:center;gap:2rem;list-style:none}
.nav-links a{font-size:.875rem;font-weight:500;color:#4b5563;text-decoration:none;transition:color .2s;position:relative}
.nav-links a:hover{color:#3B82F6}
.nav-links a.cta{display:inline-flex;align-items:center;gap:.375rem;background:#3B82F6;color:#fff;padding:.5rem 1.25rem;border-radius:6px;font-weight:600;font-size:.875rem;transition:background .2s}
.nav-links a.cta:hover{background:#2563EB;color:#fff}
.nav-links .dropdown{position:relative;cursor:pointer}
.nav-links .dropdown-label{font-size:.875rem;font-weight:500;color:#4b5563;display:flex;align-items:center;gap:.25rem;padding:.25rem 0}
.nav-links .dropdown-label::after{content:"▼";font-size:.625rem;margin-left:.125rem;transition:transform .2s}
.nav-links .dropdown:hover .dropdown-label::after{transform:rotate(180deg)}
.nav-links .dropdown-menu{position:absolute;top:100%;left:50%;transform:translateX(-50%);background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:.5rem 0;min-width:180px;opacity:0;visibility:hidden;transition:all .2s;box-shadow:0 8px 24px rgba(0,0,0,.08)}
.nav-links .dropdown:hover .dropdown-menu{opacity:1;visibility:visible}
.nav-links .dropdown-menu a{display:block;padding:.5rem 1.25rem;font-size:.875rem;white-space:nowrap}
.nav-links .dropdown-menu a:hover{background:#f3f4f6;color:#3B82F6}
.nav-toggle{display:none;background:none;border:none;font-size:1.5rem;color:#111827;cursor:pointer;padding:.25rem}
@media(max-width:700px){
  .nav-links{display:none;position:absolute;top:3.5rem;left:0;right:0;background:#fff;border-bottom:1px solid #f0f0f0;flex-direction:column;padding:1rem 1.5rem;gap:1rem;align-items:stretch}
  .nav-links.open{display:flex}
  .nav-toggle{display:block}
  .nav-links .dropdown-menu{position:static;opacity:1;visibility:visible;box-shadow:none;border:none;padding-left:1rem;min-width:auto;transform:none}
}

/* Breadcrumb */
.breadcrumb{padding:1.5rem 0 0;font-size:.875rem;color:#6b7280}
.breadcrumb a{color:#3B82F6;text-decoration:none}
.breadcrumb a:hover{text-decoration:underline}
.breadcrumb .sep{margin:0 .5rem;color:#9ca3af}

/* Article Header */
.article-header{padding:2rem 0 1.5rem}
.article-header h1{font-size:2rem;line-height:1.3;margin-bottom:1rem}
.article-meta{display:flex;flex-wrap:wrap;gap:1rem;font-size:.875rem;color:#6b7280;align-items:center}
.article-meta span{display:inline-flex;align-items:center;gap:.25rem}
.article-tags{display:flex;flex-wrap:wrap;gap:.5rem;margin-bottom:1rem}
.article-tags .tag{font-size:.75rem;font-weight:600;padding:.125rem .625rem;border-radius:4px;background:#eff6ff;color:#3B82F6}
.article-tags .tag.green{background:#ecfdf5;color:#047857}
.article-tags .tag.purple{background:#f5f3ff;color:#6D28D9}
.article-tags .tag.amber{background:#fffbeb;color:#b45309}
.article-tags .tag.pink{background:#fce7f3;color:#be185d}

/* Article Body */
.article-body{padding:0 0 3rem}
.article-body h2{font-size:1.5rem;margin:2rem 0 .75rem;padding-bottom:.5rem;border-bottom:1px solid #f0f0f0}
.article-body h3{font-size:1.2rem;margin:1.5rem 0 .5rem}
.article-body h2:first-child{margin-top:0}
.article-body p{margin-bottom:1rem;line-height:1.8;color:#374151}
.article-body strong{font-weight:600;color:#111}
.article-body ul,.article-body ol{margin:0 0 1rem 1.5rem}
.article-body li{margin-bottom:.375rem;line-height:1.7;color:#374151}
.article-body li::marker{color:#3B82F6}
.article-body blockquote{margin:1.5rem 0;padding:1rem 1.5rem;border-left:4px solid #3B82F6;background:#f8fafc;border-radius:0 8px 8px 0;color:#374151}
.article-body blockquote p:last-child{margin-bottom:0}
.article-body code{font-size:.875rem;background:#f3f4f6;padding:.125rem .375rem;border-radius:4px;font-family:'Consolas','Courier New',monospace}
.article-body pre{margin:1rem 0;padding:1rem;background:#1f2937;color:#e5e7eb;border-radius:8px;overflow-x:auto;font-size:.875rem;line-height:1.5}
.article-body pre code{background:none;padding:0;color:inherit}
.article-body hr{margin:2rem 0;border:none;border-top:1px solid #f0f0f0}
.article-body table{width:100%;border-collapse:collapse;margin:1rem 0 1.5rem;font-size:.875rem}
.article-body th{background:#f8fafc;padding:.625rem .875rem;text-align:left;font-weight:600;border:1px solid #e5e7eb}
.article-body td{padding:.5rem .875rem;border:1px solid #e5e7eb;color:#374151}
.article-body tr:nth-child(even){background:#fafbfc}
.article-body a{color:#3B82F6;text-decoration:none}
.article-body a:hover{text-decoration:underline}

/* Footer */
.footer{padding:2.5rem 0;border-top:1px solid #f0f0f0;text-align:center}
.footer p{font-size:.875rem;color:#6b7280}
.footer .footer-brand{font-family:'Poppins',sans-serif;font-weight:700;color:#3B82F6;font-size:1.125rem;margin-bottom:.5rem}
.footer .footer-brand span{color:#8B5CF6}
"""


def slugify(title):
    """Create a URL-safe filename from title."""
    s = title.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s[:80]


def parse_front_matter(content):
    """Parse front matter: standard YAML, JSON, or fenced YAML code block."""
    DQ = chr(34)  # double quote
    SQ = chr(39)  # single quote
    
    # 1. Standard YAML (--- ... ---)
    m = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if m:
        fm = {}
        for line in m.group(1).split("\n"):
            line = line.strip()
            if ":" in line and not line.startswith("#"):
                key, _, val = line.partition(":")
                val = val.strip().strip(DQ).strip(SQ)
                fm[key.strip()] = val
        if fm:
            return fm, content[m.end():]
    
    # 2. JSON format ({ ... })
    m = re.match(r"^\{.*\}", content.strip(), re.DOTALL)
    if m:
        try:
            import json
            cleaned = content.strip()
            # Remove trailing } if present
            if cleaned.endswith("}"):
                cleaned = cleaned[:-1]
            if cleaned.startswith("{"):
                cleaned = cleaned[1:]
            fm = json.loads("{" + cleaned + "}")
            return fm, content[len(content.strip()):].lstrip("\n")
        except:
            pass
    
    # 3. Fenced YAML code block (```yaml ... ```)
    m = re.search(r"```(?:yaml|yml)\n(.*?)\n```", content, re.DOTALL)
    if m:
        fm = {}
        for line in m.group(1).split("\n"):
            line = line.strip()
            if ":" in line:
                key, _, val = line.partition(":")
                val = val.strip().strip(DQ).strip(SQ)
                fm[key.strip()] = val
        if fm:
            return fm, content[m.end():].lstrip("\n")
    
    return {}, content


def extract_meta_from_body(content, fname):
    """Extract title, date, desc, tags from markdown body when no front matter."""
    title = ""
    date_str = ""
    description = ""
    tags = []
    
    lines = content.split("\n")
    for line in lines:
        if not title and line.startswith("# "):
            title = line[2:].strip()
        if not date_str:
            dm = re.search(r"更新日期[：:]\s*(\d{4}-\d{2}-\d{2})", line)
            if dm:
                date_str = dm.group(1)
        if not description and line.strip() and not line.startswith("#") and len(line.strip()) > 60:
            description = line.strip()[:240]
    
    if not date_str:
        dm = re.search(r"(\d{4}[-/]\d{2}[-/]\d{2})", fname)
        if dm:
            date_str = dm.group(1)
    if not date_str:
        dm = re.search(r"(\d{4}[-/]\d{2}[-/]\d{2})", content)
        if dm:
            date_str = dm.group(1)
    
    return title, date_str or "2026-01-01", description or title, tags


def render_markdown_to_html(md_content):
    """Convert markdown to HTML using Python-markdown with extra extensions."""
    return markdown.markdown(
        md_content,
        extensions=['fenced_code', 'codehilite', 'tables', 'nl2br', 'sane_lists']
    )


def generate_article_page(title, date_str, description, tags, body_html, category_name, slug):
    """Generate a standalone HTML page for one article."""
    
    # Format date
    display_date = date_str
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        d = datetime.strptime(date_str, "%Y-%m-%d")
        display_date = f"{d.year}年{d.month}月{d.day}日"
    
    # Read time estimate
    read_time = max(5, len(body_html) // 1800)
    
    # Tags HTML
    tag_colors = {"9001":"", "14001":"green", "45001":"amber", "50001":"pink", "27001":"purple", "治理":"pink", "综合":"amber"}
    tag_html = ""
    default_colors = ["", "green", "amber", "purple", "pink"]
    for i, t in enumerate(tags[:4]):
        color = default_colors[i % len(default_colors)]
        tag_html += f'<span class="tag {color}">{t}</span>\n                    '
    
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | abcISO</title>
<meta name="description" content="{description[:160]}" />
<style>{CSS_ARTICLE}</style>
</head>
<body>

<!-- ===== Navigation ===== -->
<nav class="nav">{NAVBAR_HTML}</nav>

<!-- ===== Main ===== -->
<main>
  <div class="container">

    <!-- Breadcrumb -->
    <nav class="breadcrumb">
      <a href="../kb-list.html">知识库</a>
      <span class="sep">›</span>
      <span class="current">{title[:50]}…</span>
    </nav>

    <!-- Article Header -->
    <header class="article-header">
      <div class="article-tags">
        {tag_html}
      </div>
      <h1>{title}</h1>
      <div class="article-meta">
        <span>📅 {display_date}</span>
        <span>📂 {category_name}</span>
        <span>⏱️ 约 {read_time} 分钟阅读</span>
      </div>
    </header>

    <!-- Article Body -->
    <div class="article-body">
{body_html}
    </div>

  </div>
</main>

{FOOTER_HTML}

<script>
document.querySelector('.nav-toggle').addEventListener('click', function(){{
  document.querySelector('.nav-links').classList.toggle('open');
}});
</script>
<a href="/chat/" target="_blank" style="position:fixed;bottom:24px;right:24px;background:#3B82F6;color:#fff;width:56px;height:56px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:28px;text-decoration:none;box-shadow:0 4px 12px rgba(59,130,246,.4);z-index:999">🤖</a>
</body>
</html>"""


CAT_INFO = {
    "iso9001":    {"name": "ISO 9001 质量管理"},
    "iso14001":   {"name": "ISO 14001 环境管理"},
    "iso45001":   {"name": "ISO 45001 职业健康安全"},
    "iso50001":   {"name": "ISO 50001 能源管理"},
    "iso27001":   {"name": "ISO 27001 信息安全"},
    "ai-governance": {"name": "AI 治理与合规"},
    "general":    {"name": "综合管理"},
    "food-safety": {"name": "食品安全"},
    "iatf16949":  {"name": "IATF 16949 汽车质量"},
}


def main():
    os.makedirs(GEO_OUT, exist_ok=True)
    converted = 0
    skipped = 0
    
    # Build slug-to-filename mapping for cross-references
    slug_map = {}
    
    for cat, info in CAT_INFO.items():
        cat_dir = os.path.join(GEO_DIR, cat)
        if not os.path.isdir(cat_dir):
            continue
        
        for fname in sorted(os.listdir(cat_dir)):
            if not fname.endswith(".md") or fname in ("index.md", "README.md"):
                continue
            
            fpath = os.path.join(cat_dir, fname)
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            # Parse front matter
            fm, body = parse_front_matter(content)
            if fm:
                title = fm.get("title", "")
                date_str = fm.get("date", "")
                description = fm.get("description", "")
                tags = [t.strip() for t in fm.get("tags", "").split(",") if t.strip()]
                permalink = fm.get("permalink", "")
                slug = slugify(title) if title else os.path.splitext(fname)[0]
            else:
                title, date_str, description, tags = extract_meta_from_body(content, fname)
                slug = slugify(title) if title else os.path.splitext(fname)[0]
            
            if not title:
                title = os.path.splitext(fname)[0]
            
            # Check if already converted
            out_path = os.path.join(GEO_OUT, f"{slug}.html")
            if os.path.exists(out_path):
                # Compare modification times
                md_mtime = os.path.getmtime(fpath)
                html_mtime = os.path.getmtime(out_path)
                if html_mtime >= md_mtime:
                    skipped += 1
                    continue
            
            # Convert markdown to HTML
            body_html = render_markdown_to_html(body)
            # Strip duplicate h1 (template already renders title in header)
            import re as _re
            body_html = _re.sub(r"\s*<h1>[^<]*</h1>\s*(<hr\s*/?>)?\s*", "", body_html, count=1)
            
            # Generate full page
            page = generate_article_page(title, date_str, description, tags, body_html, info["name"], slug)
            
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(page)
            
            converted += 1
            print(f"  ✓ {slug}.html  ({info['name']})")
    
    print(f"\n✅ Converted: {converted} new, Skipped: {skipped} up-to-date")
    return converted > 0


if __name__ == "__main__":
    if main():
        print("🟡 Run --apply on _generate_kb.py to update local links")
