# Backend — {产品名称} 项目 SOP

> 通用角色定义：`agents/04_backend.md`
> 本文件仅包含 {产品名称} 项目特有流程

## §0.5 Skill 加载路由

本 Agent 在不同流程步骤中需加载对应的 Skill 文件。**不在 §0 预读**，按 SOP 步骤触发时加载。

| SOP 步骤 | 触发条件 | 加载 Skill | 说明 |
|---------|---------|-----------|------|
| §5 Step 12 提交前自检 | 永远 | `skills/BACKEND_SELF_CHECK.md` | 后端商业级自检 |
| 代码审查（被请求时） | 永远 | `skills/CODE_REVIEW_CHECKLIST.md` | 作为审查方使用 |

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
3. 读取 step_plan.md → 锁定当前 `Doing` 任务卡片
4. 确认任务类型（接口开发 / 业务逻辑 / 数据库迁移 / Bug 修复 / Hotfix）
5. 覆盖写入 `docs/04_agent/memory/current/task_context.md`（使用模板 `docs/templates/TASK_CONTEXT_Template.md`）
6. 📋 CHECKPOINT（任务归属确认）→ 执行 §2.0 职责判定规则

### §2.2 Phase B: 知识获取

#### 任务类型：后端编码（Branch_1/2/4）

**必读项**：

| # | 知识项 | 来源 | 读取范围 | 预估行数 |
|---|--------|------|---------|---------|
| K1 | 任务卡片 | step_plan.md | 仅当前 Doing 卡片 | ~20 |
| K2 | API 契约 | api/contracts/{module}.json | 全文 | ~100 |
| K3 | ER 定义 | data_model/tables/{table}.json | 仅涉及变更的表 | ~50 |
| K4 | LLD 设计 | LLD.md | 仅相关章节 | ~80 |
| K5 | 测试用例 | plan/test_cases/{task}.md | 全文 | ~40 |

**按需项**：

| # | 知识项 | 来源 | 读取范围 | 触发条件 |
|---|--------|------|---------|---------|
| K6 | 枚举/状态机 | data_model/enums/{module}_status.json | 仅涉及变更的枚举 | 状态流转逻辑 |
| K7 | State Machine Dict | data_model/state-machines/{module}.json | 状态机相关变更 | 转换合法性校验 |
| K8 | Permission Registry | api/permission_registry.json | 权限相关变更 | permission_code 来源 |
| K9 | NFR Registry | design/NFR_REGISTRY.md | 限流/缓存相关 | rate_limit / TTL 数值 |
| K7 | 防腐层接口 | src/backend/interfaces/ | 仅相关接口文件 | ACL 确认 |

### §2.3 Phase C: 规则执行

**准入条件**：Phase B 必读项全部已读。

1. 按任务类型执行对应流程（§3 特殊流程 / §5 SOP）
2. **提交前** → **读取 `skills/BACKEND_SELF_CHECK.md`**，逐条检查并标记 ✅/⚠️/❌
3. **代码审查（被请求时）** → **读取 `skills/CODE_REVIEW_CHECKLIST.md`**，逐条检查并标记
4. 遇到不确定的条目 → 按参考表格查阅知识层
5. 输出执行结果

### §2.4 Phase D: 完成与流转

1. 将开发结论写入 session_notes.md
2. 更新 step_plan.md 任务状态
3. 清除/标记 `docs/04_agent/memory/current/task_context.md`
4. 交接下游 Agent
5. → 回到 §2.1 Phase A

---

## §3 特殊流程

### §3.1 Hotfix 模式 (紧急修复)

> **触发条件**：收到 `[Handoff: Branch_5]` 或 PRD 包含 `hotfix: true` 标记

**Hotfix 简化流程**：
```
正常流程: Draft → Reviewing → Approved → WIP → In_Review → Testing → Ready_for_Release → Done
Hotfix流程: Draft → Approved → WIP → Testing → Ready_for_Release → Done
                    ↑ 跳过 Reviewing 和 In_Review
```

**Hotfix 执行步骤**：
1. **快速确认分支**：确保在 `hotfix/*` 分支上工作
2. **读取简化文档**：仅读取 `PRD_hotfix.md` 和 `LLD_delta.md`
3. **最小化修改**：仅修复核心问题，不进行重构
4. **简化测试**：仅运行核心功能测试，不做完整回归
5. **快速提交**：使用 `git commit -m "hotfix: [问题描述]"` 格式
6. **标记就绪**：在 `step_plan.md` 标记 `[Hotfix Ready]: Yes`
7. **通知下游**：使用 `@{qa} [Handoff: Branch_5]` 请求简化测试

**Hotfix 禁止事项**：
- ❌ 禁止进行代码重构
- ❌ 禁止添加新功能
- ❌ 禁止修改非相关模块
- ❌ 禁止跳过核心功能测试

**Hotfix 完成后补齐**：
- 必须在下一迭代补齐完整单元测试
- 必须更新相关文档（如有遗漏）

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

- 新踩坑或约定 → 更新 `global/pitfalls.md` 或 `global/conventions.md`
- 关键结论 → 压缩写入 `current/session_notes.md`

---

## §5 SOP 标准执行步骤

1. **记忆恢复**: 读取三层记忆文件
2. **数据库版本校验**: 读取 `step_plan.md` 的 `[Migration Version]`，查询 `schema_migrations` 表。版本不匹配 → 拒绝开发，输出版本不一致提示
3. **分支确认**: 确保在独立 feature/bugfix/hotfix 分支上工作，严禁 `main` 直接开发
4. **任务接管**: 读取 `plan/step_plan.md`，锁定 `Doing` 或 `Bug-P*` 任务
5. **Bug 状态识别**: 若任务状态为 `Bug-P*`，读取 `[Bug Reference]` 获取 Issue 详情
6. **读取测试用例**: 读取 `plan/test_cases/` 对应任务的测试用例大纲（TDD 前置）
7. **防腐层确认**: 检查任务"防腐层依赖"字段，确认接口已存在于 `src/backend/interfaces/`
8. **挂载上下文**: 读取任务卡片 `[Mount Context]` 列表，加载指定文件
9. **编码与单测**: 根据 `api/contracts/` 和 `LLD.md` 编写业务代码。**脏数据物理拦截铁律**：编写业务代码前必须先定义 DTO/Schema 校验层
10. **人类门禁识别**: 若当前任务 `[Human Review Required]: Yes`，完成编码后强制挂起，等 [用户 Approve] 才能 commit
11. **验证与自愈**: 运行测试，失败则按排错模板分析修复，最多重试 3 次。3 次仍失败 → 标记 `Blocked` 呼叫人类介入
12. **商业级自检**: → **读取 `skills/BACKEND_SELF_CHECK.md`**，逐条检查并标记 ✅/⚠️/❌
13. **代码提交**: 自检通过后 `git commit -m "feat/fix: [任务名称]"`
14. **标记 Backend Ready**: 若涉及 API 实现，标记 `[Backend Ready]: Yes (commit: abc123)`
15. **发起 PR**: 向 `main` 发起 Pull Request，关联看板任务卡片
16. **状态流转**: 修改 step_plan.md 和文档 YAML 为 `status: In_Review`，交接给 `{reviewer}`
17. **代码索引更新**: 更新 `_index.json` 的 `"code"` 字段，同步本批次新增/变更的模块包路径和接口
18. **Bug 修复回归**: 若任务是 Bug 修复，自动流转给 `{qa}` 回归验证

**排错输出模板**（遇错时强制使用）：
```text
【自我纠错报告】
- 预期运行结果：[描述期望的正确输出]
- 实际异常表现：[描述当前的错误现象]
- 完整报错日志：[粘贴终端关键 Error Trace]
- 根本原因分析：[分析为何会出错]
- 解决方案：[说明接下来将修改哪个文件的哪几行代码]
```

---
