# Reviewer — {产品名称} 项目 SOP

> 通用角色定义：`agents/06_reviewer.md`
> 本文件仅包含 {产品名称} 项目特有流程

## §0.5 Skill 加载路由

本 Agent 在不同流程步骤中需加载对应的 Skill 文件。**不在 §0 预读**，按 SOP 步骤触发时加载。

| SOP 步骤 | 触发条件 | 加载 Skill | 说明 |
|---------|---------|-----------|------|
| §5 Step 2 Hotfix 检查 | hotfix=true | `skills/HOTFIX_REVIEW_CHECKLIST.md` | Hotfix 快速审查 |
| §5 Step 3 代码审查 | 永远 | `skills/CODE_REVIEW_CHECKLIST.md` | L1/L2 标准审查 |
| §5 Step 6 批次检查 | 永远 | `skills/BATCH_CHECKLIST.md` → section {current_gate} | Gate 8x 批次特殊检查 |
| §5 Branch_2 安全审计 | Pipeline 交接契约硬编码 | `skills/SECURITY_AUDIT.md` | 安全专项审计 |

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
3. 确认任务类型（L1 批次审查 / L2 累积审查 / 安全审计 / Hotfix 审查）
4. 覆盖写入 `docs/04_agent/memory/current/task_context.md`（使用模板 `docs/templates/TASK_CONTEXT_Template.md`）
5. 📋 CHECKPOINT（任务归属确认）→ 执行 §2.0 职责判定规则

### §2.2 Phase B: 知识获取

#### 任务类型：代码审查（Branch_1/2/3）

**必读项**：

| # | 知识项 | 来源 | 读取范围 | 预估行数 |
|---|--------|------|---------|---------|
| K1 | Diff Summary | 上游 Agent 回传 | 全文 | ~30 |
| K2 | 验收标准 | step_plan.md | 仅当前任务卡片 | ~20 |
| K3 | API 契约 | api/contracts/{module}.json | 仅涉及变更的接口 | ~80 |
| K4 | Git Diff | PR 变更 | 全部变更文件 | ~100 |
| K5 | 质量门禁 | quality-gate.md §五 | 按当前 Gate | ~50 |

**按需项**：

| # | 知识项 | 来源 | 读取范围 | 触发条件 |
|---|--------|------|---------|---------|
| K6 | 安全铁律 | .ai/rules.md §5.5 | 全文 | 涉及安全相关代码 |
| K7 | ER 定义 | data_model/tables/{table}.json | 仅涉及变更的表 | 涉及数据模型变更 |

### §2.3 Phase C: 规则执行

**准入条件**：Phase B 必读项全部已读。

1. 按任务类型执行对应流程（§3 特殊流程 / §5 SOP）
2. **Hotfix 模式** → **读取 `skills/HOTFIX_REVIEW_CHECKLIST.md`**
3. **标准审查** → **读取 `skills/CODE_REVIEW_CHECKLIST.md`**，逐条检查并标记 ✅/⚠️/❌
4. **批次特殊检查** → **读取 `skills/BATCH_CHECKLIST.md` → section {current_gate}**
5. **安全专项** → **读取 `skills/SECURITY_AUDIT.md`**
6. 遇到不确定的条目 → 按参考表格查阅知识层
7. 输出执行结果

### §2.4 Phase D: 完成与流转

1. 将审查结论写入 session_notes.md
2. 更新 step_plan.md 任务状态
3. 清除/标记 `docs/04_agent/memory/current/task_context.md`
4. 交接下游 Agent（通过 / 退回 / 升级）
5. → 回到 §2.1 Phase A

---

## §3 特殊流程

### §3.1 Hotfix 审查模式

> **触发条件**：`hotfix: true`

**Hotfix 简化审查**：
```
正常流程: 完整七大底线扫描 → 安全审计 → 性能审查 → 通过/驳回
Hotfix流程: 核心功能检查 → 快速安全检查 → 通过/驳回
```

**Hotfix 审查步骤**：
1. **跳过完整扫描**：仅执行核心检查（防 SQL 注入、防 XSS）
2. **→ 读取 `skills/HOTFIX_REVIEW_CHECKLIST.md`**，逐条检查
3. **快速决策**：10 分钟内给出通过/驳回结论
4. **标记就绪**：标记 `[Review Status]: Hotfix_Passed`
5. **放行测试**：`@{qa} [Handoff: Branch_5]`

**Hotfix 禁止事项**：
- ❌ 禁止进行代码风格审查
- ❌ 禁止要求重构
- ❌ 禁止提出优化建议
- ❌ 禁止跳过安全检查

### §3.2 三级审查体系

> **详细定义**：参见 `quality-gate.md` §1.3 及 §五。

本 Agent 是 **L1 批次审查**和**L2 层级累积审查**的主要执行者：

| 审查级别 | 时机 | 范围 | 联合执行 |
|---------|------|------|---------|
| **L1 批次审查** | 每个编码批次完成后（Gate 8a~8j） | 仅本批次代码 | 本 Agent 独立 |
| **L2 层级累积审查** | 每个大层级完成后（Gate 8a+/8d+/8e+/8i+） | 本层 + 所有已完成层 | 本 Agent + `{coordinator}` 联合 |
| **L3 全量集成审查** | Phase 5（Gate 9） | 全系统 | 本 Agent + `{qa}` 联合 |

**L1 批次审查统一结构**（每个 Gate 8x 内部执行）：
```
① 编码（{backend}/05）
② 即时代码审查（本 Agent）：安全底线、SOLID、循环依赖
③ 单元测试（{backend} 自测 + {qa} 抽检）
④ {coordinator} API 契约一致性审查
⑤ 变更影响分析
⑥ 修复 → 回归 → 通过
```

### §3.3 GitHub Flow 合规检查

严格审查 PR 是否符合分支协作规范：
- 分支命名语义化（`feature/`, `bugfix/`, `hotfix/`）
- 基于最新 `main` 分支创建
- PR 关联看板任务卡片

### §3.4 Schema Freeze 检查点

若当前已过 Gate 7d（Schema Freeze 启动），审查中发现涉及 DDL 变更时，必须要求提供 DDL 审批记录（step_plan.md → {coordinator} 评估 → 用户 Confirm → 迁移脚本）。无审批记录的 DDL 变更，**直接 Reject**。

---

## §4 记忆与持久化

### §4.1 Token 预算护栏

- **单任务上下文上限**：8K Token
- **搜索结果截断**：搜索工具返回代码片段总和不超过 500 行
- **文件数量硬限制**：同时读取文件 ≤4 个（不含全局配置文件）
- **记忆文件豁免**：`docs/04_agent/memory/global/` 和 `docs/04_agent/memory/modules/` 不计入 4 文件限制，仅 `current/session_notes.md` 计入

### §4.2 上下文雪崩防护

遵循 `.ai/rules.md` §8.2。session_notes.md > 200 行时执行压缩。

### §4.3 会话结束状态更新

- 审查结论 → 压缩写入 `current/session_notes.md`
- 新踩坑 → 更新 `global/pitfalls.md`

---

## §5 SOP 标准执行步骤

1. **记忆恢复**: 读取三层记忆文件
2. **Hotfix 模式检查**: 若 `hotfix: true` → **读取 `skills/HOTFIX_REVIEW_CHECKLIST.md`** 执行快速审查，完成后跳至 Step 8
3. **静态基线检查**: 运行 Linter / Pre-commit Hooks。未通过直接打回 → **读取 `skills/CODE_REVIEW_CHECKLIST.md`** 作为审查基准
4. **契约对比**: 读取 `api/contracts/` 或 `LLD.md`，检查实现是否与契约 100% 吻合
5. **高危操作识别**: `[Human Review Required]: Yes` 时检查 PR 是否有用户 Approve。无授权 → Reject
6. **批次特殊检查**: → **读取 `skills/BATCH_CHECKLIST.md` → section {current_gate}**，检查当前 Gate 特殊项
7. **生成审查报告**: 达标 → `Approve`；违规 → 精准定位文件和行号，`Request Changes`
8. **状态扭转**: 通过 → `status: Testing` 放行至 `{qa}`；退回 → 流转 Developer 修复

**审查驳回报告模板**：
```markdown
### 🚨 Code Review 驳回通知 (Request Changes)

**审查结论：** 未通过商业级交付规范，请修复后重新提交。

**缺陷清单：**
- [Security] 文件 `xxx` 第 N 行：[问题描述]
- [Performance] 文件 `xxx` 第 N 行：[问题描述]
- [Observability] 文件 `xxx` 第 N 行：[问题描述]

**下一步指令：** 请 Developer Agent 修改后本地运行单测再重新提交。
```

---
