---
name: obsidian-vault
description: >
  搜索、创建和管理 Obsidian vault 笔记，使用 wikilinks 与 index notes。
  Use when user wants to find/create/organize notes in Obsidian, or asks 管理 Obsidian/查笔记/新建笔记。
---

# Obsidian 知识库（obsidian-vault）

## Vault 位置

`/mnt/d/Obsidian Vault/AI Research/`

这是个人 vault 路径，且目前是 WSL 风格路径。若当前环境无法访问，先向用户确认最新路径。根层级基本保持扁平。

## 命名约定

- **Index notes**：聚合相关主题，例如 `Ralph Wiggum Index.md`、`Skills Index.md`、`RAG Index.md`。
- **所有 note 名称使用 Title Case**。
- **不要用文件夹组织内容**：使用 links 与 index notes。

## 链接

- 使用 Obsidian `[[wikilinks]]` 语法：`[[Note Title]]`。
- 每篇 note 底部链接依赖 / 相关 notes。
- Index notes 只是 `[[wikilinks]]` 列表。

## 工作流

### 搜索 notes

优先使用 IDE / 代理提供的文件名搜索与全文搜索工具，并把搜索范围限定到 vault 路径。

PowerShell 示例：

```powershell
$VaultPath = "/mnt/d/Obsidian Vault/AI Research/"

Get-ChildItem -Path $VaultPath -Filter "*.md" -File | Where-Object { $_.Name -match "keyword" }
Get-ChildItem -Path $VaultPath -Filter "*.md" -File | Select-String -Pattern "keyword"
```

也可以直接在 vault 路径上使用 Grep / Glob 工具。

### 创建新 note

1. 文件名使用 **Title Case**。
2. 把内容写成一个学习单元，遵守 vault 规则。
3. 在底部添加指向相关 notes 的 `[[wikilinks]]`。
4. 若属于编号序列，使用层级编号方案。

### 查找相关 notes

在 vault 中搜索 `[[Note Title]]` 以找到 backlinks：

```powershell
$VaultPath = "/mnt/d/Obsidian Vault/AI Research/"
Get-ChildItem -Path $VaultPath -Filter "*.md" -File | Select-String -Pattern "\[\[Note Title\]\]"
```

### 查找 index notes

```powershell
$VaultPath = "/mnt/d/Obsidian Vault/AI Research/"
Get-ChildItem -Path $VaultPath -Filter "*Index*" -File
```
