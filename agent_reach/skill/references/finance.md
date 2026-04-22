# 金融 & 股票

雪球股票行情、社区热帖、热门排行。

## 雪球 / Xueqiu

```python
from agent_reach import AgentReach
reach = AgentReach()

# 获取实时行情
reach.get_stock_quote("SH600519")

# 搜索股票
reach.search_stock("茅台", limit=5)

# 热门帖子
reach.get_hot_posts(limit=10)

# 热门股票排行
reach.get_hot_stocks(limit=10, stock_type=10)
```

### 股票代码格式

| 市场 | 前缀 | 示例 |
|------|------|------|
| 沪市 | SH | SH600519 |
| 深市 | SZ | SZ000858 |
| 港股 | 无 | 00700 |
| 美股 | 无 | AAPL |

### Cookie 配置（可选）

雪球公开 API 大部分无需登录即可使用。若遇到 400016 错误（需要登录态），可配置 cookie：

```bash
# 从浏览器开发者工具复制 xq_a_token 的值
agent-reach configure xueqiu_cookie "xq_a_token=YOUR_TOKEN"
```

优先级：
1. 配置的 `xueqiu_cookie`
2. 浏览器自动提取（rookiepy / browser_cookie3）
3. 匿名 session（访问首页获取）

### 返回字段说明

**`get_stock_quote`** 返回：
```python
{
  "symbol": "SH600519",
  "name": "贵州茅台",
  "current": 1688.88,      # 当前价
  "percent": 1.23,         # 涨跌幅 %
  "chg": 20.5,             # 涨跌额
  "high": 1700.0,          # 最高价
  "low": 1670.0,           # 最低价
  "open": 1675.0,          # 开盘价
  "last_close": 1668.38,   # 昨收
  "volume": 12345,         # 成交量
  "amount": 20800000,      # 成交额
  "market_capital": 2.1e12,# 市值
  "turnover_rate": 0.01,   # 换手率
  "pe_ttm": 28.5,          # 市盈率 TTM
  "timestamp": 1700000000
}
```

**`get_hot_stocks`** 的 `stock_type`：
- `10` = 人气榜（默认）
- `12` = 关注榜

### 注意事项

> **公开 API**：雪球行情接口是公开的，无需认证即可调用。
>
> **频率限制**：匿名访问可能有频率限制，频繁调用时建议配置 cookie。
>
> **社区帖子**：`get_hot_posts` 返回的 `text` 字段已去除 HTML 标签，长度截断至 200 字符。
