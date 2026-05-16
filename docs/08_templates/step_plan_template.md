---
doc_type: "STEP_PLAN"
module_id: "module_name"
version: "V 1.0"
phase: "Phase_3_Architecture"
status: "Draft"
complexity: "L3"
author_agent: "{architect}"
reviewer_agent: "{coordinator_agent}"
last_updated: "YYYY-MM-DDTHH:mm:ssZ"
approved_by: ""
depends_on: ["prd_module"]
acl_dependencies: []
---

# 任务执行计划 (step_plan.md) 模板

> **系统{修订人} ({architect})** 必须在需求包的 `plan/` 目录下生成名为 `step_plan.md` 的文件。
> **后端开发 ({backend})** 和 **前端开发 ({frontend})** 必须严格执行并打勾。
>
> **文件位置**：`docs/backend/prd/{层A}/{ModuleCode}/YYYYMMDD_Desc/plan/step_plan.md`

---

## ⚠️ 重要约定

1. **[Human Review Required] 标识规则**：
   - 凡涉及以下**高危任务类型**，该项**必须**标记为 `Yes`：
     - 核心财务计算（金额、折扣、结算）
     - 复杂状态机流转（BPM 审批流、订单状态）
     - 权限控制（UAC、RBAC、数据可见性）
     - 数据迁移（DDL 变更、数据清洗）
     - 第三方集成（支付、短信、邮件）
   - 标记为 `Yes` 的任务，**人类必须亲自 Review 代码逻辑**，Agent 完成编码后必须强制挂起等待人类授权

2. **两段式审查制**：
   - **第一阶段（骨架）**：仅输出 Task Name 和 Mount Context，等待 {coordinator} 审计 + **[用户 Approve]**
   - **第二阶段（血肉）**：填充 AC（验收标准），再次等待 {coordinator} 审计 + **[用户 Approve]**

3. **TDD 用例前置**：
   - `{qa_agent}_engineer` 会基于此模板提前编写测试用例大纲到 `plan/test_cases/`
   - 开发完成后必须跑通所有测试用例才能提交

4. **Bug 完整生命周期**：
   ```
   测试发现 Bug → {coordinator} 定级建议 → [用户 Decide] 确认等级 & 是否立即处理
       ↓
   修复完成 → 自动流转 {qa} 回归验证
       ↓
   验证通过 → 状态更新为 Done
   验证失败 → 打回继续修复
   ```

   **Bug 状态标记**：
   - `Bug-P0/P1/P2/P3` 表示缺陷等级
   - 开发 Agent 必须读取 `[Bug Reference]` 获取 Issue 详情

5. **防腐层依赖必填**：
   - 每个任务**必须**包含 `防腐层依赖` 字段
   - Phase 3 阶段会自检，缺失必须补充后才能提交

6. **WIP=1 约束**：
   > **注意**：WIP=1 限制仅在并行开发场景下需要显式执行。串行开发模式下，一次只处理一个任务，天然满足 WIP=1 约束。

---

## 当前所属迭代 / Epic: [填写名称]
## 当前关联 PRD: [填写相对路径]
## 复杂度级别: [ ] L1-Strategic [ ] L2-Domain [ ] L3-Feature [ ] L4-UserStory

---

### Task 1: [具体动作描述，如：实现 UAC 组织树查询接口]

- **状态**: [ ] Todo / [ ] Doing / [x] Done / [ ] Blocked / [ ] **Bug-P0 / [ ] Bug-P1 / [ ] Bug-P2 / [ ] Bug-P3**
- **[Human Review Required]**: [ ] Yes / [x] No
- **[Mock Status]**: [ ] Not Needed / [ ] Pending / [x] Verified
- **[Backend Ready]**: [x] Yes (commit: abc123) / [ ] No

> **注意**：Mock 状态仅在并行开发场景下使用。串行开发模式下，后端先完成（`[Backend Ready]: Yes`），前端开发时直接调用真实接口。
- **[Bug Reference]**: #IssueID（仅 Bug 状态时填写）
- **验收标准 (AC)**:
  1. [正向流程] 接口路径为 `/api/v1/uac/departments/tree`，返回层级嵌套结构 (children)
  2. [异常处理] 当部门不存在时，返回 HTTP 404 和标准错误码
  3. [边界条件] 当部门数量超过 1000 时，启用分页或懒加载
  4. [权限校验] 通过权限拦截器校验，仅返回当前用户有权限查看的部门
- **[Mount Context]** (必须挂载的受控文件路径，上限4个):
  1. `docs/api/contracts/`
  2. `plan/LLD_UAC.md`
  3. `src/backend/services/department_service.py`
  4. `tests/unit/test_department.py`
- **防腐层依赖**:
  - 数据库: PostgreSQL (需通过 Repository 接口抽象)
  - 缓存: Redis (需通过 Cache 接口抽象)
- **约束**: 请遵守 `docs/backend/specs/DEV_STANDARDS.md` 进行开发，完成后必须运行本地自测。
- **执行日志**: [开发者完成任务后，在这里填写关键 MR 的 hash 或简单结论]

---

### Task 2: [具体动作描述 - 高危任务示例：订单金额计算]

- **状态**: [ ] Todo
- **[Human Review Required]**: [x] Yes ⚠️ **涉及财务计算，人类必须亲自 Review**
- **[Mock Status]**: [x] Not Needed
- **[Backend Ready]**: [ ] No
- **[Bug Reference]**: -
- **验收标准 (AC)**:
  1. [正向流程] 计算订单总金额 = 商品金额 × 数量 - 折扣 + 运费
  2. [精度处理] 金额使用分为单位，避免浮点精度问题
  3. [异常处理] 当折扣金额超过商品金额时，返回 HTTP 400
  4. [审计日志] 记录每次金额计算的关键参数和结果
  5. [并发控制] 使用乐观锁防止并发修改
- **[Mount Context]**:
  1. `docs/api/contracts/`
  2. `plan/LLD_Order.md`
  3. `src/backend/services/order_service.py`
  4. `src/backend/models/order.py`
- **防腐层依赖**:
  - 数据库: PostgreSQL (需通过 Repository 接口抽象)
  - 分布式锁: Redis (需通过 Lock 接口抽象)
- **约束**: 此任务涉及财务计算，完成后必须挂起等待 **[用户 Approve]** 后才能提交。
- **执行日志**:

---

### Task 3: [具体动作描述 - 前端任务示例：订单列表页面]

- **状态**: [ ] Todo
- **[Human Review Required]**: [ ] Yes / [x] No
- **[Mock Status]**: [ ] Not Needed / [x] Pending / [ ] Verified
- **[Backend Ready]**: [ ] No（后端接口未就绪，使用 Mock 开发）
- **[Bug Reference]**: -
- **验收标准 (AC)**:
  1. [正向流程] 页面路径为 `/orders`，展示订单列表，支持分页
  2. [交互] 点击订单行跳转至详情页
  3. [状态展示] 订单状态使用不同颜色标签区分
  4. [权限] 根据用户角色显示/隐藏操作按钮
- **[Mount Context]**:
  1. `docs/api/contracts/`
  2. `docs/backend/specs/`
  3. `src/components/business/OrderCard/`
  4. `src/pages/orders/`
- **防腐层依赖**:
  - API 客户端: 需通过 ApiClient 接口抽象
- **约束**: 后端接口未就绪时使用 Mock 开发，标记 `[Mock Status]: Pending`。后端就绪后切换真实 API 并标记 `Verified`。
- **执行日志**:

---

## 任务汇总

| Task ID | 任务名称 | Human Review | Mock Status | 涉及类型 | 优先级 |
|---------|---------|--------------|-------------|---------|--------|
| 1 | UAC 组织树查询 | No | Not Needed | - | P2 |
| 2 | 订单金额计算 | Yes ⚠️ | Not Needed | 财务计算 | P0 |
| 3 | 订单列表页面 | No | Pending | 前端 | P1 |

---

## 审批记录

### 第一阶段审批（骨架）
- **审批人**: [用户]
- **审批时间**: [YYYY-MM-DD HH:mm]
- **审批结果**: [ ] **[用户 Approve]** / [ ] Reject
- **版本快照**: 骨架 v1.0（用于回退对比）
- **备注**:

### 第二阶段审批（血肉）
- **审批人**: [用户]
- **审批时间**: [YYYY-MM-DD HH:mm]
- **审批结果**: [ ] **[用户 Approve]** / [ ] Reject
- **版本快照**: 血肉 v1.0（用于回退对比）
- **备注**:

## 回退历史

| 时间 | 触发人 | 回退类型 | 回退原因 | 恢复版本 |
|------|--------|---------|---------|---------|
| - | - | - | - | - |

> **回退类型**: Skeleton-Rollback（骨架回退）/ Requirement-Change（需求变更）

---

## 业务一致性审计（{coordinator}）

### 骨架审计
```markdown
### ✅ 业务审计通过（骨架）
**审计时间**: [YYYY-MM-DD HH:mm]
**审计人**: {coordinator}
**审查依据**: [基于 Diff Summary] / [基于源文件深读]
**审计结论**: 任务划分完整，覆盖 PRD 边界
**下一步**: 请用户审查并回复 **[用户 Approve]** 以放行
---
```
*（若不通过，替换为 🚨 业务审计意见模板）*

### 血肉审计
```markdown
### ✅ 业务审计通过（血肉）
**审计时间**: [YYYY-MM-DD HH:mm]
**审计人**: {coordinator}
**审查依据**: [基于 Diff Summary] / [基于源文件深读]
**审计结论**: AC 覆盖 PRD 的 NFR 要求
**下一步**: 请用户审查并回复 **[用户 Approve]** 以放行
---
```
*（若不通过，替换为 🚨 业务审计意见模板）*

**🚨 业务审计意见模板（不通过时使用）**：
```markdown
### 🚨 业务审计意见 (不通过)
**审计时间**: [YYYY-MM-DD HH:mm]
**审计人**: {coordinator}
**问题**: [具体问题描述，如：任务 3 遗漏了 PRD 中"并发超卖"的处理逻辑]
**要求**: [修改要求，如：补充任务或修改 AC]
---
```

---

## ⚠️ 回退机制

### 触发条件

| 场景 | 触发条件 | 回退类型 |
|------|---------|---------|
| 血肉阶段发现骨架缺陷 | AC 无法覆盖的边界场景，需要新增/删除 Task | Skeleton-Rollback |
| 需求变更 | 用户主动提出需求调整 | Requirement-Change |

### 回退操作流程

**场景 A：血肉阶段回退到骨架阶段**
```
发现骨架需要调整
    ↓
在 step_plan.md 记录 🔄 回退申请
    ↓
@{coordinator} [Handoff: Branch_5] 请求回退评估
    ↓
[用户 Confirm] 后执行回退
    ↓
恢复到骨架版本，重新走审批流程
```

**场景 B：需求变更**
```
用户提出需求变更
    ↓
{pm} 评估变更影响范围
    ↓
[用户 Decide] 变更范围
    ↓
若影响骨架 → 触发 Skeleton-Rollback
若仅影响 AC → 修改 AC 后重新血肉审计
```

### 回退申请模板

```markdown
### 🔄 回退申请
**申请时间**: [YYYY-MM-DD HH:mm]
**申请人**: [Agent ID / 用户]
**回退类型**: [ ] Skeleton-Rollback / [ ] Requirement-Change
**回退原因**: [具体描述]
**影响范围**: [哪些 Task 受影响]
**恢复版本**: [骨架 vX.Y / 血肉 vX.Y]
**数据库影响**: [ ] 涉及（需执行 DOWN 脚本） / [ ] 不涉及
**下一步**: 请 {coordinator} 确认后，等待 [用户 Confirm] 执行回退
---
```

> ⚠️ **数据库回滚铁律**：若回退涉及数据库变更，**必须先执行 DOWN 脚本回滚物理环境**，再恢复文档版本。

---

## 技术债引用

> 当用户拒绝回退时，在此记录技术债条目，并在 `docs/04_agent/memory/global/technical_debt.json` 中创建完整记录。

| 债务ID | 描述 | 风险等级 | 还债目标 |
|:---|:---:|:---:|:---|
| - | - | - | - |

> **若存在技术债，{architect} 产出 step_plan 时必须同步更新 `technical_debt.json`**
