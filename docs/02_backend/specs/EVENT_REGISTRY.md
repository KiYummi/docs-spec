# 事件注册表 (Event Registry)

> **doc_type**: EVENT_REGISTRY
> **module_id**: global_event
> **version**: V 1.0
> **phase**: Phase_3
> **用途**: 全局事件定义与注册

---

## 1. 事件命名规范

```
{domain}.{entity}.{action}
```

示例：`order.created`, `user.updated`, `payment.completed`

## 2. 事件注册表模板

| # | 事件名 | 发布方 | 消费方 | 触发时机 | Payload |
|---|--------|--------|--------|---------|---------|
| 1 | `{domain}.{entity}.{created}` | {模块A} | {模块B} | {触发时机} | {Payload} |
| 2 | `{domain}.{entity}.{updated}` | {模块A} | {模块B} | {触发时机} | {Payload} |

## 3. 事件 Payload 规范

```json
{
  "event_id": "uuid",
  "event_type": "{domain}.{entity}.{action}",
  "tenant_id": "uuid",
  "timestamp": "ISO8601",
  "payload": {
    "entity_id": "uuid",
    "fields": {}
  }
}
```

## 4. 事件消费规范

- 所有消费端必须实现幂等性
- 失败重试：3 次，间隔指数退避
- 死信队列：重试失败后进入死信队列
