#!/usr/bin/env python3
"""Convert all GEO markdown articles to local HTML pages under geo/ dir — VPS版"""

import os, re, sys, glob
from datetime import datetime, timedelta
import markdown

GEO_DIR = "/root/GEO文章"
DESIGN_DIR = "/root/GEO文章/abciso.com/design"
GEO_OUT = os.path.join(DESIGN_DIR, "geo")

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
              <a href="../kb-list.html#ai-governance">AI 治理与合规</a>
              <a href="../kb-list.html#general">综合管理</a>
            </div>
          </li>
          <li><a href="../download.html">资料下载</a></li>
        </ul>
      </div>
    </div>"""

CSS_ARTICLE = """
/* ===== Reset & Base ===== */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{font-size:16px;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}
body{font-family:'Roboto',sans-serif;font-size:16px;line-height:1.6;color:#111827;background:#fff;}
h1,h2,h3,h4{font-family:'Poppins',sans-serif;font-weight:600;color:#111827;line-height:1.25}
h1{font-size:2rem}h2{font-size:1.5rem}h3{font-size:1.25rem}h4{font-size:1rem}
.container{max-width:820px;margin:0 auto;padding:0 1.5rem}
/* Nav */
.nav{position:sticky;top:0;z-index:100;background:rgba(255,255,255,.96);backdrop-filter:blur(8px);border-bottom:1px solid #f0f0f0}
.nav-inner{display:flex;align-items:center;justify-content:space-between;height:3.5rem}
.nav-logo{font-family:'Poppins',sans-serif;font-size:1.25rem;font-weight:700;color:#3B82F6;text-decoration:none;display:flex;align-items:center;gap:.5rem}
.nav-logo span{color:#8B5CF6}
.nav-links{display:flex;align-items:center;gap:2rem;list-style:none}
.nav-links a{font-size:.875rem;font-weight:500;color:#4b5563;text-decoration:none;transition:color .2s;position:relative}
.nav-links a:hover{color:#3B82F6}
.nav-links a.cta{display:inline-flex;align-items:center;gap:.375rem;background:#3B82F6;color:#fff;padding:.5rem 1.25rem;border-radius:6px;font-weight:600;font-size:.875rem;transition:background .2s}
.nav-links a.cta:hover{background:#2563EB;color:#fff}
.nav-links .dropdown{position:relative;cursor:pointer}
.nav-links .dropdown-label{font-size:.875rem;font-weight:500;color:#4b5563;display:flex;align-items:center;gap:.25rem;padding:.25rem 0}
.nav-links .dropdown-label::after{content:"\\25bc";font-size:.625rem;margin-left:.125rem;transition:transform .2s}
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
/* CTA Card */
.cta-article{display:flex;gap:1rem;padding:1.5rem;margin:0 1.5rem 2rem;background:linear-gradient(135deg,#f0f7ff,#faf5ff);border:1px solid #e0e7ff;border-radius:12px;max-width:820px}
.cta-icon{font-size:2rem;line-height:1;flex-shrink:0}
.cta-body h3{font-size:1.125rem;margin-bottom:.375rem}
.cta-body>p{font-size:.875rem;color:#4b5563;margin-bottom:.75rem;line-height:1.5}
.cta-list{list-style:none;padding:0;margin:0 0 1rem;display:flex;flex-direction:column;gap:.375rem}
.cta-list li{font-size:.875rem;color:#374151;line-height:1.4}
.btn-cta-planet{display:inline-flex;align-items:center;gap:.375rem;background:#8B5CF6;color:#fff;padding:.5rem 1.25rem;border-radius:6px;font-weight:600;font-size:.875rem;text-decoration:none;transition:background .2s}
.btn-cta-planet:hover{background:#7C3AED;color:#fff}
@media(max-width:600px){.cta-article{flex-direction:column;align-items:flex-start;padding:1.25rem;margin:0 1rem 1.5rem}}
"""


def slugify(title):
    s = title.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s[:80]


def extract_title_from_body(body):
    """Extract title from first # heading in markdown body, fallback to None."""
    m = re.match(r'^#\s+(.+?)(?:\s*\{|$)', body, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return None

def extract_date_from_filename(fname):
    """Extract date from filename pattern *-YYYYMMDD.md, fallback to file mtime."""
    m = re.search(r'(\d{8})\.md$', fname)
    if m:
        try:
            d = datetime.strptime(m.group(1), "%Y%m%d")
            return d.strftime("%Y-%m-%d")
        except ValueError:
            pass
    return None

def parse_front_matter(content):
    m = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not m:
        return {}, content
    fm = {}
    for line in m.group(1).split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            val = val.strip().strip('"').strip("'")
            fm[key.strip()] = val
    return fm, content[m.end():]


def render_markdown_to_html(md_content):
    return markdown.markdown(
        md_content,
        extensions=['fenced_code', 'codehilite', 'tables', 'nl2br', 'sane_lists']
    )


def generate_article_page(title, date_str, description, tags, body_html, category_name, slug):
    display_date = date_str
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        d = datetime.strptime(date_str, "%Y-%m-%d")
        display_date = f"{d.year}年{d.month}月{d.day}日"
    read_time = max(5, len(body_html) // 1800)

    default_colors = ["", "green", "amber", "purple", "pink"]
    tag_html = ""
    for i, t in enumerate(tags[:4]):
        color = default_colors[i % len(default_colors)]
        tag_html += f'<span class="tag {color}">{t}</span>\n                    '

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | abcISO</title>
<link rel="canonical" href="https://abciso.com/geo/{slug}.html" />
<meta name="description" content="{description[:160]}" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inconsolata:wght@400;600&family=Poppins:wght@500;600;700&family=Roboto:wght@400;500&display=swap" rel="stylesheet">
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

    <!-- CTA Card: 星球引流 -->
    <div class="cta-article">
      <div class="cta-icon">📘</div>
      <div class="cta-body">
        <h3>搜索知识星球【智造本质】</h3>
        <p>10年制造业管理 + 10年ISO认证审核实操经验浓缩。<br>
        两门体系实操课程 + 完整文献清单 + 真实审核案例库。</p>
        <ul class="cta-list">
          <li>📚 《AI时代，你更应该学会管理》— 16讲+番外篇，管理体系通识课</li>
          <li>⚡ 《能源管理体系：39节落地实操课》— ISO 50001体系搭建与审核实务</li>
          <li>📄 本文引用的完整文献清单、合规模板与工具</li>
        </ul>
        <a href="https://t.zsxq.com/lWQ5E" target="_blank" rel="noopener" class="btn-cta-planet">加入星球 → 299元/年</a>
      </div>
    </div>

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <div class="footer-brand">abcISO<span>.com</span></div>
        <p>制造业管理与ISO认证体系实操知识库 · 让管理体系不再纸上谈兵</p>
      </div>
    </footer>

<script>
document.querySelector('.nav-toggle').addEventListener('click', function(){{
  document.querySelector('.nav-links').classList.toggle('open');
}});
</script>
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
}


def main():
    os.makedirs(GEO_OUT, exist_ok=True)
    converted = 0
    skipped = 0

    # 只转换今天新写的文章（3篇），旧文章保留已有HTML
    today_str = datetime.now().strftime("%Y-%m-%d")

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
                slug = slugify(title) if title else os.path.splitext(fname)[0]
            else:
                title = extract_title_from_body(body) or os.path.splitext(fname)[0]
                date_str = extract_date_from_filename(fname) or "2026-01-01"
                description = title
                tags = []
                slug = slugify(title) if title else os.path.splitext(fname)[0]

            if not title:
                title = extract_title_from_body(body) or os.path.splitext(fname)[0]

            # 只转换今天日期的文章，旧文章跳过
            if date_str != today_str:
                # 文件名含今天日期但frontmatter没日期 → 可能是忘了frontmatter
                if extract_date_from_filename(fname) == today_str:
                    print(f"  ⚠ WARNING: {fname} filename has today's date but frontmatter date is missing/invalid, skipping. Consider adding frontmatter.")
                skipped += 1
                continue

            # Check if already converted (mtime guard for same-day re-runs)
            out_path = os.path.join(GEO_OUT, f"{slug}.html")
            if os.path.exists(out_path):
                md_mtime = os.path.getmtime(fpath)
                html_mtime = os.path.getmtime(out_path)
                if html_mtime >= md_mtime:
                    skipped += 1
                    continue

            # Convert
            body_html = render_markdown_to_html(body)
            # Strip first <h1> from body — already rendered in article header
            body_html = re.sub(r'^\s*<h1[^>]*>.*?</h1>\s*', '', body_html, count=1)
            page = generate_article_page(title, date_str, description, tags, body_html, info["name"], slug)

            with open(out_path, "w", encoding="utf-8") as f:
                f.write(page)

            converted += 1
            print(f"  ✓ {slug}.html  ({info['name']})")

    print(f"\n✅ Converted: {converted} new, Skipped: {skipped} up-to-date")

    # Regenerate homepage 精选文章 section
    updated = regenerate_homepage_picks()
    if updated:
        print("  ✓ 首页精选文章已更新")

    # Regenerate kb-list.html from .md files
    updated = regenerate_kb_list()
    if updated:
        print("  ✓ 知识库列表已自动生成")

    # Regenerate news.html from _data/news.json
    updated = regenerate_news_list()
    if updated:
        print("  ✓ 行业动态列表已自动生成")

    return converted > 0


CAT_EMOJI = {
    "iso9001": "✅",
    "iso14001": "🌿",
    "iso45001": "🛡️",
    "iso50001": "⚡",
    "iso27001": "🔒",
    "ai-governance": "🤖",
    "general": "📊",
}

CAT_DESC = {
    "iso9001":    "ISO 9001 质量管理体系标准解读、内审实战、认证指南与体系搭建全流程",
    "iso14001":   "环境管理体系标准解析、碳管理整合、ESG信息披露与绿色制造实践",
    "iso45001":   "职业健康安全管理体系合规、风险控制、AI产线安全与新要求",
    "iso50001":   "能源管理体系标准、碳市场数据对账、节能降碳与能源绩效管理",
    "iso27001":   "信息安全管理体系、数据合规、隐私保护与数字化风控",
    "ai-governance": "AI治理框架、算法合规、欧盟AI法案解读与模型风险管理",
    "general":    "制造业管理方法论、审核实战案例、体系建设与流程优化",
}

CAT_GRADIENT = {
    "iso9001":    ("#eff6ff", "#dbeafe"),
    "iso14001":   ("#f0fdf4", "#dcfce7"),
    "iso45001":   ("#fffbeb", "#fef3c7"),
    "iso50001":   ("#fef2f2", "#fee2e2"),
    "iso27001":   ("#f5f3ff", "#ede9fe"),
    "ai-governance": ("#fdf2f8", "#fce7f3"),
    "general":    ("#f8fafc", "#f1f5f9"),
}


def regenerate_kb_list():
    """Scan all .md files by category, regenerate full kb-list.html category sections."""
    kb_path = os.path.join(DESIGN_DIR, "kb-list.html")
    if not os.path.exists(kb_path):
        print("  WARNING kb-list.html not found, skipping kb-list update")
        return False

    # Build articles by category
    cat_articles = {cat: [] for cat in CAT_INFO}

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
            fm, body = parse_front_matter(content)
            if fm:
                title = fm.get("title", "")
                date_str = fm.get("date", "")
                description = fm.get("description", "")
            else:
                title = extract_title_from_body(body) or os.path.splitext(fname)[0]
                # Try filename date → mtime → hard fallback
                date_str = extract_date_from_filename(fname) or datetime.fromtimestamp(os.path.getmtime(fpath)).strftime("%Y-%m-%d")
                description = title
            if not title:
                title = extract_title_from_body(body) or os.path.splitext(fname)[0]
            slug = slugify(title)

            # Fallback description from first paragraph
            if not description or description == title:
                desc_para = ""
                for line in body.split("\n"):
                    line = line.strip()
                    if line and not line.startswith("#") and not line.startswith(">") and len(line) > 40:
                        desc_para = line[:240]
                        break
                description = desc_para or title

            cat_articles[cat].append({
                "title": title,
                "date": date_str,
                "description": description,
                "slug": slug,
                "mtime": os.path.getmtime(fpath),
            })

    total_articles = sum(len(v) for v in cat_articles.values())

    # Generate HTML for each category
    sections_html = []
    for cat, info in CAT_INFO.items():
        arts = cat_articles.get(cat, [])
        if not arts:
            continue
        # Sort by mtime, newest first
        arts.sort(key=lambda a: a["mtime"], reverse=True)
        emoji = CAT_EMOJI.get(cat, "📄")
        grad_from, grad_to = CAT_GRADIENT.get(cat, ("#f8fafc", "#f1f5f9"))
        desc = CAT_DESC.get(cat, info["name"])

        articles_html = []
        for art in arts:
            desc_text = art["description"]
            if len(desc_text) > 200:
                desc_text = desc_text[:197] + "…"

            # Calculate read time
            read_time = max(5, len(desc_text) // 200 * 3)

            # Format date
            display_date = art["date"]
            if re.match(r"^\d{4}-\d{2}-\d{2}$", art["date"]):
                d = datetime.strptime(art["date"], "%Y-%m-%d")
                display_date = f"{d.year}-{d.month:02d}-{d.day:02d}"

            article_html = f"""        <article class="article-card">
          <a href="/geo/{art['slug']}.html" class="card-link">
            <div class="article-thumb"></div>
            <div class="article-body">
              <h3>{art['title'][:80]}</h3>
              <p class="article-excerpt">{desc_text}</p>
              <div class="article-meta">
                <span class="meta-item">📅 {display_date}</span>
                <span class="meta-item">⏱️ {read_time} 分钟阅读</span>
                <span class="card-tags"></span>
              </div>
              <span class="read-more">阅读全文 →</span>
            </div>
          </a>
        </article>"""
            articles_html.append(article_html)

        section = f"""    <!-- ==================== CATEGORY: {info['name']} ==================== -->
    <div class="cat-section" id="{cat}">
      <div class="cat-header-wrap" style="background:linear-gradient(135deg, {grad_from} 0%, {grad_to} 100%)">
        <h2 class="cat-section-title">{emoji} {info['name']}</h2>
        <p class="cat-section-desc">{desc}</p>
      </div>
      <div class="article-list">

{chr(10).join(articles_html)}

      </div>
    </div>"""
        sections_html.append(section)

    kb_content_new = "\n".join(sections_html)

    with open(kb_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<!-- KB_LIST_START -->"
    end_marker = "<!-- KB_LIST_END -->"
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("  WARNING: KB_LIST_START or KB_LIST_END markers not found in kb-list.html")
        return False

    start_marker_end = start_idx + len(start_marker)
    replacement = content[start_marker_end:end_idx]
    new_section = f"\n{kb_content_new}\n    "
    content = content[:start_marker_end] + new_section + content[end_idx:]

    # Update result count
    content = re.sub(
        r'共 <strong>\d+</strong> 篇文章 · <strong>\d+</strong> 个分类',
        f'共 <strong>{total_articles}</strong> 篇文章 · <strong>{len([c for c, a in cat_articles.items() if a])}</strong> 个分类',
        content
    )

    with open(kb_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  📚 知识库更新：{total_articles} 篇文章，{len([c for c, a in cat_articles.items() if a])} 个分类")
    return True


def regenerate_news_list():
    """Read _data/news.json and regenerate news.html news-list section."""
    news_path = os.path.join(DESIGN_DIR, "news.html")
    data_path = os.path.join(DESIGN_DIR, "_data", "news.json")
    if not os.path.exists(news_path):
        print("  WARNING news.html not found, skipping news update")
        return False
    if not os.path.exists(data_path):
        print("  WARNING _data/news.json not found, skipping news update")
        return False

    import json
    with open(data_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    # Sort by date descending, preserve original order for same date
    for idx, item in enumerate(items):
        item["_orig_idx"] = idx
    items.sort(key=lambda x: (x.get("date", ""), -x["_orig_idx"]), reverse=True)

    # Generate HTML
    news_html_lines = []
    for i, item in enumerate(items, 1):
        date = item.get("date", "")
        title = item.get("title", "")
        url = item.get("url", "")
        category = item.get("category", "iso")
        cat_label = item.get("cat_label", "ISO动态")
        source = item.get("source", "")

        news_html_lines.append(f"""      <!-- {i} -->
      <a data-category="{category}" href="{url}" class="news-item" target="_blank" rel="noopener">
        <span class="date">{date}</span>
        <span class="title">{title}</span>
        <span class="cat-tag cat-{category}">{cat_label}</span>
        <span class="source-tag">{source}</span>
        <span class="link-icon">🔗</span>
      </a>""")

    news_list_html = "\n".join(news_html_lines)

    with open(news_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<!-- NEWS_LIST_START -->"
    end_marker = "<!-- NEWS_LIST_END -->"
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("  WARNING: NEWS_LIST_START or NEWS_LIST_END markers not found in news.html")
        return False

    start_marker_end = start_idx + len(start_marker)
    new_section = f"\n{news_list_html}\n      "
    content = content[:start_marker_end] + new_section + content[end_idx:]

    with open(news_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  📰 行业动态更新：{len(items)} 条新闻")
    return True


def regenerate_homepage_picks():
    """Scan .md files, pick 3 newest by mtime (only last 24h), update index.html 精选文章 section."""
    index_path = os.path.join(DESIGN_DIR, "index.html")
    if not os.path.exists(index_path):
        print("  WARNING index.html not found, skipping homepage update")
        return False

    cutoff = datetime.now() - timedelta(hours=24)

    # Gather all .md files with mtime
    articles = []
    for cat, info in CAT_INFO.items():
        cat_dir = os.path.join(GEO_DIR, cat)
        if not os.path.isdir(cat_dir):
            continue
        for fname in os.listdir(cat_dir):
            if not fname.endswith(".md") or fname in ("index.md", "README.md"):
                continue
            fpath = os.path.join(cat_dir, fname)
            mtime = os.path.getmtime(fpath)
            # Skip files older than 24 hours
            if datetime.fromtimestamp(mtime) < cutoff:
                continue
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            fm, body = parse_front_matter(content)
            if fm:
                title = fm.get("title", "")
                description = fm.get("description", "")
                tags = [t.strip() for t in fm.get("tags", "").split(",") if t.strip()]
                date_str = str(fm.get("date", ""))[:10] if fm.get("date") else ""
            else:
                title = extract_title_from_body(body) or os.path.splitext(fname)[0]
                description = title
                tags = []
                date_str = extract_date_from_filename(fname) or ""
            if not title:
                title = extract_title_from_body(body) or os.path.splitext(fname)[0]
            slug = slugify(title)

            # First paragraph for description fallback
            first_para = ""
            if not description or description == title:
                for line in body.split("\n"):
                    line = line.strip()
                    if line and not line.startswith("#") and not line.startswith(">") and len(line) > 40:
                        first_para = line[:160]
                        break

            articles.append({
                "cat": cat,
                "title": title,
                "description": description if description and description != title else first_para,
                "slug": slug,
                "tags": tags if tags else [info["name"].replace("ISO ", "ISO ")],
                "cat_name": info["name"],
                "mtime": mtime,
                "date_str": date_str,
            })

    # Sort by frontmatter date (newest first), then mtime, then slug
    articles.sort(key=lambda a: (a["date_str"], a["mtime"], a["slug"]), reverse=True)
    picks = articles[:3]

    if not picks:
        return False

    # Tag name short
    tag_short = {
        "iso9001": "ISO 9001",
        "iso14001": "ISO 14001",
        "iso45001": "ISO 45001",
        "iso50001": "ISO 50001",
        "iso27001": "ISO 27001",
        "ai-governance": "AI治理",
        "general": "综合",
    }

    # Generate card HTML
    cards_html = []
    for art in picks:
        emoji = CAT_EMOJI.get(art["cat"], "📄")
        tag_label = tag_short.get(art["cat"], art["cat_name"])
        desc = art["description"]
        if len(desc) > 140:
            desc = desc[:137] + "…"

        card = f"""      <article class="article-card">
        <div class="art-img">{emoji}</div>
        <div class="art-body">
          <a href="kb-list.html#{art['cat']}" class="art-cat">{art['cat_name']}</a>
          <h3>{art["title"][:60]}</h3>
          <p>{desc}</p>
        <div class="article-meta"><span class="meta-item">📅 {art['date_str'] or '—'}</span></div>
          <a href="geo/{art["slug"]}.html" class="read-more">阅读全文 →</a>
        </div>
      </article>"""
        cards_html.append(card)

    new_section = f"""<!-- ===== 精选文章 ===== -->
<section class="section" style="background:#fafbfc">
  <div class="container">
    <div class="section-header">
      <h2>📚 精选文章</h2>
      <a href="kb-list.html" class="more-link">浏览全部 →</a>
    </div>
    <div class="grid-3">
{chr(10).join(cards_html)}

    </div>
  </div>
</section>"""

    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find and replace the 精选文章 section
    start_marker = "<!-- ===== 精选文章 ===== -->"
    end_marker = "<!-- ===== 热门下载 ===== -->"
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("  WARNING: 精选文章 or 热门下载 markers not found in index.html")
        return False

    old_section = content[start_idx:end_idx]
    content = content.replace(old_section, new_section + "\n")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  📚 首页精选文章更新为最近3篇：")
    for art in picks:
        print(f"    - {art['title'][:50]}…")
    return True


if __name__ == "__main__":
    main()
