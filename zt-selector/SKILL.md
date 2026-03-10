---
name: zt-selector
description: A-share stock selection tool for simulated trading entertainment. Analyzes stocks using 5 key criteria including K-line trends, recent limit-up boards, sector momentum, and index analysis. Triggers when users mention limit-up stock selection, A-share stock picking, intraday trading stocks, end-of-day stock selection, or any variation of "涨停选股", "敢死队选股", "尾盘选股", "今日选股", or "zt-selector". Use this skill whenever users want to find potential A-share stocks to watch for simulated trading accounts, especially around 14:30 market close time.
---

# 涨停敢死队选股技能

帮助用户基于akshare数据源进行A股模拟盘选股，使用5大规则筛选当日尾盘可关注的潜在标的。,执行时间为每个交易日的14:30开始寻找标的.

## 选股逻辑（6大规则）

0. **个股过滤** - 去除科创板（688开头），去除ST股票，去除市值5000亿以上的个股
1. **K线上扬趋势** - 当前价 > MA5 > MA20
2. **近期强势表现** - 15个交易日内有涨停记录
3. **近5个交易日红肥绿瘦** - 上涨天数 > 下跌天数
4. **市盈率展示** - 查看并展示市盈率（辅助判断）
5. **板块共振效应** - 所属板块当日有3只以上涨停股票
6. **大盘环境判断** - 上证指数技术面分析（MA5与MA10对比）

**未来规划**：
- 基本面数据接口 - 财报数据接口（待实现）

## 工作流程

### 第一步：环境准备

确保akshare和pandas已安装：

```bash
pip install akshare pandas -q
```

### 第二步：生成选股脚本

使用Read工具读取 `scripts/zt_selector_fast.py` 脚本，然后将其写入用户当前工作目录：

```bash
cp ~/.claude/skills/zt-selector/scripts/zt_selector_fast.py ./zt_selector_fast.py
```

或者直接使用Read读取脚本内容后用Write工具写到当前目录。

### 第三步：执行选股

运行选股脚本：

```bash
python zt_selector_fast.py
```

脚本会自动完成以下步骤：
1. 分析上证指数当前趋势
2. 获取今日涨停池，识别热门板块（≥3只涨停）
3. 从热门板块中筛选股票池
4. 逐个分析K线趋势和涨停记录
5. 输出符合5大规则的股票列表

### 第四步：结果展示

将选股结果以清晰的表格形式展示给用户，包括：

#### 📊 大盘状态
- 上证指数当前点位
- MA5 / MA10 数值
- 趋势预判（看涨/看跌）

#### 🔥 热门板块
- 板块名称
- 今日涨停股票数量

#### 📈 符合条件股票（按涨停次数排序）
- 股票代码和名称
- 所属行业
- 10日涨停次数
- MA5/MA10/MA20数值
- 当前价格
- 市盈率
- 近5日涨跌情况

#### 💡 重点关注
突出显示10日涨停次数最多的股票，说明为什么它们值得模拟盘关注。

#### ⚠️ 风险提示
提醒用户：
- 仅供模拟盘娱乐使用
- 不构成投资建议
- 大盘偏弱时需谨慎
- 14:30尾盘建议观察成交量和资金流向

## 输出格式示例

```
🎯 今日选股结果（2026-03-10）

📊 大盘状态
上证指数: 4096.60
MA5: 4106.90 | MA10: 4129.13
预判: 看跌 ⚠️

🔥 热门板块（今日涨停≥3只）
- 通用设备: 6只涨停
- 元件: 4只涨停

📈 符合条件股票（共20只）
[表格显示...]

💡 模拟盘重点关注
- 开山股份(300257) - 10日内3次涨停，通用设备板块
- 欧科亿(688308) - 2次涨停，均线多头排列标准

⚠️ 风险提示
- 仅供模拟盘娱乐使用，不构成投资建议
- 股市有风险，投资需谨慎
- ⚠️ 大盘今日MA5 < MA10，偏弱，尾盘操作需谨慎
- 14:30尾盘建议观察成交量和资金流向
```

## 可定制参数

用户可以要求调整以下参数：
- **选股数量限制** - 默认20只，可调整
- **涨停阈值** - 默认9.9%（创业板/科创板为20%）
- **板块涨停数要求** - 默认≥3只，可调整
- **均线周期** - 默认MA5/MA10/MA20

## 注意事项

1. **数据时效性** - akshare数据通常有几分钟延迟，建议14:00-14:30之间运行
2. **运行时间** - 首次运行需要5-10分钟（取决于热门板块数量）
3. **仅供娱乐** - 明确告知用户这是模拟盘工具，不构成任何投资建议
4. **大盘判断** - 如果上证指数预判为"看跌"，特别强调风险提示

## 常见问题处理

- **网络错误** - akshare依赖网络接口，如遇网络问题建议稍后重试
- **今日无涨停** - 如果今日涨停股票<10只，可能无符合条件板块，提示用户等待更好时机
- **筛选结果为空** - 说明市场环境不佳或规则过严，建议调整筛选条件

## 脚本文件位置

核心选股脚本位于：`~/.claude/skills/zt-selector/scripts/zt_selector_fast.py`
