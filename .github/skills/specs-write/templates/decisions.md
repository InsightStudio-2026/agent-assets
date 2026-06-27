# decisions.md 模板

> **When to read**: 在 `/specs-write` 步进 4 (Decisions) 进行深度拷问与关键决策定盘时读取本模板。本阶段是将游离态想法（`docs/Idea.md`）和现状审计（`audit.md`）结合进行的高压压测定盘。

## 步进 4 (Decisions) 决策硬规则（落 decisions.md 前必读）

- **双端输入**：必须综合用户的原始构想（游离态 Idea）和 步进 3 (Audit) 的 `audit.md` 中的技术债与冲突约束。
- **拷问必闭环**：所有的决策点必须通过 `grill-me` 与用户确认，完成从 `[ ]` 到 `[x]` 的全封闭定盘，不可留下模糊地带。
- **不可动摇的基准**：本文件一旦定盘，将成为后续 步进 5 (Requirements) 与 步进 6 (Design) 的事实源，后续步骤不得擅自推翻本文件的架构折中。

---

## Key Decisions & Architectural Blueprint — `<Feature Name>`

Feature Slug: `<feature-slug>`
Charter Ref: charter.md
Audit Ref: audit.md (若有)

## 1. 原点愿景 (Idea Anchor)

> <将游离态 `docs/Idea.md` 中的核心诉求与愿景搬迁至此>

## 2. 审计与现状摩擦 (Audit Context)

- **核心技术债与冲突**：<列出 audit.md 中发现的影响本方案的阻碍和限制>
- **边界约束**：<由于上述技术债，我们必须做出的业务或技术让步>

## 3. 核心拷问与折中 (Grill-me & Trade-offs)

> 本节记录对本特性的深度压测与关键选择。所有的决策点必须获得用户的明确共识。

### 3.1 拷问决策树状态

- `[x]` [D-1: <决策点名称>] (L-DESIGN) -> 决议: <选择的方案>
- `[x]` [D-2: <决策点名称>] (L-STRAT) -> 决议: <选择的方案>
- `[x]` [D-3: <决策点名称>] (L-IMPL) -> 决议: <选择的方案>

### 3.2 决策过程详情

#### [D-1] <决策点名称>

- **面临的挑战**：<为什么需要做这个决定？>
- **备选方案 A**：<描述> (代价: ...)
- **备选方案 B**：<描述> (代价: ...)
- **最终拍板**：<记录最终选择及理由>

## 4. 最终架构蓝图与业务定盘 (Final Blueprint)

- **核心定盘 1**：<确立下来的业务流转或核心设计原则>
- **核心定盘 2**：<同上>
- **后续派生指引**：<给 步进 5 Requirements 和 步进 6 Design 划定的设计与功能框框>
