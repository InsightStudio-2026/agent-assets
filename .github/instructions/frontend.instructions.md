---
name: 前端代码规范
description: TypeScript/React 前端代码风格与架构约束。编辑 .tsx/.ts/.jsx/.js 文件时自动加载。
applyTo: '**/*.{tsx,ts,jsx,js}'
---

# 前端开发规范

> 编辑 TypeScript / React 代码时自动生效。本文档是前端代码风格的权威 SSOT。

## 1. 尾随逗号规则

- ✅ **多参数 / 多元素时必须加尾随逗号**- ❌**单参数 / 单元素时禁止尾随逗号**

## 2. React Native 样式规范

-**静态样式**→ Tailwind classes
-**动态样式**→ inline styles 或 StyleSheet
-**复杂样式**→ `StyleSheet.create()`

## 3. TypeScript 类型定义规范

-**定时器类型**：React Native 环境用 `ReturnType<typeof setInterval>` 而非 `NodeJS.Timeout`

- **any 类型抑制**：必要时用 `eslint-disable-next-line @typescript-eslint/no-explicit-any` + 原因注释
- **未使用的变量 / 导入**：及时删除；未使用参数用 `_` 前缀
- **Promise 类型**：用 `Promise<T>` 而非 `PromiseLike<T>`

## 4. 配置文件的 require()

每个 `require()` 前加 `// eslint-disable-next-line @typescript-eslint/no-require-imports`

## 5. 通用前端开发纪律

### 5.1 中文化与命名

- **源码注释**：`src/` 目录内所有注释和 JSDoc 必须使用中文。
- **变量命名**：业务相关变量优先使用拼音或中文，良好的命名应能自解释。

### 5.2 代码设计原则

- **单一职责**：每个组件 / Hook 只做一件事。
- **早返回**：优先处理异常与边界情况，减少嵌套。
- **显式优于隐式**：不依赖隐式类型转换。
- **DRY 原则**：重复逻辑超 3 次必须抽取公共方法/自定义 Hook。
- **边界思维**：始终处理空值、undefined、空数组、加载失败等状态。
- **先理解后动手**：修改前先读懂现有组件逻辑。
- **及时清理**：删除无用代码、未使用的 imports、注释掉的代码、临时 console.log。
- **根因修复**：bug 修复必须解释根因、覆盖复现路径和回归测试。
- **兼容与清理**：兼容层/fallback 只能服务明确的迁移窗口。
- **代码文件头**：覆写文件头而非追加，避免头信息堆积。

### 5.3 错误与日志处理

- **捕获具体异常**：避免静默吞错；必要时 fallback UI 或 toast。
- **携带上下文**：错误信息包含操作描述、数据、失败原因。
- **关键操作日志**：支付、核心提交、网络状态变更必须有日志。

## 6. DoD 自动化检查与修复

**验证检查**：

```powershell
npx eslint . --max-warnings 0
npx prettier --check .
npx tsc --noEmit
npx jest --no-coverage --verbose
```

**自动修复**：

```powershell
npx prettier --write .
npx eslint . --fix
```
