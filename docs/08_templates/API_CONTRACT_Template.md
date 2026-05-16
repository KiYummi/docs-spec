---
# ==========================================
# 📄 Document Metadata (由 Agent 自动维护)
# ==========================================
doc_type: "API_CONTRACT"
module_id: "api_contract"
version: "V 1.0"
phase: "Phase_3_Architecture"
status: "Draft"
complexity: "L2"

# ==========================================
# 🤖 Agentic Workflow & Audit
# ==========================================
author_agent: "{architect}"
reviewer_agent: "{coordinator_agent}"
last_updated: "YYYY-MM-DDTHH:mm:ssZ"
approved_by: ""

# ==========================================
# 🔗 Dependency & Isolation
# ==========================================
depends_on:
  - "GLOBAL_HLD"
  - "PRD_*"
acl_dependencies: []

# ==========================================
# 📡 API Versioning
# ==========================================
last_sync_version: ""  # 由 {devops} 发版时从 CHANGELOG 同步
base_url: "/api/v1"
---

# API 契约 (API Contract)

> **用途**: 定义系统对外暴露的所有 RESTful API 接口规范，作为前后端协作的唯一契约。

## 1. 通用约定

### 1.1 请求规范

| 项目 | 规范 |
|------|------|
| 协议 | HTTPS |
| 数据格式 | JSON |
| 字符编码 | UTF-8 |
| 时间格式 | ISO 8601 (`YYYY-MM-DDTHH:mm:ssZ`) |
| 分页参数 | `page` (页码), `page_size` (每页数量) |

### 1.2 响应格式

```json
{
  "code": 0,
  "message": "success",
  "data": {},
  "request_id": "uuid-v4"
}
```

### 1.3 错误码定义

| 错误码 | HTTP Status | 说明 |
|--------|-------------|------|
| 0 | 200 | 成功 |
| 1001 | 400 | 参数错误 |
| 1002 | 401 | 未授权 |
| 1003 | 403 | 禁止访问 |
| 1004 | 404 | 资源不存在 |
| 2001 | 500 | 服务器内部错误 |

### 1.4 需求溯源扩展字段 [强制]

> **说明**：每个 API 端点必须包含 `x-req-ids` 扩展字段，标注该端点承接的需求 ID。
> 这是全链路索引的核心机制，确保 API 设计可追溯到原始需求。

**扩展字段格式**：

```yaml
paths:
  /api/v1/{resource}:
    post:
      summary: {操作描述}
      x-req-ids:
        - "@req-id: R001"
        - "@req-id: R002"
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/{SchemaName}'
      responses:
        '201':
          description: {响应描述}
```

**标注规则**：
- 每个端点必须标注 `x-req-ids`
- `x-req-ids` 必须是数组格式
- 每个需求 ID 必须符合 `@req-id: R{序号}` 格式
- 一个端点可以承接多个需求

---

## 2. 接口清单

### 2.1 用户认证模块

#### POST /auth/login

**描述**: 用户登录

**请求体**:
```json
{
  "username": "string",
  "password": "string"
}
```

**响应体**:
```json
{
  "code": 0,
  "data": {
    "token": "jwt_token_string",
    "expires_in": 3600,
    "user": {
      "id": "uuid",
      "username": "string",
      "tenant_id": "uuid"
    }
  }
}
```

---

### 2.2 [模块名] 模块

> TODO: 按模块添加接口定义

---

## 3. 变更日志

| 版本 | 日期 | 变更内容 | 作者 |
|------|------|----------|------|
| v1.0.0 | YYYY-MM-DD | 初始版本 | {architect} |
