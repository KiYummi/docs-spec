# 幂等性规范 (Idempotency Spec)

> **定位**: 定义所有写操作的幂等策略，作为 API 契约和编码的强制约束。
> **适用范围**: 全模块

---

## 1. 幂等策略矩阵

| 策略缩写 | 全称 | 说明 |
|---------|------|------|
| `NI` | Natural Idempotent | 自然幂等（同参数同结果） |
| `IK` | Idempotency-Key | 请求头携带幂等键 |
| `SM` | State Machine | 状态机守卫（只允许合法转换） |
| `OL` | Optimistic Lock | 乐观锁（version 字段） |
| `FK` | Field Key | 业务字段唯一约束 |
| `TX` | Transaction | 数据库事务保护 |

---

## 2. 模块幂等矩阵模板

| 模块 | 操作 | 策略 | 说明 |
|------|------|------|------|
| `{MODULE_A}` | 创建{资源} | `IK` | Idempotency-Key |
| `{MODULE_A}` | 更新{资源} | `OL` | 乐观锁 |
| `{MODULE_A}` | 删除{资源} | `SM` | 状态机守卫 |
| `{MODULE_B}` | 查询{资源} | `NI` | 自然幂等 |
| `{MODULE_B}` | 提交{操作} | `IK + SM` | 幂等键 + 状态机 |

---

## 3. Idempotency-Key 规范

### 3.1 请求格式

```http
POST /api/v1/{resource}
Idempotency-Key: {uuid-v4}
Content-Type: application/json
```

### 3.2 规则

- Key 格式：UUID v4
- Key 有效期：24 小时
- 同 Key 重复请求：返回首次结果（不重复执行）
- 存储：Redis（TTL 24h）

### 3.3 响应头

```http
HTTP/1.1 201 Created
X-Idempotency-Key: {uuid-v4}
X-Idempotency-Replayed: false  # true 表示返回的是缓存结果
```

---

## 4. 状态机守卫规范

### 4.1 规则

- 只允许合法的状态转换
- 非法转换返回 409 Conflict
- 转换必须记录操作人和时间

### 4.2 示例

```json
{
  "from": "draft",
  "to": "submitted",
  "action": "submit",
  "guard": "所有必填字段已填写",
  "side_effect": "发布 submitted 事件"
}
```

---

## 5. 乐观锁规范

### 5.1 规则

- 请求必须携带 `version` 字段
- 版本不匹配返回 409 Conflict
- 更新成功后 version +1

### 5.2 请求示例

```json
{
  "field_a": "new_value",
  "version": 3
}
```

### 5.3 错误响应

```json
{
  "code": 1005,
  "message": "数据冲突，请刷新后重试",
  "data": {
    "current_version": 5,
    "submitted_version": 3
  }
}
```
