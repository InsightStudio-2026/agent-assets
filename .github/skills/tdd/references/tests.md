# Good and Bad Tests / 好测试与坏测试

## 好测试

**集成风格**：通过真实接口测试，不 mock 内部部件。

```typescript
// 好：测试可观察行为
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

特征：

- **测试用户 / 调用者关心的行为**-**只使用公共 API**-**能穿过内部重构存活**-**描述 WHAT，而不是 HOW**-**每个测试只有一个逻辑断言**## 坏测试**实现细节测试**：与内部结构耦合。

```typescript
// 坏：测试实现细节
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

危险信号：

- **mock 内部协作者**-**测试私有方法**-**断言调用次数 / 调用顺序**-**行为没变但重构后测试失败**-**测试名描述 HOW，而不是 WHAT**-**绕过接口，用外部手段验证**

```typescript
// 坏：绕过接口验证
test("createUser saves to database", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});

// 好：通过接口验证
test("createUser makes user retrievable", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```
