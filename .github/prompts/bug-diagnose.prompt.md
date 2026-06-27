---
name: bug-diagnose
description: 纪律化缺陷诊断——复现、定位、根因、修复、预防五步闭环。
argument-hint: '[bug 描述或错误信息]'
agent: agent
---

# 缺陷诊断

诊断并修复指定缺陷。

严格按 `.github/skills/diagnose/SKILL.md` 协议：

1. 复现 → 收集完整错误信息，写最小复现用例
2. 定位 → 二分法缩小范围，检查测试覆盖
3. 根因 → 区分逻辑/数据/契约错误，评估影响面
4. 修复 → TDD（先写复现测试 → 最小修复 → 清理）
5. 预防 → 补测试、加强门禁

追根因，不治标——不以扩大 catch、吞错、重试掩盖。

Bug：${input:bugDescription}
