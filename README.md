# Claude Skills 技能集合

这是一个精心整理的 Claude Code 技能集合仓库，包含了多个实用的 AI 技能，涵盖内容创作、办公文档处理、浏览器自动化、前端开发等多个领域。

## 📚 技能分类

### 🎨 内容创作类
- **ai-insights-daily** - AI动态洞察专栏生成器，为"AI拉呱"品牌生成高质量中文技术文章
- **viral-article-creator** - 智能爆文创作工具，从原文翻译、调研到改写的全流程创作
- **viral-article-rewriter** - 爆文改写器，将普通技术文章改写成高传播度的爆文风格
- **video-script-writer** - 视频脚本写作工具，将技术文章批量改写为4-6分钟的知识类视频脚本
- **technical-blog-writing** - 技术博客写作，结构化输出开发者内容
- **doc-coauthoring** - 文档协作指南，帮助创建提案、技术规范等结构化内容
- **book-chapter-writer** - 技术书籍/教程章节写作工具，按五步流程输出大篇幅、含 Python 示例、举例丰富的中文章节
- **paper-writer** - 学术/科研论文全流程写作工具，从文献检索到投稿就绪，支持中英日三语

### 📄 文档处理类
- **pdf** - PDF 文件全功能处理（读取、合并、分割、转换、加密等）
- **pdf-to-images** - PDF 转图片工具
- **xlsx** - Excel 表格处理（创建、编辑、数据分析）
- **pptx** - PowerPoint 演示文稿处理
- **docx** - Word 文档处理

### 🌐 浏览器与网络类
- **agent-browser** - 浏览器自动化 CLI，支持页面交互、表单填写、截图、数据提取等
- **baoyu-url-to-markdown** - 使用 Chrome CDP 将任何 URL 转换为 Markdown
- **webapp-testing** - 本地 Web 应用测试工具

### 💻 开发设计类
- **frontend-design** - 创建高质量前端界面，避免通用 AI 美学
- **web-artifacts-builder** - 构建复杂的多组件 Web artifacts
- **algorithmic-art** - 使用 p5.js 创建算法艺术
- **canvas-design** - 使用设计哲学创建精美的视觉艺术
- **mcp-builder** - 创建高质量 MCP (Model Context Protocol) 服务器
- **remotion** - Remotion 最佳实践，使用 React 创建视频内容

### 🎯 工具与效率类
- **skill-creator** - 创建、修改和优化技能的工具
- **theme-factory** - 为 artifacts 应用主题样式（幻灯片、文档、报告等）
- **brand-guidelines** - 应用 Anthropic 官方品牌色彩和排版
- **slack-gif-creator** - 创建适用于 Slack 的动画 GIF
- **find-skills** - 帮助用户发现和安装新技能

### 📝 代码与协作类
- **code-review-excellence** - 掌握有效的代码审查实践
- **receiving-code-review** - 接收代码审查反馈的最佳实践
- **internal-comms** - 内部沟通文档模板（状态报告、更新、FAQ 等）
- **VibeSec-Skill** - 安全编码技能，从漏洞赏金猎人视角审查代码，涵盖 XSS、IDOR、SQL 注入等常见漏洞

### 🖼️ AI 图像生成
- **ai-image-generation** - 使用 FLUX、Gemini、Grok 等 50+ 模型生成 AI 图像

### 💰 金融工具类
- **polymarket-trading-bot** - Polymarket 复制交易机器人，自动跟随成功交易者进行预测市场交易，支持盈利监控和仓位管理
- **zt-selector** - A股涨停选股工具，基于6大规则筛选模拟盘标的（智能过滤、市盈率展示、红肥绿瘦检查）

### 📓 其他工具
- **notebooklm** - Google NotebookLM 完整 API 访问

## 🚀 快速开始

### 前置要求
- 安装 [Claude Code](https://claude.com/claude-code)
- 熟悉 Claude Code 的基本使用

### 使用技能

在 Claude Code 中，你可以通过以下方式使用技能：

```bash
# 方式1：直接提及技能功能
# 例如："帮我把这个 PDF 转成图片"（会自动触发 pdf-to-images 技能）

# 方式2：使用斜杠命令
/pdf          # 调用 PDF 处理技能
/xlsx         # 调用 Excel 处理技能
/agent-browser # 调用浏览器自动化技能
```

## 📁 目录结构

```
.
├── README.md                    # 本文件
├── agent-browser/               # 浏览器自动化
├── ai-insights-daily/          # AI 动态洞察生成器
├── ai-insights-daily-workspace/# AI 洞察工作区
├── algorithmic-art/            # 算法艺术
├── brand-guidelines/           # 品牌指南
├── canvas-design/              # 画布设计
├── book-chapter-writer/        # 技术书籍章节写作
├── doc-coauthoring/            # 文档协作
├── frontend-design/            # 前端设计
├── internal-comms/             # 内部沟通
├── mcp-builder/                # MCP 构建器
├── notebooklm/                 # NotebookLM
├── paper-writer/               # 学术论文写作
├── pdf/                        # PDF 处理
├── pdf-to-images/              # PDF 转图片
├── polymarket-trading-bot/     # Polymarket 复制交易机器人
├── remotion/                   # Remotion 视频创建最佳实践
├── skill-creator/              # 技能创建器
├── slack-gif-creator/          # Slack GIF 创建
├── theme-factory/              # 主题工厂
├── video-script-writer/        # 视频脚本写作
├── viral-article-creator/      # 爆文创作
├── viral-article-rewriter/     # 爆文改写器
├── web-artifacts-builder/      # Web Artifacts 构建
├── VibeSec-Skill/              # 安全编码技能
├── webapp-testing/             # Web 应用测试
├── xlsx/                       # Excel 处理
└── zt-selector/                # A股选股工具

# 符号链接（指向全局技能）
├── ai-image-generation@ -> ../../.agents/skills/ai-image-generation
├── baoyu-url-to-markdown@ -> ../../.agents/skills/baoyu-url-to-markdown
├── code-review-excellence@ -> ../../.agents/skills/code-review-excellence
├── docx@ -> ../../.agents/skills/docx
├── find-skills@ -> ../../.agents/skills/find-skills
├── pptx@ -> ../../.agents/skills/pptx
├── receiving-code-review@ -> ../../.agents/skills/receiving-code-review
└── technical-blog-writing@ -> ../../.agents/skills/technical-blog-writing
```

## 🎯 典型使用场景

### 内容创作者
```bash
# 生成 AI 技术文章
/ai-insights-daily

# 改写和优化文章
/viral-article-creator

# 写技术博客
/technical-blog-writing

# 写书籍/教程章节
/book-chapter-writer
```

### 开发者
```bash
# 浏览器自动化测试
/agent-browser

# 前端界面开发
/frontend-design

# 代码审查
/code-review-excellence
```

### 办公人员
```bash
# 处理 PDF 文档
/pdf

# 编辑 Excel 表格
/xlsx

# 制作 PPT
/pptx

# 编辑 Word 文档
/docx
```

### 模拟盘玩家
```bash
# A股涨停选股（仅供娱乐）
/zt-selector

# Polymarket 复制交易（预测市场）
/polymarket-trading-bot
```

## 🔧 技能开发

如果你想创建自己的技能：

```bash
# 使用 skill-creator 创建新技能
/skill-creator

# 或者查找现有技能
/find-skills
```

## 📝 技能文件结构

每个技能目录通常包含：
- `SKILL.md` - 技能的核心配置和文档
- `LICENSE.txt` - 许可证文件（如适用）
- 其他辅助文件（模板、字体、示例等）

## 🤝 贡献

欢迎贡献新技能或改进现有技能！

## 📄 许可证

各技能可能有不同的许可证，请查看各技能目录中的 LICENSE.txt 文件。

## 🔗 相关链接

- [Claude Code 官方文档](https://docs.anthropic.com/claude-code)
- [Claude API 文档](https://docs.anthropic.com/claude/docs)
- [Anthropic 官网](https://www.anthropic.com)

---

**最后更新**: 2026-03-13
**技能数量**: 28+
