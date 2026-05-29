#!/usr/bin/env python3
"""Generate sitemap.xml for abciso.com with correct domain URLs."""
import os, re
from datetime import date

BASE = "https://abciso.com"
TODAY = date.today().isoformat()
DESIGN = "/root/GEO文章/abciso.com/design"

# Core pages
pages = [
    ("", 1.0, "daily"),
    ("kb-list.html", 0.8, "weekly"),
    ("news.html", 0.8, "daily"),
    ("course.html", 0.7, "monthly"),
    ("books/", 0.7, "monthly"),
    ("download.html", 0.5, "monthly"),
    ("about.html", 0.5, "monthly"),
]

# Collect GEO articles from geo/ directory
geo_dir = os.path.join(DESIGN, "geo")
geo_files = sorted([f for f in os.listdir(geo_dir) if f.endswith(".html")]) if os.path.isdir(geo_dir) else []

urls = []
for path, pri, freq in pages:
    urls.append((f"{BASE}/{path}", TODAY, freq, pri))

for gf in geo_files:
    # Use the filename as-is (already URL-friendly lowercase)
    url = f"{BASE}/geo/{gf}"
    urls.append((url, TODAY, "weekly", 0.9))

# Write sitemap
lines = ["<?xml version=\"1.0\" encoding=\"UTF-8\"?>"]
lines.append("<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">")
for url, mod, freq, pri in urls:
    lines.append("  <url>")
    lines.append(f"    <loc>{url}</loc>")
    lines.append(f"    <lastmod>{mod}</lastmod>")
    lines.append(f"    <changefreq>{freq}</changefreq>")
    lines.append(f"    <priority>{pri}</priority>")
    lines.append("  </url>")
lines.append("</urlset>")

out = "\n".join(lines) + "\n"

# Write to both locations
for dst in [os.path.join(DESIGN, "sitemap.xml"), "/var/www/abciso/sitemap.xml"]:
    with open(dst, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"Written {len(urls)} URLs to {dst}")
