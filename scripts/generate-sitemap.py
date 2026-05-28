#!/usr/bin/env python3
"""生成 site sitemap.xml，从每个 .md 文件 frontmatter 读取 permalink"""

import os, re, sys, glob
from datetime import date
from urllib.parse import quote

REPO_ROOT = "/root/GEO文章"
BASE_URL = "https://yijzhu-netizen.github.io/ai-daily-brief"
# 排除文件
EXCLUDE = {"index.md", "README.md", "Gemfile", "Gemfile.lock"}
EXCLUDE_DIRS = {".git", ".pipeline", ".report", "abciso.com", "geo-site", "scripts", "assets", "_knowledge"}

today = date.today().isoformat()

def extract_permalink(filepath):
    """从 .md 文件读取 permalink（frontmatter 中的），无 frontmatter 则从文件路径推算"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 有 YAML frontmatter
    if content.startswith('---'):
        m = re.match(r'^---\s*\n(.*?\n)---', content, re.DOTALL)
        if m:
            fm = m.group(1)
            for line in fm.split('\n'):
                if line.startswith('permalink:'):
                    permalink = line.split(':', 1)[1].strip().strip('"').strip("'")
                    if permalink:
                        if not permalink.startswith('/'):
                            permalink = '/' + permalink
                        if not permalink.endswith('/'):
                            permalink += '/'
                        return permalink
    
    # 无 frontmatter 或没有 permalink 字段 → 从文件路径推算
    rel_path = os.path.relpath(filepath, REPO_ROOT)
    name = os.path.splitext(rel_path)[0]
    return f"/{name}/"


def collect_articles():
    """收集所有 .md 文章"""
    articles = []
    pattern = os.path.join(REPO_ROOT, "**", "*.md")
    
    for filepath in glob.glob(pattern, recursive=True):
        rel = os.path.relpath(filepath, REPO_ROOT)
        # 排除
        parts = rel.replace('\\', '/').split('/')
        if parts[0] in EXCLUDE_DIRS:
            continue
        filename = os.path.basename(filepath)
        if filename in EXCLUDE or filename.startswith('_'):
            continue
        
        permalink = extract_permalink(filepath)
        
        # 首页
        if rel == "index.md":
            priority = "1.0"
            changefreq = "daily"
        else:
            priority = "0.9"
            changefreq = "weekly"
        
        articles.append((permalink, priority, changefreq))
    
    return articles


def generate_sitemap(articles):
    """生成 sitemap XML"""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # 首页排第一
    lines.append('  <url>')
    lines.append(f'    <loc>{BASE_URL}/</loc>')
    lines.append(f'    <lastmod>{today}</lastmod>')
    lines.append(f'    <changefreq>daily</changefreq>')
    lines.append(f'    <priority>1.0</priority>')
    lines.append('  </url>')
    
    for permalink, priority, changefreq in articles:
        if permalink == '/':
            continue
        full_url = f"{BASE_URL}{permalink}"
        # 只对路径部分编码（保留已有编码）
        encoded_url = quote(full_url, safe='/:')
        
        lines.append('  <url>')
        lines.append(f'    <loc>{encoded_url}</loc>')
        lines.append(f'    <lastmod>{today}</lastmod>')
        lines.append(f'    <changefreq>{changefreq}</changefreq>')
        lines.append(f'    <priority>{priority}</priority>')
        lines.append('  </url>')
    
    lines.append('</urlset>')
    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    articles = collect_articles()
    print(f"Found {len(articles)} articles", file=sys.stderr)
    
    xml = generate_sitemap(articles)
    output_path = os.path.join(REPO_ROOT, "sitemap.xml")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml)
    
    print(f"Written: {output_path}")
    
    # 验证所有 URL
    for permalink, _, _ in articles:
        full_url = f"{BASE_URL}{permalink}"
        print(f"  {full_url}")
