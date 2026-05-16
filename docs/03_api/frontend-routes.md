# 前端路由表 (Frontend Routes)

> **用途**: 定义系统前端所有页面路由，作为前后端协作的路由参考。
> **维护者**: frontend agent + coordinator

---

## 1. 路由结构

```
/                               → RootLayout（认证后）
├── /login                      → 登录页（未认证）
├── /register                   → 注册页（未认证）
├── /dashboard                  → 首页仪表盘
│
├── /{module-a}                 → 模块 A
│   ├── /{resource}             → 资源列表
│   ├── /{resource}/new         → 新建资源
│   └── /{resource}/:id         → 资源详情
│
├── /{module-b}                 → 模块 B
│   └── ...
│
├── /settings                   → 系统设置
│   ├── /profile                → 个人设置
│   └── /organization           → 组织设置
│
└── /admin                      → 管理后台
    ├── /users                  → 用户管理
    └── /roles                  → 角色管理
```

## 2. 路由表模板

| # | 路由 | 页面 | 权限 | 对应 API |
|---|------|------|------|---------|
| 1 | `/login` | 登录页 | `public` | `POST /auth/login` |
| 2 | `/dashboard` | 首页仪表盘 | `authenticated` | `GET /dashboard/summary` |
| 3 | `/{module}/{resource}` | 资源列表 | `perm:{module}:read` | `GET /api/v1/{resource}` |
| 4 | `/{module}/{resource}/new` | 新建资源 | `perm:{module}:write` | `POST /api/v1/{resource}` |
| 5 | `/{module}/{resource}/:id` | 资源详情 | `perm:{module}:read` | `GET /api/v1/{resource}/:id` |

## 3. 权限标注规则

| 标注 | 说明 |
|------|------|
| `public` | 无需登录即可访问 |
| `authenticated` | 登录后即可访问 |
| `perm:{module}:{action}` | 需要特定权限 |
| `RBAC` | 基于角色的访问控制 |
| `super_admin` | 仅超级管理员 |
