# Interface Design for Testability / 可测试接口设计

好接口会让测试自然发生：

1. **接收依赖，不要内部创建依赖**```typescript
   // 易测试
   function processOrder(order, paymentGateway) {}

   // 难测试
   function processOrder(order) {
     const gateway = new StripeGateway();
   }

```text

2.**返回结果，不要制造隐式副作用**```typescript
   // 易测试
   function calculateDiscount(cart): Discount {}

   // 难测试
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
```

1.**接口面积小**

- 方法更少 = 需要测试的入口更少
- 参数更少 = 测试准备更简单
