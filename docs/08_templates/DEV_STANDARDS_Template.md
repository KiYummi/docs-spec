---
# ==========================================
# 📄 Document Metadata (由 Agent 自动维护)
# ==========================================
doc_type: "DEV_STANDARDS"
module_id: "dev_standards"
version: "V 2.0"
phase: "Phase_7_Implementation"
status: "Draft"
complexity: "L2"

# ==========================================
# 🤖 Agentic Workflow & Audit
# ==========================================
author_agent: "{backend}_backend"
reviewer_agent: "{coordinator_agent}"
last_updated: "YYYY-MM-DDTHH:mm:ssZ"
approved_by: ""

# ==========================================
# 🔗 Dependency & Isolation
# ==========================================
depends_on:
  - "NAMING_CONVENTIONS"
  - "SECURITY_BASELINE"
  - "AOP_DESIGN"
acl_dependencies: []
---

# 开发规范 (Development Standards)

> **用途**: 定义 {产品名称} 项目（{语言} + {框架} / {ORM} / {数据库}）的编码规范、目录结构、命名约定及开发流程，确保团队协作一致性。

## §1 项目结构

> 定义 Go 项目的目录组织方式。列出顶层目录、各包的职责与边界。
> SSOT: `docs/02_backend/architecture/codebase-architecture.md` B1~B2

### 1.1 顶层目录
<!-- 填写顶层目录结构与职责说明 -->

### 1.2 模块内部 8 文件骨架
<!-- 填写 handler / service / repo / model / dto / router / test / doc 骨架 -->

---

## §2 命名规范

> 定义文件、变量、函数、数据库对象的命名约定。
> SSOT: `docs/02_backend/specs/NAMING_CONVENTIONS.md`

### 2.1 文件命名
<!-- Go 文件命名规范 -->

### 2.2 变量与函数命名
<!-- Go 变量、函数、常量、接口命名规范 -->

### 2.3 数据库命名
<!-- 表名、字段名、索引命名规范 -->

### 2.4 包命名
<!-- Go package 命名规范 -->

---

## §3 Git 提交规范

> 定义 Commit Message 格式、分支命名、PR 流程。

### 3.1 Commit Message 格式
<!-- type(scope): subject 格式说明 -->

### 3.2 分支命名
<!-- feature/ bugfix/ hotfix/ 规范 -->

### 3.3 PR 流程
<!-- PR 模板、审查要求 -->

---

## §4 错误处理规范

> 定义 Go error wrapping 策略、业务错误码体系、HTTP 状态码映射规则。
> SSOT: `docs/03_api/error-codes.json`

### 4.1 Go Error Wrapping
<!-- fmt.Errorf("...: %w", err) / errors.Is / errors.As 使用规范 -->

### 4.2 业务错误码
<!-- 错误码结构定义、与 error-codes.json 的对应 -->

### 4.3 HTTP 状态码映射
<!-- 业务错误码 → HTTP status 的映射规则 -->

### 4.4 错误传播边界
<!-- 哪些层返回原始错误、哪些层包装、哪些层吞掉 -->

---

## §5 日志规范

> 定义结构化日志、TraceID 传播、日志级别使用、必打字段。
> SSOT: `docs/02_backend/specs/AOP_DESIGN.md`, `docs/02_backend/specs/MONITORING_DASHBOARD.md`

### 5.1 结构化日志
<!-- zap/slog 字段约定、JSON 格式 -->

### 5.2 TraceID 传播
<!-- Context 中传递 TraceID、跨服务透传 -->

### 5.3 日志级别
<!-- Debug / Info / Warn / Error / Fatal 各级别使用场景 -->

### 5.4 必打字段
<!-- 每条日志必须包含的字段（trace_id, tenant_id, user_id 等） -->

---

## §6 代码审查清单

> PR 审查时的检查项。
> SSOT: `docs/04_agent/skills/LLD_QUALITY_CHECKLIST.md`

### 6.1 通用检查
<!-- 通用代码质量检查项 -->

### 6.2 后端检查
<!-- SQL 参数化、权限校验、事务处理、错误处理 -->

### 6.3 安全检查
<!-- 参考 SECURITY_BASELINE.md -->

---

## §7 API 开发约定

> 定义 RESTful 模式、分页、幂等性、事务边界。
> SSOT: `docs/03_api/idempotency-spec.md`, `docs/02_backend/architecture/overview.md`

### 7.1 RESTful 模式
<!-- URL 设计、HTTP 方法使用、资源命名 -->

### 7.2 分页规范
<!-- 统一分页参数、响应格式 -->

### 7.3 幂等性
<!-- 幂等键设计、重试安全 -->

### 7.4 事务边界
<!-- 事务在 service 层管理、避免长事务 -->

---

## §8 测试规范

> 定义测试覆盖率、命名、分层策略。
> SSOT: `docs/00_meta/master-prd.md` §5, `docs/02_backend/architecture/overview.md`

### 8.1 测试分层
<!-- 单元测试 / 集成测试 / E2E 测试 -->

### 8.2 覆盖率要求
<!-- 各层级最低覆盖率 -->

### 8.3 测试命名
<!-- Go test 函数命名规范 -->

---

## §9 变更日志

| 版本 | 日期 | 变更内容 | 作者 |
|------|------|----------|------|
| v2.0.0 | YYYY-MM-DD | 新增 §4 错误处理、§5 日志、§7 API 约定 | {backend} |
| v1.0.0 | YYYY-MM-DD | 初始版本 | {architect} |
