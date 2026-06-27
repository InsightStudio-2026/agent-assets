# 外部来源审计凭证 · greensock/gsap-skills

## 1. 资产来源

| 属性 | 具体值 |
| ------ | -------- |
| 来源名称 | `greensock/gsap-skills` |
| 本地参考路径 | `外部参考/gsap-skills-main/` |
| 来源类型 | 外部 skill 参考仓库 |
| 引入模式 | 直接迁移与整合 (MIT 协议) |
| 目标策略 | 直接导入本地 + 本地索引登记 |
| 获取时间 | 2026-05-29 |
| 获取人 | 代理 Cascade（受用户委托） |

## 2. 协议兼容性

- **原始协议**: MIT (宽松、商业友好)
- **兼容情况**: 与本地项目完全兼容
- **用户裁决**: 用户于 2026-05-29 明确批准（原话：“直接搬迁，做好windsurf及本地适配化即可”）
- **已执行动作**: 成功将 `外部参考/gsap-skills-main/skills/gsap-*` 下的 8 个活跃 skill 目录完整拷贝到本地启用路径 `.github/skills/` 下。

## 3. 已吸收的 Skill 目录映射

| 技能名称 | 本地启用路径 | 本地状态 | 角色 | 核心描述 |
| ---------- | -------------- | ---------- | ------ | ---------- |
| `gsap-core` | `.github/skills/gsap-core/SKILL.md` | 已启用 | Active | GSAP 核心 API 指南 (补间, 缓动, 交错, 默认值) |
| `gsap-timeline` | `.github/skills/gsap-timeline/SKILL.md` | 已启用 | Active | 动画编排、时间轴嵌套与播放控制 |
| `gsap-scrolltrigger` | `.github/skills/gsap-scrolltrigger/SKILL.md` | 已启用 | Active | 滚动联动动画与元素固定 (pinning) |
| `gsap-plugins` | `.github/skills/gsap-plugins/SKILL.md` | 已启用 | Active | SplitText, ScrollSmoother, Flip 等高级插件使用 |
| `gsap-utils` | `.github/skills/gsap-utils/SKILL.md` | 已启用 | Active | clamp, mapRange, snap 等实用计算辅助函数 |
| `gsap-react` | `.github/skills/gsap-react/SKILL.md` | 已启用 | Active | useGSAP 钩子、ref 绑定与 React 组件销毁清理 |
| `gsap-performance` | `.github/skills/gsap-performance/SKILL.md` | 已启用 | Active | 优先使用位移属性与 will-change 优化动画性能 |
| `gsap-frameworks` | `.github/skills/gsap-frameworks/SKILL.md` | 已启用 | Active | Vue 与 Svelte 生命周期下的 GSAP 作用域托管与销毁 |

## 4. 本地适配与集成

1. **[AGENTS.md 索引登记]**: 已经在顶级注册表 `AGENTS.md` 中为全部 8 个 GSAP 技能补充了其中文译名、活跃角色与本地化功能描述。
2. **[Windsurf 原生激活]**: 技能直接置于平铺的 `.github/skills/` 下，符合 Windsurf 自动发现契约。
3. **[删除第三方冗余工具]**: 排除了外部原有的平台专属配置文件（如 `.claude-plugin`, `.cursor-plugin`），使仓库专属于 Windsurf 运行环境。

## 5. 验证

| 检查项 | 预期标准 | 实际结果 |
| ------- | ---------- | ---------- |
| 目标目录完整度 | `.github/skills/` 下已复制 8 个 gsap-* 目录 | 通过 |
| 索引登记校验 | `AGENTS.md` 中正确登载了 8 个 Active 角色的技能 | 通过 |
| 目录契约合宪性 | 启用路径不含多余的 `.github/workflows/` 等嵌套层级 | 通过 |
