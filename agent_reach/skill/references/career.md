# 职场招聘

Boss直聘、LinkedIn。

## Boss直聘

**用途**: 招聘/求职相关操作，获取推荐候选人、发送问候等。
**状态**: 需要本地 MCP 服务器运行 (http://localhost:8000)

### 启动服务器

服务器源码位置: `/Users/mima0000/Desktop/repos/mcp-workspace/mcp-servers/bosszhipin/`

```bash
# 方式 1：直接启动
cd /Users/mima0000/Desktop/repos/mcp-workspace/mcp-servers/bosszhipin
python boss_zhipin_fastmcp_v2.py

# 方式 2：Docker 启动（推荐）
cd /Users/mima0000/Desktop/repos/mcp-workspace/mcp-servers/bosszhipin
docker-compose up -d

# 方式 3：后台常驻
nohup python boss_zhipin_fastmcp_v2.py > boss_mcp.log 2>&1 &
```

### 环境变量（可选但推荐）

```bash
# 连接本地 Chrome CDP（绕过风控）
export BOSS_CHROME_CDP_URL="http://localhost:9222"

# 登录态持久化路径
export BOSS_STATE_PATH="/Users/mima0000/Desktop/repos/mcp-workspace/mcp-servers/bosszhipin/data/state.json"

# 使用持久化浏览器 Profile
export BOSS_USE_PERSISTENT_CONTEXT="true"
export BOSS_USER_DATA_DIR="/Users/mima0000/Desktop/repos/mcp-workspace/mcp-servers/bosszhipin/data/browser_profile"
```

### 启动 Chrome CDP（推荐）

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome_dev_profile
```

### MCP 调用方式

确保服务器在 `http://localhost:8000` 运行，然后：

```bash
# 检查登录状态
mcporter call 'bosszhipin.get_login_info_tool()' --output json

# 全自动登录（二维码+验证）
mcporter call 'bosszhipin.login_full_auto()' --output json

# 获取推荐候选人
mcporter call 'bosszhipin.get_recommend_jobs_tool(page: 1)' --output json

# 向候选人发送问候
mcporter call 'bosszhipin.send_greeting_tool(candidate_id: "xxx", message: "您好...")' --output json
```

### 使用场景

| 用户请求 | 操作 |
|---------|------|
| "帮我启动 Boss 直聘" | 启动服务器 |
| "看看有没有推荐的候选人" | `get_recommend_jobs_tool` |
| "给这个候选人发个问候" | `send_greeting_tool` |

### 故障排除

| 问题 | 解决方案 |
|------|---------|
| 连接失败 | 确认服务器已启动：`curl http://localhost:8000` |
| 登录超时 | 检查 Chrome CDP 是否正常启动 |
| Cookie 过期 | 重新执行 `bosszhipin.login_full_auto` |

## LinkedIn

```bash
# 获取个人资料
mcporter call 'linkedin-scraper.get_person_profile(linkedin_url: "https://linkedin.com/in/username")'

# 搜索人才
mcporter call 'linkedin-scraper.search_people(keyword: "AI engineer", limit: 10)'

# 获取公司资料
mcporter call 'linkedin-scraper.get_company_profile(linkedin_url: "https://linkedin.com/company/xxx")'

# 搜索职位
mcporter call 'linkedin-scraper.search_jobs(keyword: "software engineer", limit: 10)'
```

> **需要登录**: LinkedIn scraper 需要有效的登录态。

### Fallback 方案

如果 MCP 不可用，可以用 Jina Reader：

```bash
curl -s "https://r.jina.ai/https://linkedin.com/in/username"
```
