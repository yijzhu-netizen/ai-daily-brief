# GEO内容分发流水线说明

> 备份日期：2026-05-21
> 后续更新此文件即可保持记忆同步

## 整体架构

```
GEO文章每日产出  ──→  GitHub Pages (ai-daily-brief)
                      ↓               ↓
                  百家号(09:00)    知乎专栏(11:30)
                  每天2篇           自动同步含引流语的文章
```

## 一、GEO文章产出

| 项目 | 内容 |
|------|------|
| 定时任务 | `智造本质GEO - 每日两篇（AI管理+能源管理）` |
| Job ID | `72d53c420225` |
| 执行时间 | 每天 09:00 |
| 技能 | `geo-writer` |
| 输出目录 | `/mnt/e/GEO文章/` |
| 仓库 | `yijzhu-netizen/ai-daily-brief` (GitHub Pages) |
| 方法论 | `E:/知识库/三层诱惑链方法论.md` |

## 二、百家号自动发布

| 项目 | 内容 |
|------|------|
| 定时任务 | `百家号每日GEO文章同步（2篇/天）` |
| Job ID | `7fbbe921f339` |
| 执行时间 | 每天 09:00 |
| 入口脚本 | `~/.hermes/profiles/sage/scripts/bjh_daily_publish.py` |
| 核心发布脚本 | `C:/temp/bjh_publish_v5.py` (Windows) |
| 状态跟踪 | `~/.hermes/bjh_publish_state.json` |
| Chrome持久化 | `C:\temp\bjh_profile`，远程调试端口9222 |

**发布逻辑：**
1. 扫描 `/mnt/e/GEO文章/*.md`（排除 index.md, README.md, zhishixingqiu-*）
2. 与状态文件中已发布的文件名比对去重
3. 按文件修改时间排序，取最新的2篇
4. 确保Chrome远程调试端口9222就绪
5. 对每篇：读取.md全文 → 调用 `bjh_publish_v5.py --title --content` → 记录结果
6. 每篇间隔30秒，防反爬

**技术细节：**
- 使用 PubSub 方式：Playwright连接Chrome CDP → 填标题/正文/封面上传 → 存草稿获取JWT Token → Python requests 调 `/pcui/article/publish` API
- 封面上传弹窗"确定"按钮文本会变成"确定 (1)"，需用`includes`匹配
- 不需要手动登录，Chrome持久化目录保持登录态

## 三、知乎专栏同步

| 项目 | 内容 |
|------|------|
| 定时任务 | `GEO→知乎专栏每日同步` |
| Job ID | `934ee110a090` |
| 执行时间 | 每天 11:30 |
| 入口脚本 | `~/.hermes/profiles/sage/scripts/zhihu_daily_sync.py` |
| 运行模式 | `no_agent: true`（纯脚本，省token） |
| 专栏ID | `c_2034942220785153532` |
| Session目录 | `~/.cloak-zhihu-session` |
| 浏览器 | `~/.cloakbrowser/chromium-146.0.7680.177.3/chrome` |
| 跟踪文件 | `~/.hermes/profiles/sage/cache/zhihu_sync_tracker.json` |

**同步逻辑：**
1. 扫描 `/mnt/e/GEO文章/*.md` 文件
2. 与跟踪文件中的已同步标题比对去重
3. 只同步包含引流语的文章（知识星球、智造本质、课程《、能源管理体系、AI时代）
4. Cloak浏览器持久上下文，headless模式
5. Playwright打开 ziuanlan.zhihu.com/write?column_id=xxx
6. 填写标题 + 逐段键盘输入正文（截断至18000字符）
7. 点击"发布到专栏" → 点击"发布"按钮
8. 跟踪记录已同步的文章

**Session过期处理：**
当跳转到登录页时，脚本会中止同步，等待手动重新登录。

## 四、GEO每日整体报告（每天11:00）

| 项目 | 内容 |
|------|------|
| 定时任务 | `GEO每日整体报告 - 11点（产出+监测+趋势+发布数据）` |
| Job ID | `61491ca96709` |
| 执行时间 | 每天 11:00 |
| 交付渠道 | 微信 |
| 技能 | 无（纯LLM） |
| 工作目录 | `/mnt/e/GEO文章/` |

**报告包含7个板块：**
1. 文章产出（今日新增、累计总数、本周趋势）
2. **百家号发布**（今日发布文章、阅读量、累计总数）
3. **知乎同步**（今日同步文章、阅读量、累计总数）
4. GitHub同步（今日提交次数、状态）
5. 五平台监测（站点健康、收录情况、各平台引用趋势）
6. 待办事项（sitemap Bug、index.md重复链接、百度站长验证）
7. 报告保存到 `/mnt/e/GEO文章/.report/daily-summary-YYYYMMDD.md`

**阅读量获取方法：**
- 读取 `~/.hermes/bjh_publish_state.json` 和 `~/.hermes/profiles/sage/cache/zhihu_sync_tracker.json`
- 对今日发布的文章，通过 web_search 搜索文章URL获取阅读数据

## 五、GEO引用监控

| 项目 | 内容 |
|------|------|
| 增强版监控 | 每天10:00，Job ID `28aeb0854e50` |
| 监控平台 | DeepSeek、豆包、千问、Kimi、元宝 + Google |
| 检测内容 | 文章是否被AI搜索引用、可见度报告 |

## 五、待办事项

- [ ] 百度站长平台验证文件（baidu_verify）确认是否已放置到GitHub Pages仓库根目录
- [ ] sitemap中4个URL的%20编码Bug修复
- [ ] index.md中2篇重复链接修复
