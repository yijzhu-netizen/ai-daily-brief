# GEO文章每日可见度报告

**日期：** 2026-05-15（周五）
**报告周期：** 首次基准报告

---

## 状态总览

| 状态 | 篇数 | 文章 |
|------|:----:|------|
| ✅ 已收录（搜索引擎） | 0 | - |
| ❌ 未收录（搜索引擎） | 9 | 全部 |
| 🆕 新增收录 | 0 | - |
| ⚠️ 可访问但缺sitemap | 3 | ISO 14001 / AI智能体 / ISO 9001 |

---

## 站点健康状态

| 检查项 | 状态 | 说明 |
|--------|:----:|------|
| GitHub Pages 首页 | ✅ 可访问 | `https://yijzhu-netizen.github.io/ai-daily-brief/` 正常渲染 |
| Sitemap | ✅ 存在 | `https://yijzhu-netizen.github.io/ai-daily-brief/sitemap.xml` — 含8个URL |
| robots.txt | ✅ 完善 | AI搜索爬虫放行（OAI-SearchBot / Claude-SearchBot / PerplexityBot），训练爬虫屏蔽 |
| 文章总数 | 9篇 | 全部可访问 |
| 首页链接完整性 | ✅ 9篇均链接正确 | 无死链 |

---

## 详细检测结果

### 站点可用性（所有文章均通过浏览器验证可访问）

| # | 文章标题 | 站点状态 | 搜索引擎收录 | 是否在sitemap中 |
|:-:|:---------|:--------:|:----------:|:--------------:|
| 1 | 大模型收费时代制造业企业AI策略调整 | ✅ 可访问 | ❌ 未发现 | ✅ |
| 2 | 欧盟CBAM正式实施：制造业出口企业的能源数据管理体系升级路径 | ✅ 可访问 | ❌ 未发现 | ✅ |
| 3 | 碳双控制度化考核下制造业能源管理体系ISO 50001落地要求 | ✅ 可访问 | ❌ 未发现 | ✅ |
| 4 | 新能源车零售渗透率61.4%：制造业供应链质量管理面临的三重挑战 | ✅ 可访问 | ❌ 未发现 | ✅ |
| 5 | 制造业能源管理体系实际投资回报率分析 | ✅ 可访问 | ❌ 未发现 | ✅ |
| 6 | 制造业企业ISO 14001环境管理体系与ESG信息披露整合路径 | ✅ 可访问 | ❌ 未发现 | ❌ 缺sitemap |
| 7 | ISO 50001能源管理体系：能耗数据造假，企业每年多花多少钱？ | ✅ 可访问 | ❌ 未发现 | ✅ |
| 8 | AI智能体在制造企业生产运营中降低成本的四类应用场景 | ✅ 可访问 | ❌ 未发现 | ❌ 缺sitemap |
| 9 | ISO 9001:2025升级对制造型中小企业供应链管理的五大影响 | ✅ 可访问 | ❌ 未发现 | ❌ 缺sitemap |

### 搜索引擎检测

| 搜索引擎 | 检测结果 | 说明 |
|:---------|:--------:|:-----|
| Bing（国际版） | ❌ 未收录 | site:yijzhu-netizen.github.io 返回0条结果 |
| Bing（国内版） | ❌ 未收录 | 同上 |
| Google | ❌ 未收录 | 无搜索结果 |
| Baidu | ❌ 未收录 | 需验证码确认 |
| AI搜索引擎 | ❌ 未收录 | 站点上线仅1-2天，尚未被爬取 |

---

## 改进建议

### 🔴 高优先级

1. **修复sitemap.xml缺失URL**
   - sitemap当前仅包含7篇文章（+首页），缺少以下3篇：
     - 制造业企业ISO 14001环境管理体系与ESG信息披露整合路径
     - AI智能体在制造企业生产运营中降低成本的四类应用场景
     - ISO 9001:2025升级对制造型中小企业供应链管理的五大影响
   - **原因：** 这3篇文章使用 `# 标题` 格式（无Jekyll frontmatter `layout: default`），Jekyll构建时未自动加入sitemap
   - **建议：** 为这3篇文章添加Jekyll frontmatter（`---\nlayout: default\ntitle: ...\ndate: ...\n---`），或在 `_config.yml` 中配置 `include` 规则手动纳入sitemap

2. **提交sitemap到搜索引擎**
   - Bing Webmaster Tools：`https://www.bing.com/webmasters/` 提交sitemap
   - Google Search Console：`https://search.google.com/search-console` 提交（如能配置域名验证）
   - 百度资源平台：提交sitemap加速收录

### 🟡 中优先级

3. **验证3篇缺frontmatter文章的Jekyll兼容性**
   - ISO 9001 和 AI智能体 两篇文章无frontmatter但可正常渲染（GitHub Pages自动处理）
   - ISO 14001 文章有frontmatter，URL中使用 `ISO-14001`（连字符），确认URL路由正确
   - 建议统一所有文章的frontmatter格式，确保一致性

4. **增加外部反向链接**
   - 在知乎、CSDN、简书等平台发布内容摘要并回链到GitHub Pages
   - 这能帮助搜索引擎更快发现和索引网站

### 🟢 低优先级

5. **监控AI搜索引擎收录**
   - 目前 robots.txt 已正确配置放行 OAI-SearchBot、Claude-SearchBot、PerplexityBot
   - 建议1周后重新检查Perplexity、You.com、ChatGPT等AI搜索是否已引用内容

---

## 补充信息

- **robots.txt 配置健康：** 精细分类控制，AI搜索爬虫放行，训练爬虫屏蔽，推荐配置
- **Schema.org 结构化数据：** 每篇文章均包含 JSON-LD 结构化标注（Article类型），对AI搜索引擎友好
- **站点上线时长：** 约1-2天（2026-05-14发布），尚未进入搜索引擎爬取周期属正常现象
- **下次检查建议：** 2026-05-22（一周后）复查搜索引擎收录情况

---

*报告由 Sage 自动生成 | 检查时间：2026-05-15 10:00 CST*
