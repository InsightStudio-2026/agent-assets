# Claude Code MCP 配置经验

> 从 VS Code Copilot 迁移 MCP 服务器到 Claude Code 的实战教训
> 日期: 2026-06-30

---

## 1. 格式差异速查

### 配置文件位置

| 平台 | 配置文件 |
|------|---------|
| VS Code Copilot | `%APPDATA%/Code/User/mcp.json` |
| Claude Code | `~/.claude.json` 的 `mcpServers` 键 |

### 字段映射

```
Copilot (mcp.json)              Claude Code (.claude.json)
──────────────────────────       ──────────────────────────
"servers": {                     "mcpServers": {
  "name": {                        "name": {
    "type": "stdio",    ← 删除       "command": "...",
    "command": "...",                "args": [...],
    "args": [...],                   "env": {...}
    "env": {...},                  }
    "disabled": true/false ← 删除
  }
```

- **`type: "stdio"`** — Claude Code 不需要，默认就是 stdio
- **`disabled`** — Claude Code 没有此字段，不想要的服务器直接不配置
- **command/args/env** — 格式完全一致，直接复制

---

## 2. 命令兼容性（致命坑）

### ❌ 不兼容写法

```json
// Copilot 能用的 cmd /c 包壳 — Claude Code 不认
{ "command": "cmd", "args": ["/c", "npx", "-y", "package"] }

// 不带扩展名的命令 — 可能解析失败
{ "command": "npx" }
{ "command": "node" }
```

### ✅ 兼容写法

```json
// 绝对路径，永远正确
{ "command": "C:/Program Files/nodejs/node.exe" }
{ "command": "C:/APP/Python313/python.exe" }
{ "command": "C:/Hub/Projects/Tools/MCP/xxx/xxx.exe" }
```

### 根因

Copilot 在 VS Code 内通过**终端 shell** 启动进程，`cmd /c` 包壳和隐式扩展名解析（`.cmd`/`.ps1`）都正常工作。

Claude Code **直接 spawn 进程**（类似 Node.js `child_process.spawn`），不经过 shell。只认 `.exe` 扩展名，不自动解析 `.cmd`/`.ps1`/`.bat`。

---

## 3. npx 启动超时

### 问题

`npx -y <package>` 首次运行需下载包（10-30 秒），Claude Code 的 MCP 启动超时在此期间触发，导致服务器静默失败——不报错、不提示，只是不出现。

### 解决方案

```powershell
# 先全局安装，消除下载延迟
npm install -g <package>

# 然后用 node.exe 直调入口文件，完全跳过 npx
```

```json
// 改前（慢，可能超时）
{ "command": "npx.cmd", "args": ["-y", "@upstash/context7-mcp", "--api-key=..."] }

// 改后（快，秒启动）
{ "command": "C:/Program Files/nodejs/node.exe",
  "args": ["C:/Users/<user>/AppData/Roaming/npm/node_modules/@upstash/context7-mcp/dist/index.js", "--api-key=..."] }
```

### 找入口文件的方法

```powershell
# 找到全局包位置
npm root -g

# 读 package.json 找到 bin 入口
Get-Content "<path>\package.json" | ConvertFrom-Json | Select-Object -ExpandProperty bin
```

---

## 4. 静默失败（无日志）

Claude Code MCP 启动失败**没有任何可见的错误提示**。服务器不出现是唯一的信号。

### 排查步骤

1. **确认文件存在**：`Test-Path <exe/js/py路径>`
2. **手工测试命令**：直接在终端跑 command + args，看是否能启动
3. **检查后端依赖**：DB 端口是否监听、API 服务是否运行
4. **用绝对路径**：把所有 `command` 改为完整绝对路径
5. **消除包装层**：`npx` → `node.exe` 直调、`cmd /c` → 去掉

---

## 5. 已验证可用的服务器模式

| 模式 | 示例 | 状态 |
|------|------|:---:|
| `.exe` 绝对路径 | `C:/.../Everything.Mcp.exe` | ✅ |
| `.exe` + args | `C:/.../github-mcp-server.exe` + `["stdio"]` | ✅ |
| `uvx` 命令 | `uvx` + `["markitdown-mcp@0.0.1a4"]` | ✅ |
| Python 绝对路径 | `C:/APP/Python313/python.exe` + `["-u", "script.py"]` | ✅ |
| Node 绝对路径 | `C:/Program Files/nodejs/node.exe` + `["script.js"]` | ✅ |
| `cmd /c npx` | — | ❌ |
| 不带扩展名的命令 | `npx`、`node`（裸名） | ⚠️ 不稳定 |

---

## 6. 迁移检查清单

从 Copilot 迁移一个 MCP 服务器到 Claude Code 时：

- [ ] 去掉 `type: "stdio"`
- [ ] 去掉 `disabled: true/false`（不需要的别加）
- [ ] `command` 改为绝对路径（`.exe` 优先，其次 `C:/Program Files/nodejs/node.exe`）
- [ ] `npx` 包 → 全局安装后用 `node.exe` 直调入口文件
- [ ] `cmd /c xxx` → 拆开，`command` 放可执行文件，`args` 放参数
- [ ] 检查脚本依赖的后端服务是否运行（DB、API 等）
- [ ] 重启 Claude Code 验证
