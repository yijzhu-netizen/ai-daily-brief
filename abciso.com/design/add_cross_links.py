#!/usr/bin/env python3
"""Add cross-reference links to GEO articles on abciso.com."""
import os, re, shutil

GEO_DIR = "/root/GEO文章/abciso.com/design/geo"
DEPLOY_DIR = "/var/www/abciso/geo"

def classify(filename):
    fn = filename.lower()
    if 'iso-9001' in fn or 'iso9001' in fn:
        return 'iso9001'
    if 'iso-14001' in fn or 'iso14001' in fn or '环境' in fn or 'esg' in fn:
        return 'iso14001'
    if 'iso-45001' in fn or 'iso45001' in fn or '职业健康' in fn:
        return 'iso45001'
    if 'iso-50001' in fn or 'iso50001' in fn or '能源' in fn or '碳' in fn or 'cbam' in fn or '节能' in fn:
        return 'iso50001'
    if 'iso-27001' in fn or 'iso27001' in fn or '信息安全' in fn:
        return 'iso27001'
    if 'ai' in fn or 'agent' in fn or '大模型' in fn or '智能体' in fn:
        return 'ai'
    return 'general'

def get_title(content):
    m = re.search(r'<title>([^<]+)</title>', content)
    if m:
        return m.group(1).replace(' | abcISO', '').replace(' - abcISO', '').strip()
    m = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
    return m.group(1).strip() if m else ''

def make_related_html(related_items):
    """Generate the related articles HTML block."""
    if not related_items:
        return ''
    lis = '\n'.join(f'    <li style="margin-bottom:0.5rem;"><a href="/geo/{fname}" style="color:#2563eb;text-decoration:none;font-size:0.95rem;">{title}</a></li>'
                     for fname, title in related_items)
    return f'''
<section class="related-articles" style="max-width:800px;margin:2rem auto;padding:1.5rem;background:#f8f9fa;border-radius:8px;border-left:4px solid #2563eb;">
  <h3 style="margin:0 0 1rem;font-size:1.1rem;color:#1e40af;">📚 相关文章</h3>
  <ul style="list-style:none;padding:0;margin:0;">
{lis}
  </ul>
</section>
'''

# Step 1: Read all files and classify
files = sorted([f for f in os.listdir(GEO_DIR) if f.endswith('.html')])
print(f"Found {len(files)} GEO files")

groups = {}
titles = {}
for f in files:
    g = classify(f)
    groups.setdefault(g, []).append(f)
    with open(os.path.join(GEO_DIR, f), 'r', encoding='utf-8') as fh:
        content = fh.read()
    titles[f] = get_title(content)

for g, fs in sorted(groups.items()):
    print(f"  {g}: {len(fs)} files")

# Step 2: Add cross-links to each file
modified = 0
for f in files:
    filepath = os.path.join(GEO_DIR, f)
    with open(filepath, 'r', encoding='utf-8') as fh:
        content = fh.read()

    # Skip if already has related articles
    if 'related-articles' in content:
        print(f"  SKIP (already has): {f}")
        continue

    g = classify(f)
    # Get siblings from same group
    siblings = [s for s in groups[g] if s != f]
    # If not enough, supplement from general
    if len(siblings) < 3 and g != 'general':
        extra = [s for s in groups.get('general', []) if s != f]
        siblings.extend(extra)
    # If still not enough, supplement from ai group
    if len(siblings) < 3 and g != 'ai':
        extra = [s for s in groups.get('ai', []) if s != f]
        siblings.extend(extra)

    # Pick up to 5
    related = [(s, titles.get(s, s)) for s in siblings[:5]]

    if not related:
        print(f"  SKIP (no siblings): {f}")
        continue

    related_html = make_related_html(related)

    # Insert before </body>
    if '</body>' in content:
        content = content.replace('</body>', related_html + '\n</body>')
    else:
        content += related_html

    with open(filepath, 'w', encoding='utf-8') as fh:
        fh.write(content)

    # Copy to deploy
    deploy_path = os.path.join(DEPLOY_DIR, f)
    shutil.copy2(filepath, deploy_path)

    modified += 1
    print(f"  OK ({len(related)} links): {f}")

print(f"\nDone: {modified}/{len(files)} files modified")
