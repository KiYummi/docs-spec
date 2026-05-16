# API 契约骨架

> **模板来源**: `docs/08_templates/API_CONTRACT_Template.md`
> **用途**: 快速创建 API 契约文档

---

# {模块名称} API 契约

## 1. 通用约定

### 1.1 请求规范

| 项目 | 规范 |
|------|------|
| 协议 | HTTPS |
| 数据格式 | JSON |
| 字符编码 | UTF-8 |

### 1.2 响应格式

```json
{
  "code": 0,
  "message": "success",
  "data": {},
  "request_id": "uuid"
}
```

## 2. 接口清单

### 2.1 {资源} 模块

#### GET /api/v1/{resource}

**描述**: 查询{资源}列表

**查询参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | integer | 否 | 页码，默认 1 |
| page_size | integer | 否 | 每页数量，默认 20 |

**响应体**:
```json
{
  "code": 0,
  "data": {
    "items": [],
    "total": 0
  }
}
```

**x-req-ids**: `["@req-id: R001"]`

#### POST /api/v1/{resource}

**描述**: 创建{资源}

**请求体**:
```json
{
  "field_a": "string"
}
```

**响应体**:
```json
{
  "code": 0,
  "data": {
    "id": "uuid"
  }
}
```

**x-req-ids**: `["@req-id: R002"]`
