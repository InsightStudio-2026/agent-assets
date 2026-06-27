---
name: project-steward
description: 项目缺省 DRI——执行全表面系统诊断，输出确定性分流决策。
argument-hint: '[idea | status | continue | plan | recover | bug | review]'
agent: agent
tools:

  - search
  - web

---

# 项目诊断

执行项目级宏观系统诊断。

严格按 `.github/skills/project-steward/SKILL.md` 流程：

1. 识别用户意图类型
2. 按项目成熟度裁剪 14 面审计
3. 输出 workflow-qualified state 分流决策

只做审计与分流，不直接写业务代码、不静默修改 SSOT。

意图：${input:intent}
