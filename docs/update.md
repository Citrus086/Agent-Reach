# Agent Reach — Update Guide

## 关于本分支的自定义更新

> ⚠️ **注意**：这是 `Citrus086/Agent-Reach` 的自定义分支，在官方版本基础上增加了以下功能：
> 
> - ✅ **保留 Boss直聘检测** - 官方已移除，本分支保留 `bosszhipin` doctor 检测
> - ✅ **新增 `agent-reach update` 命令** - 自动合并上游更新，保留自定义功能
> - ✅ **完整渠道支持** - 微博、V2EX、小宇宙播客等全部 16 个渠道

### 两种更新方式

#### 方式 1：保留自定义功能（推荐）

```bash
agent-reach update
```

此命令会：
1. 自动提交未保存的本地更改（如果有）
2. 获取 upstream 最新代码
3. 合并到当前分支，**保留 bosszhipin 等自定义功能**
4. 由于是 Editable 安装，无需重新 pip install

#### 方式 2：纯净官方版本

```bash
pip install --upgrade https://github.com/Panniantong/agent-reach/archive/main.zip
```

⚠️ **警告**：此命令会完全替换为官方最新版，**丢失 Boss直聘检测等自定义功能**。

---

## For Humans

Copy this to your AI Agent:

```
帮我更新 Agent Reach：https://raw.githubusercontent.com/Citrus086/Agent-Reach/my-version/docs/update.md
```

Or in English:

```
Update Agent Reach: https://raw.githubusercontent.com/Citrus086/Agent-Reach/my-version/docs/update.md
```

---

## For AI Agents

### ⚠️ Workspace Rules

**Never create files, clone repos, or run commands in the agent workspace.** Use `/tmp/` for temporary work and `~/.agent-reach/` for persistent data.

### Goal

Update Agent Reach to the latest version, then verify everything still works.

### Step 1: Check current version

```bash
agent-reach check-update
```

If it says "已是最新版本", you're done — tell the user.

### Step 2: Update (Choose one method)

#### Method A: Preserve Custom Features (Recommended)

Use the custom `update` command to merge upstream changes while keeping bosszhipin and other custom channels:

```bash
agent-reach update
```

To preview what will be updated without making changes:

```bash
agent-reach update --dry-run
```

#### Method B: Clean Official Version

⚠️ **Warning**: This will remove bosszhipin channel detection and other custom features.

```bash
pip install --upgrade https://github.com/Panniantong/agent-reach/archive/main.zip
```

### Step 3: Verify

```bash
agent-reach version
agent-reach doctor
```

Report the new version and channel status to the user. If any channel changed status (was ✅ now ❌), investigate and fix.

Expected channels in this fork (16 total):
- Zero-config: 网页, YouTube, RSS, GitHub(公开), 微信公众号, 微博, V2EX
- With setup: Twitter, B站, Reddit, 小红书, 抖音, LinkedIn, Boss直聘, 小宇宙播客, Exa搜索

### Step 4: Update SKILL.md (if installed)

If the user has the Agent Reach skill installed, update it too:

```bash
agent-reach install --skill-only
```

If the `--skill-only` flag is not available, manually copy the latest SKILL.md:

```bash
python3 -c "
import importlib.resources, shutil, os
skill = importlib.resources.files('agent_reach').joinpath('skill', 'SKILL.md').read_text()
for d in [os.path.expanduser('~/.openclaw/skills/agent-reach'),
          os.path.expanduser('~/.claude/skills/agent-reach')]:
    if os.path.isdir(d):
        with open(os.path.join(d, 'SKILL.md'), 'w') as f:
            f.write(skill)
        print(f'✅ Updated: {d}')
"
```

Done. Tell the user what version they're now on and how many channels are available.

---

## Custom Features in This Fork

### 1. Boss直聘 Channel Detection

Official repo removed bosszhipin in PR #135. This fork keeps it:

```bash
agent-reach doctor
# Output: ✅ Boss直聘职位搜索 — 完整可用
```

Requirements:
- mcporter installed
- bosszhipin MCP configured: `mcporter config add bosszhipin http://localhost:8000/mcp`

### 2. Custom Update Command

The `agent-reach update` command provides a safer way to get upstream updates:

- ✅ Auto-commits local changes before merging
- ✅ Fetches and merges upstream/main
- ✅ Preserves custom channels (bosszhipin, etc.)
- ✅ Handles merge conflicts with clear instructions
- ✅ No need to re-run pip install (editable mode)

### 3. Full Channel Support

This fork includes all channels from upstream plus preserved custom ones:

| Channel | Status | Notes |
|---------|--------|-------|
| Boss直聘 | ✅ Preserved | Officially removed, kept in this fork |
| 微博 | ✅ Available | From upstream |
| V2EX | ✅ Available | From upstream |
| 小宇宙播客 | ✅ Available | From upstream |
| 微信公众号 | ✅ Available | Enhanced version from upstream |
| + 11 more | ✅ Available | Standard upstream channels |

---

## Troubleshooting

### "agent-reach update" not found

Make sure you're using the version from this fork:

```bash
agent-reach --help | grep update
```

Should show: `update  Update Agent Reach from upstream (preserves custom changes)`

### Merge conflicts during update

If `agent-reach update` reports conflicts:

1. Check conflicted files: `git diff --name-only --diff-filter=U`
2. Edit files to resolve `<<<<<<< HEAD` / `=======` / `>>>>>>> upstream/main` markers
3. `git add <conflicted-files>`
4. `git commit -m "resolve merge conflicts"`

Or abort: `git merge --abort`

### Want to switch to official version?

```bash
pip uninstall agent-reach -y
pip install https://github.com/Panniantong/agent-reach/archive/main.zip
```

⚠️ This will lose bosszhipin detection and other custom features.
