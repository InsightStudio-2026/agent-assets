---
name: specs-write
description: 将模糊需求转化为可审查、可实现、可验证的分阶段规格合同。
argument-hint: '[feature 简述或需求描述]'
agent: agent
tools:

  - search
  - web

---

# 编写 Spec

将以下需求编写为完整的 Spec 合同。

严格按 `.github/skills/specs-write/SKILL.md` 的 Phase 1-8 步进执行：
charter → audit → decisions → requirements → design → tasks → handoff。

只写 Spec，不写业务代码、不执行迁移、不改真实数据库。
输出落于 `docs/specs/active/<feature-slug>/`。

需求：${input:requirement}
