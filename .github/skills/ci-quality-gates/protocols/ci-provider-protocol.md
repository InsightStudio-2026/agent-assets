# CI 服务商协议 (CI Provider Protocol)

## 1. 服务商探测 (Provider Detection)

| 规则 ID (Rule ID) | 服务商 (Provider) | 探测路径 (Detection Path) | 必需证据 (Required Evidence) |
| --------- | ---------- | ---------------- | ------------------- |
| CIP-R1 | GitHub Actions | `.github/workflows/*.yml` / `.yaml` | workflow list + job names |
| CIP-R2 | GitLab CI | `.gitlab-ci.yml` | stages + jobs |
| CIP-R3 | CircleCI | `.circleci/config.yml` | workflows + jobs |
| CIP-R4 | Azure Pipelines | `azure-pipelines.yml` | stages + checks |
| CIP-R5 | Custom / Make | scripts / docs / provider config | command list + owner |
| CIP-R6 | None | no CI config found | route `/repo-safety-setup` or draft CI plan |

## 2. 必需检查映射 (Required Check Mapping)

| 规则 ID (Rule ID) | 检查类型 (Check) | 来源 (Source) | 默认是否必需 (Required By Default) |
| --------- | ------- | -------- | --------------------- |
| CIP-C1 | lint | package script / Make target / CI job | Yes if project has linter |
| CIP-C2 | typecheck | package script / CI job | Yes if typed language |
| CIP-C3 | unit test | package script / CI job | Yes |
| CIP-C4 | integration / e2e | spec / release critical path | Conditional |
| CIP-C5 | build | package script / CI job | Yes for deployable artifacts |
| CIP-C6 | security / dependency | audit job / security workflow | Conditional high-risk |
| CIP-C7 | coverage | coverage job / threshold | Project-defined |
| CIP-C8 | migration check | migration scripts / DB drift | Conditional schema changes |

## 3. 分支保护边界 (Branch Protection Boundary)

| 规则 ID (Rule ID) | 动作 (Action) | 是否需要审批 (Approval Required) | 原因 (Reason) |
| --------- | -------- | ------------------- | -------- |
| CIP-BP1 | 添加 / 移除必需检查 (Add / remove required check) | 是 (Yes) | 远端仓库策略变更 (Remote repository policy change) |
| CIP-BP2 | 变更目标分支保护 (Change target branch protection) | 是 (Yes) | 团队工作流副作用 (Team workflow side effect) |
| CIP-BP3 | 启用自动合并 / 必需评审 (Enable auto-merge / required review) | 是 (Yes) | 协作策略变更 (Collaboration policy change) |
| CIP-BP4 | 读取本地 CI 配置 (Read local CI config) | 否 (No) | 只读 (Read-only) |
| CIP-BP5 | 仅起草建议 (Draft recommendation only) | 否 (No) | 无副作用 (No side effect) |

## 4. 判定

| 条件 | 状态 (State) |
| ------ | ------- |
| provider + jobs + target branches identified | `/ci-quality-gates:CI_SCOPE_DEFINED` |
| no provider | `/ci-quality-gates:CI_PROVIDER_MISSING` |
| branch protection change needed | `/ci-quality-gates:WAITING_CI_CHANGE_APPROVAL` |
