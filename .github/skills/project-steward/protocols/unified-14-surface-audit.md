---
description: "全局统一的全景现状审计准则（14-Surface Full-Spectrum Audit），由你智能自决全貌裁剪与审查深度。拓扑序贯式五阶审计（含 NFR 与生命周期）。"
---

# Unified 14-Surface Audit (统一 14 面全景现状审计)

**适用范围**：本审计标准是项目级别的极致深广审计准则。供 `/project-steward`（项目首席责任人诊断时）和 `/specs-write`（Feature Spec 派生时）等高级工作流共用。

**智能自决范围**：

- 在 **Project DRI 宏观诊断 (/project-steward)**模式下：由你自主判断哪些表面存在技术债务、缺失或与战略发生偏差，可执行部分面的抽查（Scoped Full-Surface Audit）或触发完整的 14 面审计（Full-Surface Audit），以判定项目的阻塞和演进方向。
- 在**Spec 派生 (/specs-write Phase 1.5)**模式下：必须在“本 Feature 影响面所及的范围”内执行严格的 14 面审计（Feature-Scoped 14 面），以保证派生设计的安全性、强证据性和生产就绪性。

---

## 拓扑序贯式五阶审计 (Topology-Ordered 5-Phase Audit)

>**核心原则**：审计并非平行的清单打勾，而是具有严格依赖关系的**有向无环图 (DAG)**。必须从第一阶（锚点）向下钻取，前一阶的断裂将直接阻断后续阶的审计。
> **工具硬指令**：带有 `[强证据]` 标签的面必须使用真实工具 (MCP / CLI) 进行实时拉取或阅读，**严禁**使用 `grep` 或推测。

### 第一阶：锚点基准 (The Anchor)

必须首先确立当前项目的指导思想和历史上下文。如果锚点缺失，审计即刻阻断。

| 面 | 属性 | 核心核验法则 (Verification Checklist) | 预期 Evidence 输出范例 | 深挖与阻断法则 (Drill-down & Block) |
| ---- | ------ | --------------------------------------- | ------------------------ | ------------------------------------- |
| **1. 文档 SSOT 面** | `[强证据]` | 1. 精读 L1 SSOT 和 active/done specs。<br/>2. 验证当前用户需求与已有母本的方向一致性。<br/>3. 检查是否有架构决策记录 (ADR) 作为依据。 | `audit-evidence/ssot_survey.txt` | 若母本严重不健康或缺失，立即触发 `BLOCKED_SSOT_REPAIR` 阻断全域审计，路由回 `/project-steward` 或 `/project-inception`。 |
| **2. 历史面** | 基础 | 1. 扫描 Project Archives 归档历史。`<br/>`2. 识别曾被废弃或回滚的技术方案。<br/>3. 审查旧任务中的遗留 TODO 或已知缺陷。 | `audit-evidence/history.txt` | 发现旧废弃方案与当前计划重合时，标记为极高风险，必须追问放弃原因。 |

### 第二阶：底层事实 (The Foundation)

确立了锚点后，必须对齐底层数据和模块架构。代码只是现象，数据和架构才是本质。

| 面 | 属性 | 核心核验法则 (Verification Checklist) | 预期 Evidence 输出范例 | 深挖与阻断法则 (Drill-down & Block) |
| ---- | ------ | --------------------------------------- | ------------------------ | ------------------------------------- |
| **3. 真实数据库面** | `[强证据]` | 1. 必用真工具(MCP)跑 `SELECT * LIMIT 1` 或 `PRAGMA table_info`。<br/>2. 校验关键表的核心索引与约束是否真实存在。<br/>3. 检查落盘数据的真实类型与预期是否相符。 | `audit-evidence/db_readback.txt` | 发现真实结构与静态 Schema 不符时（Drift），以真实数据库为唯一真相，必须停止向下审计并报告 Drift Debt。 |
| **4. 数据静态面** | 基础 | 1. 检查 schema.sql 或 ORM Model 定义。`<br/>`2. 验证 migration history 是否连续且不可变。<br/>3. 检查是否有合理的 seed/fixture 脚本。 | `audit-evidence/data_static.txt` | 缺少 Migration 记录直接标记 Schema 为危险状态。 |
| **5. 架构与模块面** | 基础 | 1. 理清 service boundary 和核心业务模块拓扑。`<br/>`2. 审查包结构和项目子包边界。<br/>3. 识别分层架构（如 Controller-Service-DAO）的严密性。 | `audit-evidence/architecture_modules.txt` | 发现深层浅模块或明显跨层调用越界时，建议触发 `/architecture-audit`。 |

### 第三阶：契约与拓扑 (The Web)

理清模块间的通讯方式、依赖关系，以及项目是如何被运行起来的。

| 面 | 属性 | 核心核验法则 (Verification Checklist) | 预期 Evidence 输出范例 | 深挖与阻断法则 (Drill-down & Block) |
| ---- | ------ | --------------------------------------- | ------------------------ | ------------------------------------- |
| **6. 契约与接口面** | 基础 | 1. 校验 OpenAPI 规范或 RPC schema 契约。`<br/>`2. 审查前后端强类型 (Typescript 等) 的复用与隔离。<br/>3. 确认第三方 API 的消费数据契约。 | `audit-evidence/contracts.txt` | 未明确 Typescript 强类型保护的跨端契约必须列入待补齐的修复清单。 |
| **7. 依赖关系面** | 基础 | 1. 梳理核心调用图和读写依赖路径。`<br/>`2. 追踪上游生产者与下游消费者的拓扑。<br/>3. 确认同步调用与异步队列的明确边界。 | `audit-evidence/dependency_graph.txt` | 必须顺着依赖树跨文件追溯。如果依赖了被标记为弃用的包，标记为技术债。 |
| **8. 运行与部署面** | 基础 | 1. 确认系统启动入口与进程拓扑 (PM2/Docker)。`<br/>`2. 检查环境变量配置 (env/config) 及 Feature flags。<br/>3. 审查 CI/CD Pipeline 与自动化部署入口。 | `audit-evidence/runtime_deploy.txt` | 如果本地缺乏配置无法顺利启动服务，即刻记录阻塞点，禁止凭空臆测运行结果。 |

### 第四阶：边界与验证 (The Interface)

审查直接面向用户或被执行的代码入口，以及其质量保护网（测试）。

| 面 | 属性 | 核心核验法则 (Verification Checklist) | 预期 Evidence 输出范例 | 深挖与阻断法则 (Drill-down & Block) |
| ---- | ------ | --------------------------------------- | ------------------------ | ------------------------------------- |
| **9. 代码入口面** | 基础 | 1. 审计 API router、CLI 命令或 Worker 订阅点。`<br/>`2. 定位对应的 Handler/Service 具体实现入口。<br/>3. 寻找潜在的死代码或孤儿执行点。 | `audit-evidence/code_entrypoints.txt` | 孤儿代码（不在依赖调用网内，也无入口）必须显式标记为无用的死代码。 |
| **10. UI 面** | 基础 | 1. 审计前端页面、核心组件与交互流程。`<br/>`2. 检查用户可见的状态边界（空态/加载态/错误态）。<br/>3. （如为纯后端项目则此面 N/A）。 | `audit-evidence/ui_surfaces.txt` | 必须审查错误状态流的闭环。如果错误只是控制台报错而无 UI 反馈，标记为 UI 缺陷。 |
| **11. 测试面** | 基础 | 1. 验证已有单测 (Unit Tests) 或端到端测试 (e2e)。`<br/>`2. 检查 Snapshot / Golden 文件的存在性。<br/>3. 检查当前是否已有未修复的失败测试。 | `audit-evidence/tests.txt` | 如果代码入口面没有任何对应的测试覆盖，标记为 Audit Debt，强制其在未来的验收 DoD 中补齐。 |

### 第五阶：非功能与生命周期 (NFR & Lifecycle)

【核心升维】决定系统是否具备“生产就绪 (Production-Ready)”与“合法合规”的终极审查。

| 面 | 属性 | 核心核验法则 (Verification Checklist) | 预期 Evidence 输出范例 | 深挖与阻断法则 (Drill-down & Block) |
| ---- | ------ | --------------------------------------- | ------------------------ | ------------------------------------- |
| **12. 安全与隐私面** | 基础 | 1. 核验敏感 API 的 AuthN/AuthZ 鉴权边界。`<br/>`2. 检查 PII (个人隐私数据) 是否存在越权读写或日志泄漏。<br/>3. 审查硬编码密钥 (Secrets) 及供应链漏洞风险。 | `audit-evidence/security_privacy.txt` | 任何涉及绕过鉴权或硬编码密码的行为，一律作为最高级别的阻塞风险进行熔断拦截。 |
| **13. 可观测性面** | 基础 | 1. 检查报错与异常是否接入 Sentry 等捕获平台。`<br/>`2. 确认核心业务流有无恰当的 Log 打印与链路追踪。<br/>3. 核验是否存在暴露给外网的 Healthcheck / Metrics 探针。 | `audit-evidence/observability.txt` | 长链路、高风险的支付/迁移任务若缺乏埋点，必须勒令增加日志规范。 |
| **14. 合规与版权面** | 基础 | 1. 审查核心依赖的开源 License (防范 GPL 传染等)。`<br/>`2. 检查产出代码是否有恰当的归属权或版权申明。<br/>3. 排除代码中遗留的“AI 生成占位符”或伪造的人工痕迹。 | `audit-evidence/compliance.txt` | 发现恶意传染协议或代码归属造假，即刻报警拦截，禁止发版合入。 |

---

## 审计出口门禁 (Audit Depth Gate)

执行 14 面全景审计必须满足以下置信度底线：

1.**强制顺序**：必须遵循 1 -> 5 阶的次序执行，禁止跳阶。若前一阶产生 `BLOCKED` 级异常，立刻停止，不强行查下游。

1. **决策覆盖**：所有启用的面，必须逐一得出 Decision（pass / pass with gap / blocked）。
2. **强证据兜底**：**1. 文档 SSOT 面**与**3. 真实数据库面**在强依赖领域不可 N/A，且两者 Confidence 各需 $\ge 80\%$。

4.**零未知**：未知数 (Unknowns) 必须清零，或明确标注“不影响下一步决策”的具体证据与后续验证点。
