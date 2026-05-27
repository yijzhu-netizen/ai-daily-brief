# GEO引用可见度监测报告 — 2026-05-26

> 生成时间：2026-05-26 10:00 CST
> 站点：https://yijzhu-netizen.github.io/ai-daily-brief/
> 文章总数：31（sitemap收录）

---

## 一、AI爬虫配置状态 ✅

### 搜索爬虫（已放行 ✅）
| 爬虫 | 状态 | 策略 |
|------|------|------|
| `OAI-SearchBot` | ✅ Allow `/` | OpenAI搜索实时检索 |
| `Claude-SearchBot` | ✅ Allow `/` | Claude搜索实时检索 |
| `PerplexityBot` | ✅ Allow `/` | Perplexity搜索爬虫 |

### 用户触发爬虫（已放行 ✅）
| 爬虫 | 状态 | 策略 |
|------|------|------|
| `ChatGPT-User` | ✅ Allow `/` | 用户粘贴URL触发 |
| `Claude-User` | ✅ Allow `/` | 同上 |
| `Perplexity-User` | ✅ Allow `/` | 同上 |
| `Google-Agent` | ✅ Allow `/` | Gemini/Google用户代理 |
| `AWS-Agent` | ✅ Allow `/` | AWS Bedrock查询检索 |

### 训练爬虫（已屏蔽 ✅）
| 爬虫 | 状态 |
|------|------|
| `GPTBot` | ✅ Disallow |
| `ClaudeBot` | ✅ Disallow |
| `Meta-ExternalAgent` | ✅ Disallow |
| `CCBot` | ✅ Disallow |
| `Google-Extended` | ✅ Disallow |
| `Applebot-Extended` | ✅ Disallow |

**结论：** robots.txt配置正确，所有AI搜索爬虫已放行，训练爬虫已屏蔽，无需修改。

---

## 二、文章可用性检测

### 站点主页
- `https://yijzhu-netizen.github.io/ai-daily-brief/` → **200 ✅**

### sitemap
- `https://yijzhu-netizen.github.io/ai-daily-brief/sitemap.xml` → **200 ✅**（31条URL）
- Google Search Console验证文件 → **200 ✅**

### 最新3篇文章HTTP状态

| # | 文章 | 文件路径 | 目录路径状态 | Permalink路径状态 | 说明 |
|---|------|---------|:----------:|:----------------:|------|
| 1 | ISO9001-2025转版过渡期制造企业质量数据治理与AI融合的系统性路径 | `general/...` | **404 ❌** | **200 ✅** | 有自定义permalink，llms.txt路径不匹配 |
| 2 | 十五五节能降碳目标下制造业ISO50001能源数据体系与碳资产管理融合路径 | `iso50001/...` | **404 ❌** | **200 ✅** | 有自定义permalink，llms.txt路径不匹配 |
| 3 | 制造业AI质检系统部署陷阱与数据验证：2026年工业视觉准确率误报率与ROI真相 | `ai-governance/...` | **200 ✅** | — | 目录路径可直接访问 |

**最新文章（今日新增2篇）**：可通过permalink路径正常访问 ✅，但通过llms.txt中的目录路径访问返回404。

### 文章元数据
- 今日新增文章2篇（2026-05-26 01:03 commit）
- 昨日新增文章2篇（2026-05-25）
- GitHub Pages构建状态：**成功 ✅**（2026-05-26 01:04 UTC）

---

## 三、⚠️ llms.txt URL与Jekyll permalink不匹配（核心问题）

**问题严重性：高** — llms.txt中约 **18/29条文章URL** 返回404

### 根因
Jekyll站点使用 `permalink: pretty` 默认配置，但部分文章在frontmatter中设置了自定义 `permalink:` 字段。Jekyll会将这类文章渲染到 **permalink路径**，而非文件目录路径。

**llms.txt中的URL格式（目录路径，不可访问）：**
```
/ai-daily-brief/iso50001/ISO-50001能源管理体系-能耗数据造假
```

**实际可访问的URL格式（permalink路径）：**
```
/ai-daily-brief/ISO-50001能源管理体系-能耗数据造假/
```

### 受影响文章列表（18篇）

#### ai-governance（3篇）
| 文章 | llms.txt路径 | 正确permalink路径 |
|------|-------------|------------------|
| 制造业AI辅助培训与传统培训的五年投资回报率对比分析 | `ai-governance/...` | `/制造业AI辅助培训与传统培训的五年投资回报率对比分析/` |
| 大模型收费时代制造业企业AI策略调整 | `ai-governance/...` | `/大模型收费时代制造业企业AI策略调整/` |
| 新能源车零售渗透率61.4%制造业供应链质量管理面临的三重挑战 | `ai-governance/...` | 文件名含`%`号，需修复URL编码 |

#### general（3篇）
| 文章 | 问题 |
|------|------|
| ISO-9001-2025转版过渡期六大常见不合规项 | 有自定义permalink |
| ISO9001-2025转版过渡期制造企业质量数据治理与AI融合的系统性路径 | **今日新增**，有自定义permalink |
| 制造企业ISO管理体系基于风险导向的内部审核效率提升路径 | 有自定义permalink |

#### iso50001（8篇）
| 文章 | 问题 |
|------|------|
| 2026夏季用电高峰前制造业ISO50001能源管理体系负荷管理与应急响应 | 有自定义permalink |
| 2026年碳市场行业扩围后制造企业ISO50001能源数据管理的三项合规要求 | 有自定义permalink |
| ISO 50001能源管理体系与碳市场数据对账实操（含空格） | 有自定义permalink |
| ISO-50001能源管理体系-能耗数据造假 | 有自定义permalink |
| 制造业能源管理体系实际投资回报率分析 | 有自定义permalink |
| 欧盟CBAM正式实施制造业能源数据管理体系升级路径 | 有自定义permalink |
| 碳双控制度化考核下制造业能源管理体系ISO-50001落地要求 | 有自定义permalink |
| **十五五节能降碳目标下制造业ISO50001能源数据体系与碳资产管理融合路径** | **今日新增**，有自定义permalink |

#### 其他（4篇）
| 文章 | 问题 |
|------|------|
| iso14001/制造业企业ISO-14001环境管理体系与ESG信息披露整合路径 | 有自定义permalink |
| iso27001/ISO-27001信息安全管理体系在制造企业数字化车间落地的五大核心要求 | 有自定义permalink |
| iso45001/ISO45001职业健康安全管理体系在制造业AI自动化产线改造中的合规管理新要求 | 有自定义permalink |
| iso9001/中小制造企业首次ISO 9001:2025认证全流程指南 | 有自定义permalink |

### 意外正常访问的文章（11篇）
以下文章在llms.txt目录路径下仍可正常访问（200 ✅）：
- ai-governance目录中 **6篇**（无自定义permalink的文章）
- general目录中 **1篇**（中小制造企业多体系ISO整合管理）
- iso50001目录中 **1篇**（十五五节能降碳目标下企业如何用ISO50001量化——无frontmatter）
- iso9001目录中 **1篇**（ISO-9001-2025升级对中小制造企业）
- abciso.com目录中 **2篇**（课程介绍）

---

## 四、搜索可见性

### Google
- Search Console验证文件：✅ 存在且可访问
- 站点：已配置Google Search Console（`google_site_verification: XO3hiNDpU86_TSemPVBc5DC0RHw6yrJSeOufqbMY04U`）
- Sitemap已提交：✅
- Ping Google on push工作流：**成功 ✅**

### 收录建议
- 今日2篇新文章已成功部署（通过permalink路径），等待搜索引擎爬取
- sitemap已包含所有最新文章

---

## 五、待办事项

### 🔴 优先级：高 — llms.txt URL修复
所有有 `permalink:` 字段的文章，llms.txt中的URL需更新为 permalink 路径。
建议做法：
1. 批量扫描所有`.md`文件，提取 `permalink:` 值
2. 自动更新llms.txt中的对应URL
3. 或：删除所有文章的 `permalink:` 字段，统一使用Jekyll默认目录路径

### 🟡 优先级：中 — 新能源车文章URL编码问题
文件名中包含 `61.4%`，其中 `%` 在URL编码中需要双重编码（`%25`）。建议：
- 修改文件名，去掉 `%` 符号（如改为`61.4pct`或`百分之61.4`）
- 然后更新llms.txt和sitemap

### 🟢 优先级：低 — 建议后续优化
- 考虑统一文章URL策略：要么全部用 `permalink`，要么都不用，避免混合策略
- Git commit message中更详细地标注哪些文件有结构性变更（如此次的permalink不一致问题）
- 考虑添加 `GET https://yijzhu-netizen.github.io/ai-daily-brief/` 的定时monitoring脚本

---

*报告由Sage (Hermes Agent) 自动生成*
