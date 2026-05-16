# Frontend — {产品名称} 项目 SOP

> 通用角色定义：`agents/05_frontend.md`
> 本文件仅包含 {产品名称} 项目特有流程

## §0.5 Skill 加载路由

本 Agent 在不同流程步骤中需加载对应的 Skill 文件。**不在 §0 预读**，按 SOP 步骤触发时加载。

| SOP 步骤 | 触发条件 | 加载 Skill | 说明 |
|---------|---------|-----------|------|
| §5 Step 12 编码完成提交前 | 永远 | `skills/FRONTEND_SELF_CHECK.md` | 前端商业级自检 |

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
4. 确认任务类型（页面开发 / 组件开发 / API 对接 / Bug 修复 / UI 修订）
5. 覆盖写入 `docs/04_agent/memory/current/task_context.md`（使用模板 `docs/templates/TASK_CONTEXT_Template.md`）
6. 📋 CHECKPOINT（任务归属确认）→ 执行 §2.0 职责判定规则

### §2.2 Phase B: 知识获取

#### 任务类型：前端编码（Branch_1/2/3/4）

**必读项**：

| # | 知识项 | 来源 | 读取范围 | 预估行数 |
|---|--------|------|---------|---------|
| K1 | 任务卡片 | step_plan.md | 仅当前 Doing 卡片 | ~20 |
| K2 | API 契约 | api/contracts/{module}.json | 仅对接接口 | ~80 |
| K3 | 设计系统 |  | 组件清单 + Token | ~40 |
| K4 | LLD 设计 | LLD.md | 仅前端相关章节 | ~50 |
| K5 | 测试用例 | plan/test_cases/{task}.md | 全文 | ~40 |

**按需项**：

| # | 知识项 | 来源 | 读取范围 | 触发条件 |
|---|--------|------|---------|---------|
| K6 | Mock 数据 | src/mocks/data/{module}.json | 全文 | Backend Ready = No |
| K7 | 现有组件 | src/components/{type}/{name}/ | 按需 | 复用判断 |

### §2.3 Phase C: 规则执行

**准入条件**：Phase B 必读项全部已读。

1. 按任务类型执行对应流程（§3 特殊流程 / §5 SOP）
2. **提交前** → **读取 `skills/FRONTEND_SELF_CHECK.md`**，逐条检查并标记 ✅/⚠️/❌
3. 遇到不确定的条目 → 按参考表格查阅知识层
4. 输出执行结果

### §2.4 Phase D: 完成与流转

1. 将开发结论写入 session_notes.md
2. 更新 step_plan.md 任务状态
3. 清除/标记 `docs/04_agent/memory/current/task_context.md`
4. 交接下游 Agent
5. → 回到 §2.1 Phase A

---

## §3 特殊流程

### §3.1 Mock 机制（伪并行开发）

> 前端开发不应被后端接口阻塞，支持基于 API 契约的 Mock 开发模式。

**step_plan Mock 状态字段**：
```markdown
- **[Mock Status]**: [ ] Not Needed / [ ] Pending / [x] Verified
- **[Backend Ready]**: [ ] No / [x] Yes (commit: abc123)
```

**Mock 开发流程**：
1. **契约优先**：编码前确认 `api/contracts/` 已定义目标接口完整契约
2. **检查 Backend Ready 状态**：
   - `Yes` → 直接对接真实 API
   - `No` → 使用 Mock 开发，标记 `[Mock Status]: Pending`
3. **Mock 数据生成**：基于契约生成 Mock 数据，存放于 `src/mocks/`
   ```
   src/mocks/
   ├── handlers/          # MSW handlers 或类似拦截器
   └── data/              # Mock 响应数据
   ```
4. **开发切换**：通过环境变量 `VITE_USE_MOCK=true` 或 `NEXT_PUBLIC_USE_MOCK=true` 控制
5. **后端就绪后切换**：发现 `[Backend Ready]: Yes` 时，关闭 Mock，验证真实接口，更新 `[Mock Status]: Verified`

**Mock 数据规范**：
- 严格遵循 `API_CONTRACT.md` 响应结构
- 覆盖正常响应、空数据、错误状态
- 禁止硬编码敏感信息

**交接约定**：
- Mock 完成开发 → 标记 `[Mock Status]: Pending`
- 后端就绪 → `{backend}` 标记 `[Backend Ready]: Yes`
- 本 Agent 检测到 `[Backend Ready]: Yes` → 切换真实 API 并验证

### §3.2 Hotfix 模式 (紧急修复)

> **触发条件**：收到 `[Handoff: Branch_5]` 或 PRD 包含 `hotfix: true` 标记

**Hotfix 简化流程**：
```
正常流程: Mock开发 → Lint → 单元测试 → Review → 集成测试 → 发布
Hotfix流程: 直接修改 → 简化Lint → 核心页面验证 → 发布
```

**Hotfix 执行步骤**：
1. **跳过 Mock**：直接修改目标页面/组件，不创建新 Mock
2. **最小化修改**：仅修复 UI 问题（错位、文案、样式）
3. **简化验证**：仅验证受影响页面，不做完整 E2E 测试
4. **快速提交**：使用 `git commit -m "hotfix: [问题描述]"` 格式
5. **标记就绪**：在 `step_plan.md` 标记 `[Hotfix Ready]: Yes`
6. **通知下游**：使用 `@{qa} [Handoff: Branch_5]` 请求简化测试

**Hotfix 禁止事项**：
- ❌ 禁止重构组件结构
- ❌ 禁止更新 （除非修复组件 Bug）
- ❌ 禁止添加新页面或新组件
- ❌ 禁止跳过核心页面验证

### §3.3 Design System 维护职责

本 Agent 同时承担**设计系统维护者**角色。

**组件分类**：

| 类型 | 定义 | 目录位置 | 更新  |
|------|------|---------|----------------------|
| **基础组件** | 按钮、输入框、弹窗等通用 UI 元素 | `src/components/base/` | ✅ |
| **业务组件** | 跨页面复用的业务模块 | `src/components/business/` | ✅ |
| **页面组件** | 单页面独有组件 | `src/pages/` 或 `src/views/` | ❌ |

**必须更新  的场景**：
1. 新建基础组件
2. 新建业务组件
3. 引入新 UI 组件库
4. 新增全局 CSS 变量
5.  可复用组件清单为空或标记 `[待补充]`

**更新规范**：
- 更新 §2 UI 组件库版本（如引入新库）
- 更新 §4 可复用组件清单（组件名称、路径、功能说明、使用场景）

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
2. **分支确认**: 确保在独立 feature/bugfix/hotfix 分支上工作
3. **任务接管**: 读取 `plan/step_plan.md`，锁定 `Doing` 或 `Bug-P*` 任务
4. **Bug 状态识别**: 若 `Bug-P*`，读取 `[Bug Reference]` 获取 Issue 详情
5. **读取测试用例**: 读取 `plan/test_cases/` 测试用例大纲（TDD 前置）
6. **防腐层确认**: 检查"防腐层依赖"字段，不存在则标记 `Blocked` 呼叫 `{architect}` 补充
7. **检查 Mock 状态**: 读取 `[Backend Ready]` → `Yes` 对接真实 API，`No` 使用 Mock 并标记 `[Mock Status]: Pending`
8. **人类门禁识别**: `[Human Review Required]: Yes` 时，完成编码后强制挂起，等 [用户 Approve] 才能 commit
9. **精准检索与挂载**: 使用搜索工具定位相关组件，限制挂载文件数量
10. **编码验证**: 编写组件，执行 `npm run lint` 或 `npm run build`
11. **设计系统同步**: 检查是否新建基础/业务组件，若有则更新 ``
12. **商业级自检**: → **读取 `skills/FRONTEND_SELF_CHECK.md`**，逐条检查并标记 ✅/⚠️/❌
13. **代码提交**: 自检通过后确保安全钩子通过，执行封存
14. **状态流转**: 修改 step_plan.md 和文档 YAML 为 `status: In_Review`，交接给 `{reviewer}`
15. **Bug 修复回归**: 若任务是 Bug 修复，自动流转给 `{qa}` 回归验证

---
