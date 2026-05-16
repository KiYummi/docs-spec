# 核心业务对象与状态机元数据字典 (Metadata Dictionary)

**Version:** V 1.0
**状态:** 发布

本字典为整个多智能体研发流水线（Agentic Workflows）及各文档模块（PRD / LLD / API / 代码）的基础定义词汇与核心参数。在 AI 编写文档、架构设计与编写代码时，所有的枚举值和核心业务字段**必须**从本字典中选用，严禁各 Agent 凭空创造、篡改字段名与枚举值。

> **注意**：本文档仅定义**文档流转状态机**（§1.3 `status`）。业务实体的状态机定义（如{业务实体1}状态、{业务实体2}状态、{业务实体3}状态）已迁移至独立制品 `backend/data-model/state-machines/`，按 `_schemas/state_machine_schema.json` 格式存储，为业务状态机 SSOT。

## 1. 🤖 核心元数据 (YAML Frontmatter / Document Metadata)

所有核心研发流转文档（如 `global-blueprint.md`, `PRD_*.md`, `LLD_*.md` 等），其顶部的 YAML Frontmatter 中的键值及 Enum（枚举值）必须严格遵循以下定义：

### 1.1 `doc_type` (文档类型)

| 枚举值 | 含义说明 | 所属 Phase |
| :--- | :--- | :--- |
| `MASTER_PRD` | 核心产品白皮书（MVP 边界、全局架构设计依据） | Phase 1 |
| `GLOBAL_BLUEPRINT` | 全局架构蓝图（L1-L4 分级、依赖关系定义、执行规划） | Phase 1 |
| `REASONING_TRACE` | Agent 推理决策记录（归档冻结，用于上下文传递） | Phase 2-3 |
| `PRD` | 业务模块需求说明书（含用例、业务流转） | Phase 2 |
| `GLOBAL_HLD` | 全局高阶设计文档 | Phase 3 |
| `LLD` | 局部模块详细设计文档（含数据表定义） | Phase 3 |
| `API_CONTRACT` | API 接口契约说明书 | Phase 3 |
| `STEP_PLAN` | 细粒度任务执行计划表 (WIP=1 的任务拆解) | Phase 3 |
| `TECHNICAL_DEBT` | 技术债记录文档（跟踪延期实现的功能） | Phase 1-6 |
| `RELEASE_NOTES` | 发布说明文档（含 hotfix 简版） | Phase 6 |
| `LIVING_DOC` | 面向交付/回溯的活文档 | Phase 6 |
| `ADR` | 架构决策记录（Architecture Decision Record） | 贯穿全生命周期 |

### 1.2 `phase` (生命周期与流水线阶段)

| 枚举值 | 含义说明 | 负责人 (Agent) |
| :--- | :--- | :--- |
| `Phase_1_Strategic` | 战略级愿景定义、宏观蓝图规划 (含 Blueprint) | `{pm_agent}` |
| `Phase_2_Requirement` | 具体模块的需求澄清、拆解及红蓝对抗攻击 | `{pm_agent}`, `{qa_agent}` |
| `Phase_3_Architecture` | 技术选型、DB 设计、防腐层与任务详细计划 (Step_Plan) | `{architect}` |
| `Phase_4_Development` | 编码、单测、WIP=1 的沙盒验证 | `{backend}`, `{frontend}` |
| `Phase_5_Testing` | 静态检查、自动化/手工集成验收 | `{reviewer}`, `{qa_agent}` |
| `Phase_6_Release` | 打标、合入主干与交付活文档生成 | `{devops_agent}` |

### 1.3 `status` (流转状态机)

文档在各阶段的审批与挂起状态：

| 枚举值 | 含义说明 | 业务拦截方 |
| :--- | :--- | :--- |
| `Draft` | Agent 正在撰写初稿，禁止下游介入 | - |
| `Reviewing` | 初稿完成，正进行红蓝对抗、业务审计或等待人类 Approve | `{coordinator}`, `Human` |
| `Approved` | **已通过所有门禁审查及人工签名**，允许流转至下一 Phase | `{coordinator}` |

---

## 2. 📊 核心业务字段

### 2.1 通用审计字段

所有数据库表**必须**包含以下标准审计字段：

| 字段名 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `id` | BIGINT | 主键，自增 | - |
| `tenant_id` | BIGINT | 租户 ID，多租户隔离 | - |
| `is_deleted` | BOOLEAN | 软删除标记 | FALSE |
| `created_by` | BIGINT | 创建人 ID | - |
| `created_at` | TIMESTAMP | 创建时间 | CURRENT_TIMESTAMP |
| `updated_by` | BIGINT | 最后更新人 ID | - |
| `updated_at` | TIMESTAMP | 最后更新时间 | CURRENT_TIMESTAMP |

### 2.2 业务字段命名规范

| 规则 | 示例 | 说明 |
|------|------|------|
| 使用 snake_case | `order_number` | 禁止 camelCase |
| 禁止缩写 | `quantity` | 禁止 `qty` |
| 禁止拼音 | `status` | 禁止 `zhuangtai` |
| 外键命名 | `{表名}_id` | 如 `user_id`, `order_id` |

---

## 3. 🔄 状态机定义

### 3.1 状态机格式

所有业务实体的状态机**必须**按以下格式定义：

```json
{
  "entity": "{实体名称}",
  "states": ["{状态1}", "{状态2}", "{状态3}"],
  "transitions": [
    {
      "from": "{起始状态}",
      "to": "{目标状态}",
      "trigger": "{触发条件}",
      "guard": "{守卫条件}",
      "action": "{执行动作}"
    }
  ],
  "side_effects": [
    {
      "state": "{状态}",
      "effect": "{副作用}"
    }
  ],
  "inverse_path": [
    {
      "from": "{当前状态}",
      "to": "{回退状态}",
      "condition": "{回退条件}"
    }
  ]
}
```

### 3.2 状态机注册

所有状态机**必须**注册到 `backend/data-model/state-machines/` 目录，文件名格式：`{实体名}_state_machine.json`

---

## 4. 📋 枚举定义

### 4.1 枚举格式

所有枚举**必须**按以下格式定义：

```json
{
  "name": "{枚举名称}",
  "description": "{枚举说明}",
  "values": [
    {
      "code": "{枚举值}",
      "name": "{显示名称}",
      "description": "{说明}"
    }
  ]
}
```

### 4.2 枚举注册

所有枚举**必须**注册到 `docs/02_backend/data-model/enums/` 目录，文件名格式：`{枚举名}_enum.json`

---

## 5. 🔐 权限定义

### 5.1 权限码格式

所有权限码**必须**按以下格式定义：

```json
{
  "code": "{权限码}",
  "name": "{权限名称}",
  "description": "{权限说明}",
  "module": "{所属模块}",
  "risk_level": "{风险等级}",
  "rate_limit_level": "{限流等级}"
}
```

### 5.2 权限注册

所有权限码**必须**注册到 `docs/03_api/permission-registry.json`，为权限码 SSOT。

---

## 6. 📝 使用规则

### 6.1 强制遵循

- 所有 Agent **必须**从本字典中选用枚举值和核心业务字段
- 禁止凭空创造、篡改字段名与枚举值
- 发现新字段/枚举必须先注册到本字典，再使用

### 6.2 更新流程

1. 发现新字段/枚举
2. 提交到字典审核
3. 审核通过后注册到字典
4. 通知所有 Agent

### 6.3 冲突处理

- 同一概念使用相同字段名/枚举值
- 发现冲突以本字典为准
- 冲突由 Coordinator 决策
