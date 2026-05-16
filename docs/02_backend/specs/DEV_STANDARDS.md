# 开发规范 (Development Standards)

> **doc_type**: DEV_STANDARDS
> **用途**: 定义编码规范、目录结构、命名约定及开发流程

---

## 1. 项目目录结构

```
{project_root}/
├── cmd/                    # 入口文件
├── internal/               # 业务代码（私有）
│   ├── handler/            # HTTP 处理器
│   ├── service/            # 业务逻辑
│   ├── repo/               # 数据访问
│   ├── model/              # 数据模型
│   └── middleware/          # 中间件
├── pkg/                    # 公共库（可导出）
├── configs/                # 配置文件
├── migrations/             # 数据库迁移
├── docs/                   # 文档
└── Makefile
```

## 2. 编码规范

### 2.1 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 包名 | 小写单词 | `user`, `order` |
| 函数名 | CamelCase | `GetUserByID` |
| 常量 | 全大写下划线 | `MAX_RETRY_COUNT` |
| 数据库字段 | snake_case | `created_at` |
| API 路径 | kebab-case | `/api/v1/user-profiles` |

### 2.2 错误处理

- 所有错误必须返回结构化错误码
- 禁止吞掉错误
- 日志必须包含上下文（TraceID）

### 2.3 日志规范

| 级别 | 场景 |
|------|------|
| ERROR | 系统错误、外部依赖失败 |
| WARN | 业务异常、降级处理 |
| INFO | 关键业务节点 |
| DEBUG | 调试信息（生产关闭） |

## 3. 数据库规范

### 3.1 表设计

- 所有表必须包含标准审计字段（id, tenant_id, created_at, updated_at, deleted_at）
- 禁止物理删除，统一使用软删除
- 禁止跨租户查询，所有查询必须携带 tenant_id

### 3.2 迁移规范

- 每次 DDL 变更必须有 UP + DOWN 脚本
- Schema Freeze 后变更走审批流

## 4. API 规范

### 4.1 RESTful 规范

| 操作 | Method | Path | 说明 |
|------|--------|------|------|
| 列表 | GET | `/api/v1/{resource}` | 分页查询 |
| 详情 | GET | `/api/v1/{resource}/:id` | 单条查询 |
| 创建 | POST | `/api/v1/{resource}` | 新建 |
| 更新 | PUT | `/api/v1/{resource}/:id` | 全量更新 |
| 删除 | DELETE | `/api/v1/{resource}/:id` | 软删除 |

### 4.2 响应格式

```json
{
  "code": 0,
  "message": "success",
  "data": {},
  "request_id": "uuid"
}
```
