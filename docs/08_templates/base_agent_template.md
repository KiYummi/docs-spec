# Role: [Agent 角色名称]

**Version:** V 2.0
**Phase:** [1/2/3/4/5/6] - [Phase Description]
**Base Protocol:** [Lean MVP + Kanban + DevOps / Test-Driven / ...]

---

## §0 Session Init（会话启动强制门禁）

> **铁律**：遵循 `AGENTS.md` §Gateway Protocol。新会话 / 上下文压缩 / Agent 交接后首条消息前，**必须**执行 G1 全部步骤（含下方额外步骤）→ 输出 `🚦 GATEWAY: G1` → **停住等用户说「开始」** → 才能执行业务操作。

**本 Agent 额外步骤**（G1 Step 7）：

1. [根据具体 Agent 填充，例如：**XX确认**：确认 xxx 是否就绪]

---

## §0.5 Skill 加载路由

本 Agent 在不同流程步骤中需加载对应的 Skill 文件。**不在 §0 预读**，按 SOP 步骤触发时加载。

| SOP 步骤 | 触发条件 | 加载 Skill | 说明 |
|---------|---------|-----------|------|
| §5 Step N | [永远 / 布尔条件 / 状态取值] | `skills/{SKILL_NAME}.md` | [简要说明] |

> **注意**：路由逻辑是机械映射（无条件 / 布尔 / 从 workflow_state 机械取值），无需 Agent "判断"。详见 `SKILLS_EXTRACTION_PLAN.md` §六-A。

---

## §1 角色设定与核心约束

### 定位

[一句话描述本 Agent 的核心职责]

### 核心原则

1. [原则 1]
2. [原则 2]
3. [原则 3]

### 任务分级路由遵循

本 Agent 的所有任务必须先经过 `{coordinator_agent}` 的**任务分级路由判断**。

| 路由结果 | 本 Agent 行为 |
|---------|-------------|
| **快车道** | [说明] |
| **慢车道** | [说明] |

### §1.1 Pipeline Handoff Protocol

**本 Agent 分支定义**：

| Branch | 用途 | 触发场景 |
|--------|------|---------|
| Branch_1 | ... | ... |
| Branch_2 | ... | ... |

**交接格式**：
```markdown
@{target_agent} [Handoff: Branch_{N}] {任务描述}

[Mount Context]
1. {文件路径1}
2. {文件路径2}
```

**Diff Summary 回传义务**（回传 `{coordinator}` 审查时必须携带）：
```markdown
## [Diff Summary]
**变更范围 (Scope)**: [修改的文件/接口列表]
**核心逻辑变更 (Delta)**: [新增/删除/修改]
**风险自评**: [ ] DDL / [ ] 越权 / [ ] 金额 / [ ] 无高风险
**关联 AC**: [step_plan.md 任务 ID]
```

### §1.2 工具权限

- **Allowed**: [列出允许的工具和文件范围]
- **Forbidden**: [列出禁止的操作]

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
3. 确认任务类型
4. 覆盖写入 `docs/04_agent/memory/current/task_context.md`（使用模板 `docs/templates/TASK_CONTEXT_Template.md`）
5. 📋 CHECKPOINT（任务归属确认）→ 执行 §2.0 职责判定规则

**输出**：任务类型、当前步骤、目标 Skill、当前 Gate、CHECKPOINT 判定结果

### §2.2 Phase B: 知识获取

#### 任务类型：[名称]

**必读项**（Step 1 全部读完）：

| # | 知识项 | 来源 | 读取范围 | 预估行数 |
|---|--------|------|---------|---------|
| K1 | ... | ... | ... | ... |

**按需项**（Phase C 遇到不确定时查阅，不预读）：

| # | 知识项 | 来源 | 读取范围 | 触发条件 |
|---|--------|------|---------|---------|
| K6 | ... | ... | ... | [机械判断条件] |

#### Gap Detection / Bounded Expansion

从 Step 1 已加载的必读知识中，扫描跨模块引用信号（FK 引用、状态机跨模块、事件触发），按优先级加载关联知识（最多 3 项，每项 ≤50 行）。

### §2.3 Phase C: 规则执行

**准入条件**：Phase B 必读项全部已读。

1. 从 task_context.md 确认目标 Skill，读取该 Skill 文件
2. 逐条执行，每条标记 ✅/⚠️/❌
3. 遇到不确定的条目 → 按该条目的参考表格查阅知识层
4. 输出执行结果

### §2.4 Phase D: 完成与流转

1. 将本任务最终结果写入 session_notes.md
2. 更新 workflow_state.json（如涉及状态变更）
3. 清除/标记 `docs/04_agent/memory/current/task_context.md`
4. 交接下游 Agent（如需）
5. → 回到 §2.1 Phase A 重新定位

---

## §3 特殊流程

### §3.1 Hotfix 模式

*(触发：指令包含 `[Hotfix]` 或 `P0`/`P1` 关键词)*

[根据具体 Agent 填充 Hotfix 简化流程]

---

## §4 记忆与持久化

### §4.1 Token 预算护栏

- **单任务上下文上限**：8K Token
- **搜索结果截断**：不超过 500 行
- **文件数量硬限制**：同时读取文件 ≤4 个（不含全局配置文件）
- **记忆文件豁免**：`docs/04_agent/memory/global/` 和 `docs/04_agent/memory/modules/` 豁免，仅 `current/session_notes.md` 计入限制

### §4.2 上下文雪崩防护

遵循 `.ai/rules.md` §8.2。session_notes.md > 200 行时执行压缩。

### §4.3 会话结束状态更新

- 原则性决策（三问门禁通过） → `global/decisions.json`；具体方案归入对应文档
- 关键结论 → 压缩写入 `current/session_notes.md`

---

## §5 SOP 标准执行步骤

> [本 Agent 的标准执行流程，每个步骤内按 Phase A→B→C→D 微循环执行]

1. **记忆恢复**: 读取三层记忆文件
2. ...（根据具体 Agent 填充）
N. **提交/交接**: ...

---

## §6 与其他 Agent 的交互

| Agent | 交互场景 | 说明 |
|-------|---------|------|
| `agent_XX` (...) | ... | ... |
