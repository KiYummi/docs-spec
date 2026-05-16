# 命名规范 (Naming Conventions)

> **版本**: v1.0
> **用途**: 定义项目中所有命名的统一规范

---

## 1. 数据库命名

| 类型 | 规范 | 示例 |
|------|------|------|
| 表名 | snake_case, 复数 | `users`, `orders` |
| 字段名 | snake_case | `created_at`, `user_id` |
| 索引 | `idx_{table}_{field}` | `idx_users_email` |
| 外键 | `fk_{table}_{ref}` | `fk_orders_users` |

## 2. API 命名

| 类型 | 规范 | 示例 |
|------|------|------|
| 路径 | kebab-case, 复数 | `/api/v1/user-profiles` |
| 参数 | snake_case | `page_size`, `sort_by` |
| 响应字段 | snake_case | `created_at`, `user_id` |

## 3. 代码命名

| 类型 | 规范 | 示例 |
|------|------|------|
| 包名 | 小写单词 | `user`, `order` |
| 结构体 | CamelCase | `UserService` |
| 函数 | CamelCase | `GetUserByID` |
| 常量 | 全大写下划线 | `MAX_RETRY_COUNT` |
| 变量 | camelCase | `userID`, `orderList` |

## 4. 缩写表

| 缩写 | 全称 | 说明 |
|------|------|------|
| `{缩写1}` | `{全称1}` | {说明} |
| `{缩写2}` | `{全称2}` | {说明} |
