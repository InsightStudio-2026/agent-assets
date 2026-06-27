# When to Mock / 何时 Mock

只在**系统边界**mock：

-**外部 API**：支付、邮件等。

- **数据库**：有时可以，但优先测试数据库。
- **时间 / 随机性**-**文件系统**：有时可以。

不要 mock：

- **自己的类 / 模块**-**内部协作者**-**任何你控制的东西**## 为可 Mock 性设计

在系统边界，设计容易 mock 的接口：

## 1. 使用依赖注入

传入外部依赖，而不是在内部创建：

```typescript
// 易 mock
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// 难 mock
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

### 2. 优先 SDK 风格接口，而不是通用 fetcher

为每个外部操作创建具体函数，不要用一个内部带条件逻辑的通用函数：

```typescript
// 好：每个函数都能独立 mock
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch('/orders', { method: 'POST', body: data }),
};

// 坏：mock 内部必须写条件逻辑
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

SDK 风格意味着：

-**每个 mock 返回一种具体形状**-**测试准备里没有条件逻辑**-**更容易看出测试触达了哪些 endpoint**-**每个 endpoint 都有类型安全**
