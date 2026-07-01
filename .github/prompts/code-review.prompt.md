---
name: code-review
description: 对代码变更进行结构化审查——正确性、安全性、性能、可维护性、协议合规。
argument-hint: '[commit | branch | PR 基准]'
agent: code-reviewer
---

# 代码审查

审查指定基准以来的代码变更。

严格按 `.github/skills/review/SKILL.md` 协议：

1. 固定比较基准（`git diff<base>...HEAD`）
2. 逐文件审查 Standards / Spec / Verification 三轴
3. 命中高风险时追加 Risk Gates / Architecture / Operability / Authorship 四轴
4. 按 Critical > High > Medium > Low 输出结构化报告

基准：${input:baseRef}
