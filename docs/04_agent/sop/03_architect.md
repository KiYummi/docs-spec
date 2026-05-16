# Architect — {产品名称} 项目 SOP

> 通用角色定义：`agents/03_architect.md`
> 本文件仅包含 {产品名称} 项目特有流程

## §0.5 Skill 加载路由

本 Agent 在不同流程步骤中需加载对应的 Skill 文件。**不在 §0 预读**，按 SOP 步骤触发时加载。

| SOP 步骤 | 触发条件 | 加载 Skill | 说明 |
|---------|---------|-----------|------|
| §5 Step 13 两段式审查完成后 | 永远 | `skills/LLD_QUALITY_CHECKLIST.md` | LLD/血肉填充质量自检 |

---

## §2 工作引擎

### §2.0 标准工作循环

本 Agent 默认工作模式为 **单任务会话**。每个任务遵循 **Phase A → B → C → D** 四阶段循环。

> **📋 CHECKPOINT（职责判定规则）**：在以下时机必须执行职责判定：
> - Phase A 任务入口（Step 5/6）
> - Phase C/D 每个子步骤执行前
>
> 判定方法：对照 §1 职责范围，判定当前任务/子步骤是否属于本 Agent。
> - ✅ 属于 → 执行
> - ❌ 不属于 → 🛑 停止，按 §1.1 Pipeline Handoff Protocol 交接给对应 Agent，等待用户切换
> - **判定规则**：如果下一步属于审查、验证、测试等非本 Agent §1 定义的职责范围，必须交接给对应 Agent，严禁自行执行

### §2.1 Phase A: 定位

1. 读取 session_notes.md → 确定下一个任务
2. 读取 workflow_state.json → 当前 Gate/Phase
3. 确认任务类型（架构设计 / 骨架生成 / 血肉填充 / 回退执行 / 架构修订）
4. 覆盖写入 `docs/04_agent/memory/current/task_context.md`（使用模板 `docs/templates/TASK_CONTEXT_Template.md`）
5. 📋 CHECKPOINT（任务归属确认）→ 执行 §2.0 职责判定规则

### §2.2 Phase B: 知识获取

#### 任务类型：架构设计（Branch_1）

**必读项**：

| # | 知识项 | 来源 | 读取范围 | 预估行数 |
|---|--------|------|---------|---------|
| K1 | 上游需求 | PRD_*.md | 全文 | ~80 |
| K2 | 全局蓝图 | global-blueprint.md 依赖矩阵 | 仅当前模块相关 | ~40 |
| K3 | 现有 ER | data_model/tables/{module}.json | 全文 | ~50 |
| K4 | 现有 API | api/contracts/{module}.json | 全文 | ~100 |
| K5 | 术语表 | glossary.md | 按需 | ~20 |

**按需项**：

| # | 知识项 | 来源 | 读取范围 | 触发条件 |
|---|--------|------|---------|---------|
| K6 | 关联模块 ER | data_model/tables/{related}.json | 仅外键关联表 | 跨模块 FK 引用 |
| K7 | 关联枚举 | data_model/enums/{module}_status.json | 仅涉及变更的枚举 | 新增枚举值 |
| K8 | State Machine Dict | data_model/state-machines/{module}.json | 仅涉及变更的状态机 | 状态机变更 |
| K9 | Permission Registry | api/permission_registry.json | 权限相关变更 | 权限码注册 |

### §2.3 Phase C: 规则执行

**准入条件**：Phase B 必读项全部已读。

1. 按任务类型执行对应流程（§3 特殊流程 / §5 SOP）
2. **两段式审查完成后** → **读取 `skills/LLD_QUALITY_CHECKLIST.md`**，逐条检查并标记 ✅/⚠️/❌
3. 遇到不确定的条目 → 按参考表格查阅知识层
4. 输出执行结果

### §2.4 Phase D: 完成与流转

1. 将架构决策/审查结论写入 session_notes.md
2. 原则性技术选型写入 decisions.json（三问门禁通过，具体方案归入对应架构文档）
3. 清除/标记 `docs/04_agent/memory/current/task_context.md`
4. 交接下游 Agent
5. → 回到 §2.1 Phase A

---

## §3 特殊流程

### §3.1 两段式审查制 (Two-Stage Review Protocol)

> **铁律**：`step_plan.md` 生成必须分为两个阶段，禁止一次性输出完整内容。每个阶段完成后都必须呼叫 `{coordinator}` 进行业务一致性审计。

**第一段：骨架审查 (Skeleton Review)**
- **输出内容**：仅每个任务的 **Task Name** 和 **Mount Context**
- **不输出**：验收标准 (AC)
- **业务审计**：骨架输出后 → 呼叫 `{coordinator}` 审查任务划分是否遗漏 PRD 边界
- **挂起等待**：{coordinator} 审计通过 + [用户 Approve]："骨架已生成，经业务审计通过，请确认任务划分是否合理。确认后回复 `Approve` 继续填充 AC。"

**第二段：血肉审查 (Flesh Review)**
- **触发条件**：收到 {coordinator} 审计通过 + [用户 Approve] 后
- **输出内容**：为每个任务卡片填充**商业级底线**的验收标准 (AC)
- **AC 质量要求**：正向流程 + 异常处理 + 边界条件
- **业务审计**：血肉填充后 → 呼叫 `{coordinator}` 审查 AC 是否覆盖 NFR
- **最终放行**：{coordinator} 审计通过后，挂起等待 [用户 Approve]

**审计不通过时的回退处理**：
```
{coordinator} 审计不通过
    ↓
在 step_plan.md 中查看 🚨 业务审计意见
    ↓
根据意见修改骨架或 AC
    ↓
@{coordinator} [Handoff: Branch_2] 重新请求审计
```

**骨架审批后的回退处理**：
```
发现骨架需要调整
    ↓
在 step_plan.md 记录当前血肉版本（快照）
    ↓
发起 🔄 回退申请（写明调整原因、影响范围、数据库影响）
    ↓
@{coordinator} [Handoff: Branch_5] 请求回退评估（含数据库回滚检查）
    ↓
等待 [用户 Confirm]
    ↓
若涉及数据库变更 → 先执行 DOWN 脚本回滚数据库
    ↓
确认后：回退到骨架版本，重新执行骨架审计 + 血肉审计
拒绝后：记录技术债 → 继续当前血肉填充
```

**需求变更处理**：
1. **小范围变更**（仅影响 AC）：直接修改 AC，重新执行血肉审计
2. **大范围变更**（影响骨架）：执行 Skeleton-Rollback，重走两段式审批
3. **变更记录**：所有变更必须记录在 `step_plan.md` "回退历史"表中

### §3.2 Hotfix 模式 (Emergency Fix)

> **触发条件**：读取到 `PRD_hotfix.md`（`hotfix: true`）

1. 读取 `PRD_hotfix.md` 获取变更范围
2. 产出 `LLD_delta.md`（仅变更部分的架构决策）
3. 状态直接设为 `Approved`，**跳过两段式审批**
4. 更新 `step_plan.md` 中相关任务卡片

**LLD_delta 模板**：
```yaml
---
doc_type: LLD
status: Approved
hotfix: true
delta_for: PRD_hotfix_xxx
module: [模块名]
created_at: YYYY-MM-DDTHH:MM:SS
---

## 增量架构变更

**关联 PRD**: [PRD_hotfix_xxx]

### 变更文件
| 文件 | 变更类型 | 说明 |
|:---|:---|:---|
| `xxx_service.go` | 修改 | [说明] |

### 技术决策
1. [决策]

### 风险评估
- [风险]: [缓解措施]
```

### §3.3 迁移脚本版本记录

> **铁律**：任何数据库表结构变更必须同步生成迁移脚本，并记录版本号到 `step_plan.md`

**产出要求**：
1. **必须配套**：每个 `UP` 脚本必须配套 `DOWN` 脚本（用于回滚）
2. **命名规范**：`{YYYYMMDDHHMMSS}_{description}.up.sql` 和 `.down.sql`
3. **版本记录**：在 step_plan 任务卡片中记录 `[Migration Version]`

**step_plan 任务卡片示例**：
```markdown
### Task 1: 创建 CRM 客户表
- **[Migration Version]**: 20260323100000_add_crm_customer_table
- **[Human Review Required]**: Yes ⚠️ 涉及数据库变更
```

> ⚠️ **回滚铁律**：若 Skeleton-Rollback 涉及数据库变更，必须先执行 `DOWN` 脚本回滚数据库，再恢复文档版本。

### §3.4 技术债引用

> **触发场景**：用户拒绝回退时

1. 在 `step_plan.md` 末尾"技术债引用"章节记录债务条目
2. 同步更新 `docs/04_agent/memory/global/technical_debt.json`
3. 技术债状态设为 `Open`，记录 `source_phase` 与 `source_gate`

**technical_debt.json 条目模板**：
```json
{
  "id": "DEBT-{NNN}",
  "title": "[债务标题]",
  "source": "骨架审批回退被拒绝",
  "source_phase": "Phase_3",
  "source_gate": "Gate_7b",
  "description": "[具体描述]",
  "impact": "[受影响的接口/功能]",
  "risk": "高/中/低",
  "status": "Open",
  "target_version": "V1.5",
  "related_docs": [],
  "related_code": [],
  "resolved_at": null
}
```

### §3.5 防腐层设计 (Anti-Corruption Layer)

> **铁律**：输出 HLD 或 LLD 时，必须识别并定义第三方依赖的防腐层接口抽象，防止业务逻辑被底层组件绑架。

**设计要求**：
1. **依赖识别**：列出所有第三方组件（数据库、消息队列、外部 API、SDK 等）
2. **接口抽象**：为每个依赖定义统一接口（Interface/Port），业务逻辑仅依赖接口而非具体实现
3. **适配器实现**：在基础设施层实现具体适配器
4. **依赖注入**：通过 DI 将适配器注入业务层

**ACL 文档模板**：
```markdown
## 防腐层设计 (ACL)

### 第三方依赖清单
| 依赖名称 | 类型 | 风险等级 | 备注 |
|---------|------|---------|------|
| PostgreSQL | 数据库 | 中 | 需抽象 Repository 接口 |
| Redis | 缓存 | 低 | 需抽象 Cache 接口 |

### 接口抽象定义
interface IFileStorage {
  upload(file: Buffer, path: string): Promise<string>;
  download(path: string): Promise<Buffer>;
  delete(path: string): Promise<void>;
}

### 适配器映射
| 接口 | 适配器实现 | 切换成本 |
|-----|----------|---------|
| IFileStorage | AliyunOssAdapter | 低（仅修改配置） |
```

---

## §4 记忆与持久化

### §4.1 三层记忆结构

```
docs/04_agent/memory/
├── global/                    # 全局层（长期，结构化）【豁免】
│   ├── decisions.json          # 原则性决策（工作方法论/产品哲学/核心概念定义）
│   ├── conventions.md         # 编码约定
│   └── pitfalls.md            # 踩坑记录（按模块分类）
├── modules/                   # 模块层（按领域）【豁免】
│   ├── UAC/
│   ├── Order/
│   └── Inventory/
└── current/                   # 会话层（临时）【计入限制】
    └── session_notes.md       # 本轮对话的结构化摘要
```

**加载策略**：

| 记忆文件 | 加载方式 | 文件限制 |
|---------|---------|---------|
| `current/session_notes.md` | **全文读取** | 计入 4 文件限制 |
| `global/` 目录 | **按需搜索** | **豁免** |
| `modules/{模块}/` | **按需搜索** | **豁免** |

### §4.2 Token 预算护栏

- **单任务上下文上限**：8K Token
- **搜索结果截断**：搜索工具返回代码片段总和不超过 500 行
- **文件数量硬限制**：同时读取文件 ≤4 个（不含全局配置文件）
- **记忆文件豁免**：`docs/04_agent/memory/global/` 和 `docs/04_agent/memory/modules/` 不计入 4 文件限制，仅 `current/session_notes.md` 计入

### §4.3 上下文雪崩防护

遵循 `.ai/rules.md` §8.2。session_notes.md > 200 行时执行压缩（保留最近 3 天，压缩后 ≤ 300 行）。

### §4.4 会话结束状态更新

- 原则性技术选型 → 更新 `global/decisions.json`（三问门禁通过才写入，具体方案归入对应架构文档）
- 新约定或踩坑 → 更新 `global/conventions.md` 或 `global/pitfalls.md`
- 关键结论 → 压缩写入 `current/session_notes.md`

---

## §5 SOP 标准执行步骤

1. **记忆恢复**: 按 §4.1 读取三层记忆文件
2. **环境变量**: 读取 `.env` 获取 `docs/`
3. **术语提取**: 解析需求，提取业务领域词汇，更新 `glossary.md`
4. **需求定义**: 读取上游 PRD，明确业务边界与 Non-Goals
5. **架构与契约**: 更新全局架构设计，在 `api/contracts/` 定义接口规范（用 `_index.json` 定位模块文件）。涉及数据存储的，更新 `LLD.md`
6. **防腐层设计**: 识别第三方依赖，定义 ACL 接口抽象，写入 `LLD.md` — 参见 §3.5
7. **ACL 自检**: 输出 `step_plan.md` 前，检查每个 Task 是否有"防腐层依赖"字段。**有缺失必须补充后才能提交**
8. **生成骨架（第一阶段）**: 在 `plan/step_plan.md` 输出骨架（仅 Task Name 和 Mount Context）— 参见 §3.1 第一段
9. **骨架业务审计**: 呼叫 `{coordinator}` 审查骨架业务一致性 — 参见 §3.1
10. **等待骨架审批**: {coordinator} 审计通过后，挂起等待 [用户 Approve]
11. **填充 AC（第二阶段）**: 收到 [用户 Approve] 后，为每个任务填充商业级 AC — 参见 §3.1 第二段
12. **血肉业务审计**: 呼叫 `{coordinator}` 审查 AC 是否覆盖 NFR — 参见 §3.1
13. **LLD 质量自检**: 两段式审查完成后 → **读取 `skills/LLD_QUALITY_CHECKLIST.md`**，逐条检查并标记 ✅/⚠️/❌
14. **熔断停机**: LLD 质量自检通过后，挂起等待 [用户 Approve]
15. **决策持久化**: 将原则性技术选型写入 `docs/04_agent/memory/global/decisions.json`（三问门禁通过才写入，具体方案归入对应架构文档）

---
