---
name: migrate-to-shoehorn
description: >
  将测试文件中的 `as` 类型断言迁移到 `@total-typescript/shoehorn`。
  Use when user mentions shoehorn, wants to replace `as` in tests, needs partial test data,
  or asks 迁移测试断言/替换 as/测试数据补全。
user-invocable: false
---

# 迁移 Shoehorn（migrate-to-shoehorn）

## 为什么使用 shoehorn？

`shoehorn` 允许你在测试中传入部分数据，同时保持 TypeScript 满意。它用类型更安全的替代方案取代 `as` 断言。

**只用于测试代码。**永远不要在生产代码中使用 shoehorn。

测试中 `as` 的问题：

-**会训练出坏习惯**：让代码习惯绕过类型系统。

- **必须手动指定目标类型**。
- **故意传错数据时常出现 double-as**：`as unknown as Type`。

## 安装

如果项目尚未安装 `@total-typescript/shoehorn`，先确认包管理器与依赖策略。安装依赖属于会修改项目状态的操作，需要用户许可或明确任务要求。

常见命令示例：`npm i @total-typescript/shoehorn`。

## 迁移模式

### 大对象但只需要少数字段

Before:

```ts
type Request = {
  body: { id: string };
  headers: Record<string, string>;
  cookies: Record<string, string>;
  // ...20 more properties
};

it("gets user by id", () => {
  // Only care about body.id but must fake entire Request
  getUser({
    body: { id: "123" },
    headers: {},
    cookies: {},
    // ...fake all 20 properties
  });
});
```

After:

```ts
import { fromPartial } from "@total-typescript/shoehorn";

it("gets user by id", () => {
  getUser(
    fromPartial({
      body: { id: "123" },
    }),
  );
});
```

### `as Type` → `fromPartial()`

Before:

```ts
getUser({ body: { id: "123" } } as Request);
```

After:

```ts
import { fromPartial } from "@total-typescript/shoehorn";

getUser(fromPartial({ body: { id: "123" } }));
```

### `as unknown as Type` → `fromAny()`

Before:

```ts
getUser({ body: { id: 123 } } as unknown as Request); // wrong type on purpose
```

After:

```ts
import { fromAny } from "@total-typescript/shoehorn";

getUser(fromAny({ body: { id: 123 } }));
```

## 何时使用哪个函数

| 函数 (Function) | 适用场景 (Use Case) |
| --------------- | -------------------------------------------------- |
| `fromPartial()` | 传入仍能通过类型检查的部分数据 |
| `fromAny()` | 传入故意错误的数据，同时保留 autocomplete |
| `fromExact()` | 强制完整对象，之后可替换为 `fromPartial()` |

## 工作流

1. **收集需求**：询问或从任务中推断：
   - 哪些测试文件中的 `as` 断言正在制造问题？
   - 是否是在处理大对象，但测试只关心少数字段？
   - 是否需要为错误路径测试传入故意错误的数据？

2. **安装与迁移**：
   - [ ] 若依赖缺失，按项目包管理器安装，并确保该操作被允许。
   - [ ] 使用项目搜索工具查找测试文件中的 `as` 断言，优先限定 `*.test.ts` 与 `*.spec.ts`。
   - [ ] 将 `as Type` 替换为 `fromPartial()`。
   - [ ] 将 `as unknown as Type` 替换为 `fromAny()`。
   - [ ] 从 `@total-typescript/shoehorn` 添加 imports。
   - [ ] 运行 type check 验证。
