---
name: agent-reach
description: >
  Give your AI agent eyes to see the entire internet.
  Search and read 17 platforms: Twitter/X, Reddit, YouTube, GitHub, Bilibili,
  XiaoHongShu, Douyin, Weibo, WeChat Articles, Xiaoyuzhou Podcast, LinkedIn,
  Boss直聘, V2EX, RSS, Exa web search, and any web page.
  Zero config for 8 channels. Use when user asks to search, read, or interact
  on any supported platform, shares a URL, or asks to search the web.
  Triggers: "搜推特", "搜小红书", "看视频", "搜一下", "上网搜", "帮我查",
  "search twitter", "youtube transcript", "search reddit", "read this link",
  "B站", "bilibili", "抖音视频", "微信文章", "公众号", "微博", "V2EX",
  "小宇宙", "播客", "podcast", "LinkedIn", "Boss直聘", "招聘", "找工作",
  "web search", "research", "帮我安装".
metadata:
  openclaw:
    homepage: https://github.com/Panniantong/Agent-Reach
---

# Agent Reach — Usage Guide

Upstream tools for 17 platforms. Call them directly.

Run `agent-reach doctor` to check which channels are available.

## ⚠️ Workspace Rules

**Never create files in the agent workspace.** Use `/tmp/` for temporary output and `~/.agent-reach/` for persistent data.

## Web — Any URL

```bash
curl -s "https://r.jina.ai/URL"
```

## Web Search (Exa)

```bash
mcporter call 'exa.web_search_exa(query: "query", numResults: 5)'
mcporter call 'exa.get_code_context_exa(query: "code question", tokensNum: 3000)'
```

## Twitter/X (xreach)

```bash
xreach search "query" -n 10 --json          # search
xreach tweet URL_OR_ID --json                # read tweet (supports /status/ and /article/ URLs)
xreach tweets @username -n 20 --json         # user timeline
xreach thread URL_OR_ID --json               # full thread
```

## YouTube (yt-dlp)

```bash
yt-dlp --dump-json "URL"                     # video metadata
yt-dlp --write-sub --write-auto-sub --sub-lang "zh-Hans,zh,en" --skip-download -o "/tmp/%(id)s" "URL"
                                             # download subtitles, then read the .vtt file
yt-dlp --dump-json "ytsearch5:query"         # search
```

## Bilibili (yt-dlp)

```bash
yt-dlp --dump-json "https://www.bilibili.com/video/BVxxx"
yt-dlp --write-sub --write-auto-sub --sub-lang "zh-Hans,zh,en" --convert-subs vtt --skip-download -o "/tmp/%(id)s" "URL"
```

> Server IPs may get 412. Use `--cookies-from-browser chrome` or configure proxy.

## Reddit

```bash
curl -s "https://www.reddit.com/r/SUBREDDIT/hot.json?limit=10" -H "User-Agent: agent-reach/1.0"
curl -s "https://www.reddit.com/search.json?q=QUERY&limit=10" -H "User-Agent: agent-reach/1.0"
```

> Server IPs may get 403. Search via Exa instead, or configure proxy.

## GitHub (gh CLI)

```bash
gh search repos "query" --sort stars --limit 10
gh repo view owner/repo
gh search code "query" --language python
gh issue list -R owner/repo --state open
gh issue view 123 -R owner/repo
```

## 小红书 / XiaoHongShu (mcporter)

```bash
mcporter call 'xiaohongshu.search_feeds(keyword: "query")'
mcporter call 'xiaohongshu.get_feed_detail(feed_id: "xxx", xsec_token: "yyy")'
mcporter call 'xiaohongshu.get_feed_detail(feed_id: "xxx", xsec_token: "yyy", load_all_comments: true)'
mcporter call 'xiaohongshu.publish_content(title: "标题", content: "正文", images: ["/path/img.jpg"], tags: ["tag"])'
```

> Requires login. Use Cookie-Editor to import cookies.

## 抖音 / Douyin (mcporter)

```bash
mcporter call 'douyin.parse_douyin_video_info(share_link: "https://v.douyin.com/xxx/")'
mcporter call 'douyin.get_douyin_download_link(share_link: "https://v.douyin.com/xxx/")'
```

> No login needed.

## 微信公众号 / WeChat Articles

**Search** (miku_ai):
```python
python3 -c "
import asyncio
from miku_ai import get_wexin_article
async def s():
    for a in await get_wexin_article('query', 5):
        print(f'{a[\"title\"]} | {a[\"url\"]}')
asyncio.run(s())
"
```

**Read** (Camoufox — bypasses WeChat anti-bot):
```bash
cd ~/.agent-reach/tools/wechat-article-for-ai && python3 main.py "https://mp.weixin.qq.com/s/ARTICLE_ID"
```

> WeChat articles cannot be read with Jina Reader or curl. Must use Camoufox.

## 小宇宙播客 / Xiaoyuzhou Podcast (groq-whisper + ffmpeg)

```bash
# 转录单集播客（输出文本到 /tmp/）
~/.agent-reach/tools/xiaoyuzhou/transcribe.sh "https://www.xiaoyuzhoufm.com/episode/EPISODE_ID"
```

> 需要 ffmpeg + Groq API Key（免费）。
> 配置 Key：`agent-reach configure groq-key YOUR_KEY`
> 首次运行需安装工具：`agent-reach install --env=auto`
> 运行 `agent-reach doctor` 检查状态。
> 输出 Markdown 文件默认保存到 `/tmp/`。


## LinkedIn (mcporter)

```bash
mcporter call 'linkedin.get_person_profile(linkedin_url: "https://linkedin.com/in/username")'
mcporter call 'linkedin.search_people(keyword: "AI engineer", limit: 10)'
```

Fallback: `curl -s "https://r.jina.ai/https://linkedin.com/in/username"`

## Boss直聘 (mcporter)

**用途**：招聘/求职相关操作，获取推荐候选人、发送问候等。
**状态**：需要本地 MCP 服务器运行（http://localhost:8000）
**检测**：运行 `agent-reach doctor` 查看 Boss直聘 状态

### 启动服务器

服务器源码位置：`/Users/mima0000/Desktop/repos/mcp-workspace/mcp-servers/bosszhipin/`

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
cporter call 'bosszhipin.get_recommend_jobs_tool(page: 1)' --output json

# 向候选人发送问候
mcporter call 'bosszhipin.send_greeting_tool(candidate_id: "xxx", message: "您好...")' --output json
```

### 使用场景

| 用户请求 | 操作 |
|---------|------|
| "帮我启动 Boss 直聘" | 启动服务器：`python boss_zhipin_fastmcp_v2.py` |
| "看看有没有推荐的候选人" | `mcporter call 'bosszhipin.get_recommend_jobs_tool(page: 1)'` |
| "给这个候选人发个问候" | `mcporter call 'bosszhipin.send_greeting_tool(...)'` |

### 故障排除

| 问题 | 解决方案 |
|------|---------|
| 连接失败 | 确认服务器已启动：`curl http://localhost:8000` |
| 登录超时 | 检查 Chrome CDP 是否正常启动 |
| Cookie 过期 | 重新执行 `bosszhipin.login_full_auto` |


## V2EX (public API)

```bash
# 热门主题
curl -s "https://www.v2ex.com/api/topics/hot.json" -H "User-Agent: agent-reach/1.0"

# 节点主题（node_name 如 python、tech、jobs、qna）
curl -s "https://www.v2ex.com/api/topics/show.json?node_name=python&page=1" -H "User-Agent: agent-reach/1.0"

# 主题详情（topic_id 从 URL 获取，如 https://www.v2ex.com/t/1234567）
curl -s "https://www.v2ex.com/api/topics/show.json?id=TOPIC_ID" -H "User-Agent: agent-reach/1.0"

# 主题回复
curl -s "https://www.v2ex.com/api/replies/show.json?topic_id=TOPIC_ID&page=1" -H "User-Agent: agent-reach/1.0"

# 用户信息
curl -s "https://www.v2ex.com/api/members/show.json?username=USERNAME" -H "User-Agent: agent-reach/1.0"
```

Python 调用示例（V2EXChannel）：

```python
from agent_reach.channels.v2ex import V2EXChannel

ch = V2EXChannel()

# 获取热门帖子（默认 20 条）
# 返回字段：id, title, url, replies, node_name, node_title, content(前200字), created
topics = ch.get_hot_topics(limit=10)
for t in topics:
    print(f"[{t['node_title']}] {t['title']} ({t['replies']} 回复) {t['url']}")
    print(f"  id={t['id']} created={t['created']}")

# 获取指定节点的最新帖子
# 返回字段：id, title, url, replies, node_name, node_title, content(前200字), created
node_topics = ch.get_node_topics("python", limit=5)
for t in node_topics:
    print(t["id"], t["title"], t["url"])

# 获取单个帖子详情 + 回复列表
# 返回字段：id, title, url, content, replies_count, node_name, node_title,
#           author, created, replies (list of {author, content, created})
topic = ch.get_topic(1234567)
print(topic["title"], "—", topic["author"])
for r in topic["replies"]:
    print(f"  {r['author']}: {r['content'][:80]}")

# 获取用户信息
# 返回字段：id, username, url, website, twitter, psn, github, btc, location, bio, avatar, created
user = ch.get_user("Livid")
print(user["username"], user["bio"], user["github"])

# 搜索（V2EX 公开 API 不支持，会返回说明信息）
result = ch.search("asyncio")
print(result[0]["error"])  # 提示使用站内搜索或 Exa channel
```

> No auth required. Results are public JSON. V2EX 节点名见 https://www.v2ex.com/planes

## RSS (feedparser)

```python
python3 -c "
import feedparser
for e in feedparser.parse('FEED_URL').entries[:5]:
    print(f'{e.title} — {e.link}')
"
```

## Troubleshooting

- **Channel not working?** Run `agent-reach doctor` — shows status and fix instructions.
- **Twitter fetch failed?** Ensure `undici` is installed: `npm install -g undici`. Configure proxy: `agent-reach configure proxy URL`.
- **Boss直聘 not available?** Check if local MCP server is running: `curl http://localhost:8000`

## Setting Up a Channel ("帮我配 XXX")

If a channel needs setup (cookies, Docker, etc.), fetch the install guide:
https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md

User only provides cookies. Everything else is your job.
