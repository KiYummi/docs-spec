# 设计系统 (Design System)

> **doc_type**: DESIGN_SYSTEM
> **phase**: Phase_3
> **用途**: 后端设计系统规范（与前端设计体系 docs/01_frontend/ 对应）

---

## 1. API 设计风格

| 维度 | 规范 | 说明 |
|------|------|------|
| 风格 | RESTful | {说明} |
| 版本 | URL 路径 | `/api/v1/` |
| 认证 | Bearer Token | {说明} |
| 分页 | page + page_size | {说明} |
| 排序 | sort_by + sort_order | {说明} |

## 2. 响应格式规范

```json
{
  "code": 0,
  "message": "success",
  "data": {},
  "request_id": "uuid"
}
```

## 3. 错误响应规范

```json
{
  "code": 1001,
  "message": "参数校验失败",
  "details": [
    {
      "field": "email",
      "message": "邮箱格式不正确"
    }
  ]
}
```
