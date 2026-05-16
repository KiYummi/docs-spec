# **项目开发管理规范**

## **文档控制信息**

* **文档状态**: \[√\] 正式发布 \[ \] 草稿 \[ \] 废弃  
* **当前版本**: V1.0  
* **生效日期**: {生效日期}  
* **核心管控模式 (Lean MVP \+ Kanban \+ Harness Engineering \+ DevOps)**: 最小可行性产品 (MVP) \+ 看板管理 \+ AI 协同约束 \+ 持续集成与交付 (CI/CD)

### **修订记录**

| 版本号 | 修订日期 | 修订内容摘要 | 修订人 | 审核人 |
| :---: | :---: | ----- | :---: | :---: |
| V1.0 | {生效日期} | 初始版本发布 | {修订人} | {审核人} |
| V1.1 | {修订日期} | 新增 Agent 记忆持久化机制、多环境配置管理、更新流程图 | {修订人} | {审核人} |
| V1.2 | {修订日期} | 新增任务分级路由、上下文雪崩防护、活文档强制要求、更新 UAT 清单 | {修订人} | {审核人} |
| V1.3 | 2026/3/23 | Phase 术语统一、三层记忆结构增加 modules 层、UAT 补充热修场景 | {修订人} | {审核人} |

## **1\. 语义化版本控制规范 (Semantic Versioning)**

本项目及所有工程产出物的版本号升迁，严格遵循语义化版本控制规范（SemVer 2.0.0）。版本号格式固定为 `vX.Y.Z`（主版本号.次版本号.修订号）。

### **1.1 版本号递增规则**

所有发布至生产环境的版本，必须遵循以下升迁逻辑：

* **主版本号 (Major \- X)**：当系统进行颠覆性架构重构、UI/UX 整体改版，或引入不向下兼容的 API 及业务逻辑修改时递增。递增后，Y 和 Z 必须归零。  
* **次版本号 (Minor \- Y)**：当系统新增向下兼容的业务模块、功能特性，或对现有功能进行较大规模增强时递增。递增后，Z 必须归零。  
* **修订号 (Patch \- Z)**：当系统进行向下兼容的缺陷修复（Bugfix）、安全漏洞补丁更新或局部性能优化时递增。

### **1.2 预发布版本标签标识**

对于尚未达到生产发布标准，但需要在测试环境（Staging）进行验证的版本，需在标准版本号后追加预发布标签：

* **Alpha 版 (`-alpha.x`)**：内部研发自测版本，功能可能不完整且存在已知缺陷。  
* **Beta 版 (`-beta.x`)**：外部公测版本，核心功能已锁定，重点进行缺陷修复与稳定性验证。  
* **RC 版 (`-rc.x`)**：候选发布版本，原则上不再修改代码，仅用于最终上线前的验收测试。

### **1.3 文档及交付物版本协同**

* **工程文档同步**：核心受控文档（如 `PRD.md`、`HLD.md`）的内部版本号应与系统主体迭代节奏保持一致。  
* **交付基线**：每次对外正式发布（Release）时，必须在 Git 代码库中打上对应的版本标签（Tag），并同步更新根目录下的 `CHANGELOG.md`。

## **2\. 总则**

### **2.1 适用范围与预期读者**

本规范适用于本项目（及后续衍生 {应用层} 项目）的软件生命周期管理。**特别适用于单人主导 \+ AI 辅助编程（如 Cursor 等）的敏捷开发模式。**

* **预期读者**：{修订人} (PM)、研发工程师、自动化 AI 编程助手、测试与运维人员。

### **2.2 术语与定义**

| 术语/缩写 | 全称 | 解释说明 |
| :---: | ----- | ----- |
| SSOT | Single Source of Truth | 单一数据源，指项目的业务逻辑和架构规范均以 docs/ 目录下的受控文档为唯一准则。 |
| MVP | Minimum Viable Product | 最小可行性产品，指满足核心业务主流程运转的精简版本。 |
| WIP | Work In Progress | 在制品，指当前正在开发或处理中的任务项。 |
| AC | Acceptance Criteria | 验收标准，判定单个任务卡片是否开发完成的客观条件。 |
| Harness | Harness Engineering | 驾驭工程，指为 AI 编程助手提供受控上下文、物理隔离和自我验证循环的研发理念。 |

## **3\. 目录结构与资产管控规范**

本项目采用**代码库与文档库一体化**架构模式。文档库作为 `docs/` 子目录存在于项目根目录下。

### **3.1 项目目录结构**

```text
<PROJECT_NAME>/
├── src/                          # 源代码目录
│   ├── frontend/                 # 前端代码
│   └── backend/                  # 后端代码
├── tests/                        # 测试代码
├── .github/                      # CI/CD
├── .ai/rules.md                  # AI 规则
├── CLAUDE.md                     # Claude Code 入口
├── GEMINI.md                     # Gemini CLI 入口
├── README.md
├── agents/           # Agent 角色定义（含 skills/ 可复用检查清单、base_agent_template.md, step_plan_template.md）
└── docs/                         # 📂 文档库（子目录）
    ├── 00_meta/          # 全局架构与规范
    │   ├── Templates/            # 文档模板（含 step_plan_template.md 等；ER/ENUM/Index 模板已迁移为 JSON Schema，见 _schemas/*.json）
    │   ├── dev-spec.md
    │   ├── metadata-dictionary.md
    │   ├── master-prd.md
    │   └── ...
    ├── backend/prd/{层A}/             # 底座平台需求包
    ├── backend/prd/{层B}/             # 业务应用需求包
    ├── 03_Bugfix_And_Ops/        # 运维与修复
    ├── internal/                 # 内部文档
    ├── delivery/                 # 交付文档
    └── docs/04_agent/memory/            # Agent 记忆
```

### **3.2 文档库结构 (docs/)**

`DOCS_REPO_PATH` 环境变量默认为 `./docs`，指向项目根目录下的文档库子目录。
> **💡 新项目初始化**：执行初始化脚本即可一键创建完整目录结构：
> ```bash
> bash $GLOBAL_TEMPLATES_PATH/scripts/init_project.sh <项目名>
> ```

```text
docs// (外部业务资产大本营)
├── 00_meta/              # 全局架构与系统宪法 (静态受控)
│   ├── ADR/                      # 架构决策记录 (Architecture Decision Records)
│   ├── Templates/                # 📋 文档模板（只读，不填内容）
│   ├── master-prd.md             # 核心产品白皮书 (业务边界与路线图)
│   ├── global-blueprint.md       # 全局架构蓝图与执行顺序规划
│   ├── metadata-dictionary.md    # 全局元数据与状态机字典
│   ├── dev-spec.md               # 项目开发管理规范总纲
│   └── glossary.md               # 统一业务词典与领域概念库
│
├── backend/                      # MVP 初始开发（Phase 3~6 产出）
│   ├── data_model/               # Gate 4: ER + Enum + State Machine Dictionary
│   │   ├── tables/                # 表结构 JSON（按 _schemas/er_schema.json）
│   │   ├── enums/                 # 枚举值 JSON（按 _schemas/enum_schema.json，不含 FSM）
│   │   └── state-machines/        # 状态机字典 JSON（按 _schemas/state_machine_schema.json）[新建]
│   ├── api/                      # Gate 5: API Contract + Permission Registry + 错误码 + 幂等规范
│   │   ├── contracts/             # API 契约 JSON（按 _schemas/api_contract_schema.json）
│   │   ├── permission_registry.json  # 权限注册表（全局 SSOT）[新建]
│   │   ├── error_codes.json
│   │   ├── IDEMPOTENCY_SPEC.md
│   │   └── FRONTEND_ROUTES.md
│   ├── security/                 # Gate 6: 红蓝报告 + 架构健康度报告
│   ├── design/                   # Gate 7a: GLOBAL_HLD + DESIGN_SYSTEM + DEV_STANDARDS + EVENT_REGISTRY + NFR_REGISTRY + SECURITY_BASELINE + 缓存/FF/权限矩阵/监控
│   ├── lld/                      # Gate 7b~7d: MASTER_LLD + 各模块 LLD + step_plan + migrations
│   ├── coding/                   # Phase 4: seeds
│   └── testing/                  # Phase 5: E2E 测试用例 + 性能基线
│
├── backend/prd/{层A}/                 # 底座平台层（8 模块，PRD 已定型）
│   └── {ModuleCode}/              # 模块目录 (如：{平台层}_{模块C})
│       └── _overview/             # 模块静态参考文档
│           └── {模块名}.md
│
├── backend/prd/{层B}/                 # 业务应用层（9 模块，PRD 已定型）
│   └── {ModuleCode}/              # 模块目录 (如：CRM)
│       └── _overview/             # 模块静态参考文档
│           └── {模块名}.md
│
├── 03_Bugfix_And_Ops/            # 小需求与缺陷修复工单包
│
├── 09_iterations/                # 迭代开发（MVP 之后，按需求包组织）
│   └── YYYYMMDD_Desc/            # requirements/ + plan/ + reasoning/
│
├── planning/                     # 规划文档（可选，持续维护）
│
├── delivery/                     # 交付文档
│
├── internal/                     # 内部文档
│
└── docs/04_agent/memory/                # Agent 记忆持久化（三层结构）
    ├── global/                    # 全局层（长期，结构化）【豁免】
    │   ├── decisions.json          # 原则性决策（工作方法论/产品哲学/核心概念定义，非具体方案）
    │   ├── conventions.md         # 编码约定
    │   ├── pitfalls.md            # 踩坑记录（按模块分类）
    │   └── workflow_state.json     # 流程状态（Agent_02 维护）
    ├── modules/                   # 模块层（按领域）【豁免】
    │   ├── UAC/
    │   │   └── pitfalls.md
    │   ├── Order/
    │   └── Inventory/
    ├── current/                   # 当前迭代（临时）【计入限制】
    │   └── session_notes.md       # 本轮对话的结构化摘要
    └── per_release/               # 归档层（Phase 6 发版后）
        └── vX.Y.Z/
            ├── summary.md         # 版本记忆快照
            └── {需求包名}/         # 本次发版涉及的需求包
                └── reasoning/      # AI 推理路径归档（从需求包 reasoning/ 复制）
```

### **3.3 动态需求管理原则 (The PRD Package Pattern)**
为了保证全局架构的纯洁性，所有新需求或重构任务，**严禁在 `_meta` 内直接草拟**。
*   **沙盒建包**：产品或{修订人}必须在 `backend/prd/{层A}` 或 `backend/prd/{层B}` 的对应模块目录下（如 `backend/prd/{层A}/{平台层}_{模块C}/`），新建带时间戳的独立需求包（如 `20260321_Init`）。
*   **闭环交付**：开发、测试及 AI Agent 的所有文档协作（PRD/LLD/step_plan）均限制在该需求包内。
*   **全局沉淀**：当该需求包开发完毕并准备合并至主干时，若其产生了新的全局状态码或基础术语，必须同步更新回 `docs/00_meta/` 下的对应文件。

### **3.4 统一通信协议 (Unified Handoff Protocol)**

所有 Agent 之间的交接必须使用标准化的 `[Handoff: Branch_X]` 前缀协议，确保意图明确、上下文完整。

#### **3.4.1 协议格式**

```
@{target_agent} [Handoff: Branch_{N}] {任务描述}

[Mount Context]
1. {文件路径1}
2. {文件路径2}
3. {文件路径3}
4. {文件路径4}  <!-- 最多 4 个 -->
```

#### **3.4.2 各 Agent 分支定义**

| Agent | Branch_1 | Branch_2 | Branch_3 | Branch_4 | Branch_5 |
|-------|----------|----------|----------|----------|----------|
| **{pm}** (PM) | 探索性对话 | 项目建站 | Master PRD | 蓝图规划 | 子领域 PRD |
| **{coordinator}** (Coordinator) | 路由判断 | 阶段审查 | 缺陷定级 | UAT Sign-off | 回退建议 |
| **{architect}** (Architect) | 架构设计 | 骨架生成 | 血肉填充 | 回退执行 | 架构修订 |
| **{backend}** (Backend) | 接口开发 | 业务逻辑 | 数据库迁移 | Bug 修复 | 紧急修复 |
| **{frontend}** (Frontend) | 页面开发 | 组件开发 | API 对接 | Bug 修复 | UI 修订 |
| **{reviewer}** (Reviewer) | 代码审查 | 安全审计 | 性能审查 | - | - |
| **{qa}** (QA) | 测试计划 | 测试执行 | Bug 报告 | PRD 红蓝对抗 | 回归测试 |
| **{devops}** (DevOps) | 环境部署 | CI/CD 配置 | 发版执行 | 热修发版 | 回滚执行 |

> **注**：{pm} 额外支持 Branch_6 (红蓝修补)、Branch_7 (变更评估)、Branch_8 (Hotfix 模式)

#### **3.4.3 交接示例**

```markdown
# {architect} → {backend} (开发交接)
@{backend} [Handoff: Branch_1] 请按 step_plan.md Task-3 实现 UAC 组织树查询接口

[Mount Context]
1. /docs/02_backend/prd/{层A}/{平台层}_{模块C}/20260322_Init/plan/step_plan.md
2. /docs/02_backend/prd/{层A}/{平台层}_{模块C}/20260322_Init/plan/LLD.md
3. /docs/03_api/contracts/
4. docs/00_meta/glossary.md
```

```markdown
# {backend} → {coordinator} (审查请求)
@{coordinator} [Handoff: Branch_2] Task-3 开发完成，请求 API 契约一致性审查

[Diff Summary]
**变更范围 (Scope)**: 修改 src/backend/services/department_service.py, 新增 tests/unit/test_department.py
**核心逻辑变更 (Delta)**:
- 新增: 实现组织树查询接口及单元测试
- 修改: 调整了部门数据校验规则
**风险自评**:
- [ ] 涉及数据库 DDL 变更
- [ ] 涉及权限/越权逻辑
- [ ] 涉及核心金额计算
- [x] 无高风险变更
**关联 AC**: step_plan.md Task-3 验收标准

[Mount Context]
1. /docs/02_backend/prd/{层A}/{平台层}_{模块C}/20260322_Init/plan/step_plan.md
2. /docs/03_api/contracts/
```

#### **3.4.4 上下文传递铁律**

1. **4 文件上限**：`[Mount Context]` 最多 4 个文件路径
2. **上下文硬隔离**：下游 Agent 只能读取 Mount Context 指定的文件
3. **会话清空**：交接时必须清空当前会话的 Message History
4. **Reasoning 传递**：若需求包内存在 `reasoning/*.md`，必须作为 Mount Context 的一部分传递
5. **Diff Summary 回传**：下游 Agent 完成任务后回传 `{coordinator}` 审查时，**必须**携带标准化的 `[Diff Summary]`（含变更范围、核心逻辑变更、风险自评、关联 AC），详见 `{coordinator_agent}.md` §1.1.1

## **4\. AI 智能体研发流水线与交付物契约 (Agentic Pipeline & Artifacts)**

为了确保多智能体（Multi-Agent）在协作过程中不产生"幻觉"和"边界外溢"，本项目的研发过程被严格划分为 6 个切面阶段。每个阶段都由特定的 Agent 负责，且必须遵循**"准入模板 -> 标准动作 -> 产出模板"**的强制交接棒契约 (Handoff Protocol)。

> **⚠️ 流水线架构升级说明**：本项目流水线已从传统的线性串行模式升级为**带拦截网的非线性网状结构（铁三角会审制）**。
> - **测试左移**：QA Agent (Agent_07) 在 Phase 2 阶段就介入，对 PRD 进行红蓝对抗攻击
> - **全流程 {审核人}**：Agent_02 (Coordinator) 不再仅负责路由，而是作为"业务护城河"参与 Phase 3-6 的跨阶段审查
> - **非线性流转**：产出不能直接流入下一阶段，必须经过业务审计门禁

### **4.0 铁三角会审制 (Iron Triangle Review)**

本项目采用**铁三角会审制**，确保业务、技术、用户三方制衡：

```
           ┌─────────────────┐
           │     [用户]       │ (最终决策权)
           └────────┬────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
┌───────┴───────┐       ┌───────┴───────┐
│ Agent_02      │       │ 执行 Agent    │
│ (业务护卫)     │◄─────►│ (技术实现)    │
└───────────────┘       └───────────────┘
```

- **用户**：最终决策者，对高危操作拥有一票否决权
- **Agent_02 (业务护卫)**：负责业务防偏离审查，拥有主动向 `docs/04_agent/memory/global/decisions.json` 写入原则性决策的特权（须通过三问门禁）
- **执行 Agent**：负责技术实现，产出需经 Agent_02 审查

**非线性流转示意**：
```
Phase 1/2 ──────────────────────────────────────────────► Phase 6
  │                                                    ▲
  │  PRD ──► Agent_07 (红蓝对抗) ──► Agent_01         │
  │           │                        │              │
  │           ▼                        ▼              │
  │       修补PRD ◄── Agent_02 ◄── Agent_03          │
  │                   (业务审计)     (架构设计)        │
  │                                     │              │
  │                                     ▼              │
  │                              Agent_04/05 ◄── Agent_02 (API审查)
  │                                     │              │
  │                                     ▼              │
  │                              Agent_06/07 ──► Agent_02 (缺陷定级)
  │                                     │              │
  └─────────────────────────────────────┴──────────────┘
```

### **4.1 PRD 拆解体系 (L1-L4 分级)**

本项目的 PRD 采用四级拆解体系，根据复杂度评估选择合适粒度：

| 级别 | 名称 | 适用场景 | 特征 |
|------|------|---------|------|
| **L1** | Strategic (战略级) | MVP 边界定义、核心业务目标 | 高层愿景，不涉及具体功能 |
| **L2** | Domain (领域级) | 模块拆分（如 UAC、订单、库存） | 领域边界清晰，涉及多个 Feature |
| **L3** | Feature (功能级) | 单个功能点（如组织树查询、订单创建） | 可独立测试，有明确 AC |
| **L4** | User Story (用户故事) | 具体操作（如"作为管理员，我想批量导入用户"） | 单一场景，可在 1-2 天内完成 |

**复杂度评估维度**：
- 并发复杂度：无/简单/需锁机制/高并发分布式锁
- 数据隔离：单租户/逻辑隔离/行级权限/物理隔离
- 主数据风险：无/低/中(可恢复)/高(不可逆)

### **4.2 流水线阶段与交付契约**

> **详细 Gate 定义**：每个 Gate 的准入条件、交付物清单、评估维度、准出条件，详见 `docs/05_plans/quality-gate.md`（29 个 Gate，三级审查体系，评估维度矩阵）。

| Gate | 阶段 (Phase) | 核心目标 | 负责人/Agent | 必须产出的标准文档 (Output) | 下游承接方 | 门禁条件 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **G1** | **P1: 战略与规划** | 确定 MVP 宏观边界 | [用户] / `{pm}` | `master-prd.md`、`glossary.md` | `{pm}` | [用户 Approve] |
| **G2** | **P1 Step 2: 架构蓝图** | 生成 DAG 执行流与模块拆解 | `{pm}` | `global-blueprint.md` | `{coordinator}` | 灵魂三问 + [用户 Approve] |
| **G3** | **P2: 产品与需求设计** | Sub PRD + 红蓝对抗 | `{pm}` + `{qa}` | 14 份 PRD、红蓝攻击报告 | `{architect}` | Agent_07 攻击通过 + [用户 Approve] |
| **G4** | **P3: 数据模型** | ER 图 + 枚举字典 + 状态机字典 | `{architect}` + `{coordinator}` | `backend/data-model/tables/*.json`（141 张表）、`enums/*.json`（枚举值）、`state-machines/*.json`（状态机字典）、`SYNC_ISSUES_Phase1.md` | 后续 Gate | 16 项同步检查全过 + [用户 Approve] |
| **G5** | **P3: API 契约** | 全局 API 契约 + 权限注册表 + 错误码 + 幂等 | `{architect}` + `{coordinator}` | `api/contracts/`、`permission_registry.json`、`ERROR_CODE_DICT.md`、`FRONTEND_ROUTES.md`、`IDEMPOTENCY_SPEC.md` | 后续 Gate | Agent_02 API 审查 + 前端可用性确认 + [用户 Approve] |
| **G6** | **P3: 红蓝攻击+架构评估** | PRD 级 + 架构级安全评估 | `{qa}` + `{coordinator}` | `reports/REDBLUE_REPORT.md`、`ARCH_HEALTH_REPORT.md` | 后续 Gate | 红蓝对抗全通过 + 架构评估无 P0 + [用户 Approve] |
| **G7a** | **P3: Master LLD** | 全局架构落地 | `{architect}` + `{coordinator}` | `backend/specs/` 下 10 份文档（GLOBAL_HLD、DESIGN_SYSTEM、DEV_STANDARDS、AOP_DESIGN、CACHE_STRATEGY、FEATURE_FLAGS、DATA_PERMISSION_MATRIX、MONITORING_DASHBOARD、NFR_REGISTRY、SECURITY_BASELINE） | 后续 Gate | Agent_02 业务一致性审计 + [用户 Approve] |
| **G7b** | **P3: Sub LLD 骨架** | 各模块 LLD 骨架 | `{architect}` + `{coordinator}` | 各模块 LLD 骨架（Task Name + Mount Context） | 后续 Gate | 两段式第一阶段：骨架审计 + [用户 Approve] |
| **G7c** | **P3: Sub LLD 血肉** | LLD 完整版 + step_plan | `{architect}` + `{coordinator}` | 各模块 LLD 完整版 + `step_plan.md`（含 AC） | 后续 Gate | 两段式第二阶段：血肉审计 + [用户 Approve] |
| **G7d** | **P3: 迁移脚本** | Flyway UP+DOWN | `{architect}` | `backend/lld/migrations/` 迁移脚本 | 后续 Gate | UP→DOWN→UP 验证通过 → **Schema Freeze 启动** |
| **G8a~i** | **P4: 敏捷开发**（10 批次） | 按 DATA→COL→INT→{应用层}→前端 分批次编码，每批次执行 L1 审查 | `{backend}/05` + `{reviewer}`（L1） | 业务代码 + 单元测试 | L1/L2 审查 | 每批次 L1 审查通过（6 步流程）；每层完成后 L2 累积审查（G8a+/8d+/8e+/8i+） |
| **G9a~f** | **P5: 测试与验收**（6 门禁） | E2E→跨模块联动→安全渗透→性能基线→缺陷回归→UAT | `{reviewer}` + `{qa}` + `{coordinator}` | E2E 测试用例、性能基线、缺陷工单 | DevOps | 详见 §4.2.2 三级审查体系 |
| **G10** | **P6: 发布与交付** | 发版 + 交付文档 | `{devops}` + `{coordinator}` | RELEASE_NOTES、USER_MANUAL、DEPLOYMENT_GUIDE、DATA_INDEX、CHANGELOG | 最终用户 | UAT Sign-off + 9 项发版前置检查 + `[UAT Approved - Ready for Release]` |

#### 4.2.1 两段式审批与回退机制 (Two-Stage Review & Rollback)

> **铁律**：Phase 3 阶段的 `step_plan.md` 采用两段式审批（骨架 → 血肉），血肉阶段发现骨架问题时必须执行回退。

**两段式审批流程**：
```
第一阶段（骨架）
    ↓
{architect} 输出 Task Name + Mount Context
    ↓
{coordinator} 骨架业务审计
    ↓
[用户 Approve]
    ↓
第二阶段（血肉）
    ↓
{architect} 填充 AC（验收标准）
    ↓
{coordinator} 血肉业务审计
    ↓
[用户 Approve]
    ↓
下发开发
```

**回退触发条件**：

| 场景 | 触发条件 | 回退类型 |
|------|---------|---------|
| 血肉阶段发现骨架缺陷 | AC 无法覆盖的边界场景，需新增/删除 Task | Skeleton-Rollback |
| 需求变更 | 用户主动提出需求调整 | Requirement-Change |

**回退操作流程**：
```
发现骨架需要调整
    ↓
在 step_plan.md 记录 🔄 回退申请（含影响范围、恢复版本、数据库影响）
    ↓
@{coordinator} [Handoff: Branch_5] 请求回退评估（含数据库回滚检查）
    ↓
{coordinator} 输出 🔄 回退建议
    ↓
[用户 Confirm]
    ↓
🆕 若涉及数据库变更 → 先执行 DOWN 脚本回滚数据库
    ↓
确认后：回退到骨架版本，重新执行骨架审计 + 血肉审计
拒绝后：记录技术债，继续当前血肉填充
```

> ⚠️ **数据库回滚铁律**：若回退涉及数据库变更，**必须先执行 DOWN 脚本回滚物理环境**，再恢复文档版本。避免"幽灵表"导致开发环境与文档状态不一致。

**回退申请模板（含数据库字段）**：
```markdown
### 🔄 回退申请
**申请时间**: [YYYY-MM-DD HH:mm]
**申请人**: [Agent ID / 用户]
**回退类型**: [ ] Skeleton-Rollback / [ ] Requirement-Change
**回退原因**: [具体描述]
**影响范围**: [哪些 Task 受影响]
**恢复版本**: [骨架 vX.Y / 血肉 vX.Y]
**数据库影响**: [ ] 涉及（需执行 DOWN 脚本）/ [ ] 不涉及
**下一步**: 请 {coordinator} 确认后，等待 [用户 Confirm] 执行回退
---
```

**需求变更处理**：
- **小范围变更**（仅影响 AC）：直接修改 AC，重新执行血肉审计
- **大范围变更**（影响骨架）：执行 Skeleton-Rollback，重走两段式审批
- **变更记录**：所有变更必须记录在 `step_plan.md` 的"回退历史"表中

**版本快照要求**：
- 骨架审批通过后，记录"骨架 vX.Y"版本快照
- 血肉审批通过后，记录"血肉 vX.Y"版本快照
- 回退时通过快照对比确定恢复范围

#### 4.2.2 三级审查体系（L1/L2/L3）

> **详细定义**：参见 `docs/05_plans/quality-gate.md` §1.3 及 §五~§六。

| 级别 | 时机 | 范围 | 执行 Agent |
|------|------|------|-----------|
| **L1 批次审查** | 每个编码批次完成后（Gate 8a~8j） | 仅本批次代码 | `{reviewer}` 独立执行 |
| **L2 层级累积审查** | 每个大层级完成后 | 本层 + 所有已完成层 | `{reviewer}` + `{coordinator}` 联合 |
| **L3 全量集成审查** | Phase 5（Gate 9） | 全系统 | `{reviewer}` + `{qa}` 联合 |

**L1 批次审查统一结构**（每个 Gate 8x 内部执行）：
```
① 编码（{backend}/05）
② 即时代码审查（{reviewer}）：安全底线、SOLID、循环依赖
③ 单元测试（{backend} 自测 + {qa} 抽检）
④ {coordinator} API 契约一致性审查
⑤ 变更影响分析（本次变更涉及哪些表/API/已完成的模块）
⑥ 修复 → 回归 → 通过
```

**L1 通用评估维度**（每个批次都做）：

| # | 评估项 | 检查内容 |
|---|--------|---------|
| 1 | 编码规范 | DEV_STANDARDS.md 合规 |
| 2 | 安全底线 | SQL 防注入、软删除、tenant_id 强制、PII 脱敏 |
| 3 | PII + 多租户 | 本批次涉及的 PII 字段、tenant_id 覆盖 |
| 4 | TraceID | 跨模块调用是否透传 |
| 5 | 技术债记录 | 本批次妥协项写入 `docs/04_agent/memory/global/technical_debt.json` |
| 6 | 变更影响 | 本批次变更影响哪些已完成的模块 |

**L2 累积审查节点**：

| Gate | 名称 | 审查范围 | 重点 |
|------|------|---------|------|
| G8a+ | DATA 层累积 | DATA 全部 | 种子数据完整性、FK 依赖方向、RLS 覆盖 |
| G8d+ | {平台层} COL 层累积 | DATA + COL 全部 | DATA↔COL 接口边界、权限穿透、事件总线、AOP 切面 |
| G8e+ | {平台层} INT 层累积 | DATA + COL + INT 全部 | COL↔INT 接口边界、LLM 调用链、搜索索引 |
| G8i+ | {应用层} 层累积 | 全系统 | {平台层}↔{应用层} 耦合、业务链路完整性、状态机端到端 |

**各批次特殊检查项**（详见 `quality-gate.md` §五各 Gate 8x）：

| Gate | 范围 | 关键检查项 |
|------|------|-----------|
| G8a | DATA 层 13 模块 | 种子数据（17 种字典组）、FK 方向、RLS、字典引用 |
| G8b | {平台模块2}~02（权限+流程） | RBAC+ABAC、审批流状态机、4 预设角色（super_admin/admin/sub_admin/member） + 自定义角色 CRUD、10 审批模板 |
| G8c | {平台模块4}~05（工作台+内容+建模） | unified_task 双唯一索引、JSONB 混合存储、跨模块校验 7 条硬编码 |
| G8d | {平台模块7}~07（日志+连接器） | unified_log 写入性能、外部 API 集成硬编码、熔断限流 |
| G8e | {集成模块1}~05（智能+数据） | LLM 模型路由配置化、FTS 索引、编码引擎、报表聚合 |
| G8f | {应用层} MKT+TRX | 核心链路状态机端到端、金额精度 ROUND_HALF_UP |
| G8g | {应用层} PRJ+AI | AI 沙盒 @PhysicalDelete、SimHash、偏好漂移检测 |
| G8h | {应用层} FIN | NUMERIC(18,4) 金额、核销多对多、提成安全线 80%、成本预警阈值 |
| G8i | {应用层} OPS+PROC | knowledge_card 编译、知识库权限隔离、采购与销售对称 |
| G8j | 前端集成联调 | 契约一致性验证、设计系统合规、6 角色工作台切换 |

**Phase 5 测试门禁**（Gate 9a~9f）：

| Gate | 名称 | 测试范围 | 准出条件 |
|------|------|---------|---------|
| G9a | 全链路 E2E | lead→opportunity→quotation→contract→order→filing→case→payment→invoice；37 状态机 | 核心链路全绿 |
| G9b | 跨模块联动 | EVENT_REGISTRY 全事件、7 条跨对象校验、审批流+业务状态联动 | 事件全链路通过 |
| G9c | 安全渗透 | 多租户穿透、IDOR、批量枚举、XSS/SQL 注入、PII 暴露 | 无 P0/P1 安全问题 |
| G9d | 性能基线 | unified_task/unified_log/knowledge_card 查询；N+1 抽检；>500ms 告警 | 无 P0 性能问题，热点 <500ms |
| G9e | 缺陷回归 | P0/P1 缺陷全部修复并回归 | P0/P1 全修 + {coordinator} 确认 |
| G9f | UAT | 角色走查（管理员/普通成员 + 典型自定义角色） | [用户 Approve] |

#### 4.2.3 Schema Freeze 铁律

> **触发时机**：Gate 7d（数据库迁移脚本）完成后。

Gate 7d 完成后进入**表结构冻结期**。任何后续表结构变更必须走 DDL 审批流：

1. 在 `step_plan.md` 记录变更申请（含影响范围、回滚方案）
2. `{coordinator}` 评估影响（检查依赖模块、API 契约、迁移脚本）
3. 等待 [用户 Confirm]
4. 确认后：新增迁移脚本（UP + DOWN）


### 4.3 多智能体流水线可视化拓扑 (Agentic Workflow Diagram)

```mermaid
graph TD
    %% Define styles
    classDef human fill:#f9f,stroke:#333,stroke-width:2px;
    classDef agent fill:#e1f5fe,stroke:#333,stroke-width:2px;
    classDef docs fill:#fff3e0,stroke:#333,stroke-width:1px,stroke-dasharray: 5 5;
    classDef code fill:#e8f5e9,stroke:#333,stroke-width:1px;
    classDef guard fill:#ffebee,stroke:#333,stroke-width:1px;
    classDef memory fill:#f3e5f5,stroke:#333,stroke-width:1px;
    classDef decision fill:#fff9c4,stroke:#333,stroke-width:2px;

    %% Actors
    User((用户)):::human
    Agent01[{pm}<br/>Enterprise PM]:::agent
    Agent02[{coordinator}<br/>Coordinator]:::agent
    Agent03[{architect}<br/>System Architect]:::agent
    Agent04[{backend}<br/>Backend Dev]:::agent
    Agent05[{frontend}<br/>Frontend Dev]:::agent
    Agent06[{reviewer}<br/>Code Reviewer]:::agent
    Agent07[{qa}<br/>QA Engineer]:::agent
    Agent08[{devops}<br/>DevOps]:::agent

    %% Task Routing Decision
    TaskRouter{🚦 任务分级路由}:::decision
    FastLane[快车道<br/>直接执行]:::guard
    SlowLane[慢车道<br/>完整流水线]:::guard

    %% Artifacts - External Docs Repo
    subgraph Enterprise Workspace (External Docs)
        MasterPRD[master-prd.md<br/>glossary.md]:::docs
        DesignSystem[]:::docs
        DomainPRD[PRD_Feature.md]:::docs
        LLD[LLD_Feature.md<br/>API_CONTRACT.md]:::docs
        StepPlan[step_plan.md]:::docs
    end

    %% Artifacts - Local Code Repo
    subgraph Code Repository ({PROJECT_NAME})
        AgentMemory[docs/04_agent/memory/<br/>global/modules/current]:::memory
        SourceCode[src/ & tests/]:::code
        Changelog[CHANGELOG.md]:::code
        LivingDocs[docs/07_delivery/<br/>RELEASE_NOTES.md<br/>DATA_INDEX.md]:::docs
    end

    %% Constraints
    subgraph Guardrails
        TokenBudget[Token 预算: ≤8K/500行/4文件]:::guard
        PreCommit[Pre-Commit: Lint必过]:::guard
        Parallel[并行守则: 串行交接]:::guard
        ContextPruning[上下文雪崩防护<br/>Rerank+摘要压缩]:::guard
    end

    %% Task Routing Flow
    User -- "提交任务" --> Agent01
    Agent01 -- "PRD定稿后" --> Agent02
    Agent02 -- "路由判断" --> TaskRouter
    TaskRouter -- "快车道" --> FastLane
    TaskRouter -- "慢车道" --> SlowLane
    FastLane -- "直接执行" --> User
    SlowLane -- "进入流水线" --> DomainPRD

    %% Workflow - P0: 全自动项目初始化
    User -- "P0: 新建项目 [项目名]" --> Agent01
    Agent01 -- "自动创建文档库" --> MasterPRD
    Agent01 -- "自动初始化代码库<br/>+ 配置 .env" --> SourceCode

    %% Workflow - Phase 1/2: 需求设计
    User -- "Phase 1: 提供愿景" --> Agent01
    Agent01 -- "输出蓝图" --> Blueprint[global-blueprint.md<br/>DAG依赖树]:::docs
    Blueprint -- "灵魂三问" --> HumanGate{人工审批断点}:::decision
    HumanGate -- "Approve" --> Agent01_Sub[{pm}<br/>按 DAG 顺序拆解子 PRD]:::agent
    Agent01_Sub -- "Phase 2: 需求设计" --> DomainPRD

    DomainPRD -- "挂载上下文" --> Agent03
    Agent03 -- "Phase 3: 架构设计" --> LLD
    Agent03 -- "任务拆解" --> StepPlan

    %% Memory Recovery - All agents read memory first
    AgentMemory -.->|"记忆恢复"| Agent04
    LLD -.-> Agent04
    StepPlan -.-> Agent04
    Agent04 -- "Phase 4: 编码&单测 (WIP=1)" --> SourceCode
    Agent04 -.->|"记忆更新"| AgentMemory

    AgentMemory -.->|"记忆恢复"| Agent05
    StepPlan -.-> Agent05
    DesignSystem -.->|前端必读| Agent05
    Agent05 -- "Phase 4: 前端开发<br/>+ 设计系统同步" --> SourceCode
    Agent05 -.->|"记忆更新"| AgentMemory

    SourceCode -- "Phase 5: 触发检查" --> Agent06
    Agent06 -- "静态分析&审计" --> SourceCode
    SourceCode -- "触发集成测试" --> Agent07
    Agent07 -- "黑盒验证" --> SourceCode

    SourceCode -- "Phase 6: 合并主干" --> Agent08
    Agent08 -- "打标&发版" --> MasterPRD
    Agent08 -- "交付物生成" --> Changelog
    Agent08 -- "生成活文档<br/>(UAT后、tag前)" --> LivingDocs

    %% Guardrails connections
    TokenBudget -.-> Agent04
    TokenBudget -.-> Agent05
    PreCommit -.-> Agent04
    PreCommit -.-> Agent05
    ContextPruning -.-> Agent01
    ContextPruning -.-> Agent03
```

### 4.4 UAT Sign-off 发版拦截 (Release Gate)

> **铁律**：即使代码已经合入 main 分支，`{devops}` 也**绝对不允许**直接打 Git Tag 或触发生产部署。

**发版前置条件**（9 项完整清单，参见 `quality-gate.md` §Gate 10）：
1. **@{coordinator} [Handoff: Branch_4]**：请求 UAT Sign-off，确认《发版资产与业务验收表》已齐备
   - [ ] PRD 文档完整
   - [ ] LLD/API 契约已更新
   - [ ] 测试报告通过
   - [ ] 红蓝对抗用例全绿
   - [ ] 缺陷定级完成（P0/P1 已修复）
   - [ ] 技术债总结（high 风险标注）
   - [ ] 种子数据导入脚本就绪
   - [ ] 备份策略就绪
   - [ ] Feature Flag 租户白名单就绪
2. **显式等待用户授权**：`{devops}` 必须在终端输出：
   ```
   ⚠️ 发版前 UAT Sign-off 检查：
   - [x] PRD 文档完整
   - [x] LLD/API 契约已更新
   - [x] 测试报告通过
   - [x] 红蓝对抗用例全绿
   - [x] 缺陷定级完成 (P0/P1 已修复，使用 Bug 优先级而非 Phase)
   - [x] 技术债总结（high 风险标注）
   - [x] 种子数据导入脚本就绪
   - [x] 备份策略就绪
   - [x] Feature Flag 租户白名单就绪

   请确认以上资产已齐备并通过验收。确认后请回复 `[UAT Approved - Ready for Release]` 以放行。
   ```
3. **无授权不发版**：若未收到用户的明确授权指令，**绝对禁止**执行后续的 `git tag` 和部署动作

#### 4.4.1 紧急发版通道（热修场景）

> **适用场景**：生产环境核心功能中断、安全漏洞、数据丢失风险等紧急情况。

**触发条件**（满足任一）：
- 生产环境核心功能中断
- 安全漏洞
- 数据丢失风险

**简化 UAT 流程**：
```
热修请求 → [用户 Approve] 确认紧急发版
    ↓
仅检查核心资产（PRD/LLD/API 契约）
    ↓
跳过活文档生成
    ↓
快速发版（优先级标记：hotfix/*）
```

**热修 Sign-off 模板**：
```markdown
### 🚨 紧急发版 Sign-off

**触发时间**: [YYYY-MM-DD HH:mm]
**触发原因**: [核心功能中断/安全漏洞/数据丢失风险]
**热修分支**: hotfix/[描述]

**核心资产检查**:
| 检查项 | 状态 |
|--------|------|
| PRD 核心变更已记录 | [ ] 通过 |
| LLD 关键设计已更新 | [ ] 通过 |
| API 契约已同步 | [ ] 通过 |

**豁免项**: 活文档生成、完整测试报告

**请确认**: 回复 `[Hotfix Approved]` 立即发版
---
```

### 4.5 多智能体工作流执行指南 (Step-by-Step Workflow)

为防止遗忘，以下是本项目（及基于本脚手架创建的任何新项目）从 0 到 1 的标准实操流转说明。所有指令均由人类在 IDE 终端或 AI 对话框中发出。

**Step 0: 全新项目初始化 (仅建站时执行一次) - 全自动模式**
- **用户动作**: 告诉 `{pm}`: "新建项目 [项目名]" 或 "创建 [项目名] 项目"
- **Agent 自动执行**:
  1. **创建文档库**: 在 `$WORKSPACE_ROOT/Docs/[项目名]/` 下创建标准目录结构 (`_meta`, `backend/prd/{层A}`, `backend/prd/{层B}`, `03_Bugfix_And_Ops`)，其中 `backend/prd/{层A}` 和 `backend/prd/{层B}` 内按 `{ModuleCode}/` 组织模块，每个模块下含 `_overview/` 和 `YYYYMMDD_Desc/` 需求包
  2. **初始化代码库**: 在 `${HOME}/projects/[项目名]/` 下拉取模板，自动配置 `.env`（替换 `<PROJECT_NAME>`），执行 `git init` 和初始提交
  3. **输出报告**: 告知用户文档库和代码库的路径
- **用户动作**: `cd` 到新项目目录，开始 Step 1

**Step 1: 业务宏观蓝图设计 (Phase 1)**
- **用户动作**: 告诉 `{pm}`: "我们要开发第一期 MVP，核心目标是 [你的愿景]。请更新 `MASTER_PRD`。"
- **Agent 流转**: `{pm}` 读取要求，在 `docs//_meta` 目录下产出 `master-prd.md` 和初始的 `glossary.md` 业务词典。

**Step 2: 全局架构蓝图规划与 DAG 拆解 (Phase 1 Step 2)**
- **用户动作**: 告诉 `{pm}`: "基于 Master PRD，输出子 PRD 规划清单和 DAG 依赖图。"
- **Agent 流转**: `{pm}` 进入 [分支 4]，输出 `global-blueprint.md`，并在终端触发"灵魂三问"硬性中断（Hard Stop）。
- **门禁与截断**: 等待用户回复 `Approve`。一旦获批，`{pm}` **强制结束当前会话**，交还控制权。

**Step 3: 领域需求拆解 (Phase 2)**
- **Agent 流转**: `{coordinator}` 读取 Blueprint 中的 `depends_on` 依赖，按 DAG 拓扑顺序使用**协议前缀** `@{pm} [Handoff: Branch_5]` 唤醒 `{pm}`。
- **Agent 执行**: `{pm}` 直接进入 [分支 5]，在对应模块目录下新建需求包（如 `backend/prd/{层A}/{平台层}_{模块C}/20260411_Init/`），并输出详细的带有 YAML 状态机的 `PRD_模块A.md`。完成后再次截断会话。

**Step 4: 架构与技术设计 (Phase 3)**
- **用户动作**: 告诉 `{architect}`: "PRD 已经定稿，请进行架构设计并拆解开发任务。"
- **Agent 流转**: `{architect}` 读取上述 PRD。在同一需求包内输出数据库设计 `LLD_模块A.md`，并在其中生成微观执行计划 `step_plan.md`，同时按需更新全局 API 合约文件（JSON 格式，由 `_schemas/` 下对应 Schema 校验）。

**Step 5: AI 沙盒编码与自测 (Phase 4)**
- **用户动作**: 告诉 `{backend}`: "计划已就绪，开始执行代码开发。"
- **记忆恢复**: `{backend}` 首先读取 `docs/04_agent/memory/` 下的三个文件（decisions.json（原则性决策）, conventions.md, pitfalls.md），恢复项目历史上下文。
- **Agent 流转**: `{backend}` 读取外部的 `step_plan.md`，在本地代码库 (`src/`) 严格遵循 WIP=1 原则写代码。如果报错，它会自我修复。
- **Pre-Commit 强制执行**: 在 `git commit` 前，Agent 必须主动运行 `npm run lint` / `pytest` 等检查命令。若被 hook 拦截，必须读取日志并修复后重试，**严禁使用 `--no-verify` 跳过**。
- **Token 预算约束**: 单任务上下文 ≤ 8K Token，搜索结果 ≤ 500 行，同时读取文件 ≤ 4 个。
- **前端 Agent 专属**: `{frontend}` 在编码前必须检查 `docs//backend/specs/` 中的可复用组件清单，优先复用已有组件。
- **记忆更新**: 若开发过程中发现新的约定或踩坑，Agent 必须更新 `docs/04_agent/memory/` 对应文件。
- **完成后动作**: 在 `step_plan.md` 里打 `[x]` 并执行极小范围的 `git commit`。

**Step 6: 审查与验收 (Phase 5)**
- **Agent 流转 (自动或受用户触发)**: `{reviewer}` 拦截检查代码底线（越权、SQL注入等）；`{qa}` 基于 PRD 中的 AC (验收标准) 运行集成测试，或将 Bug 提交到 GitHub Issues 闭环。

**Step 7: 发版 (Phase 6) - 含 UAT Sign-off**
- **用户动作**: 告诉 `{devops}`: "本期需求已测试通过，准备打 Release 标签发版。"
- **UAT Sign-off 门禁** (⚠️ **强制执行**):
  1. **@{coordinator} [Handoff: Branch_4]**：`{devops}` 必须使用标准协议请求 UAT Sign-off，确认《发版资产与业务验收表》已齐备
  2. **显式等待用户授权**：在终端输出："⚠️ 发版前 UAT Sign-off 检查：请确认资产已齐备。确认后请回复 `[UAT Approved - Ready for Release]` 以放行。"
  3. **无授权不发版**：若未收到用户的明确授权指令，**绝对禁止**执行后续的 `git tag` 和部署动作
- **Agent 流转** (收到 `[UAT Approved - Ready for Release]` 后): `{devops}` 会执行以下动作：
  1. **更新项目** - 更新 `CHANGELOG.md` 和用户说明书。
  2. **打标发布** - 打上 `vX.Y.Z` 标签，并 `git push --tags` 触发线上生产环境部署。

**循环**: 下一个 Sprint 或有新需求？回到 **Step 2** 继续。
任何一个 Agent 在被唤醒时，如果发现其依赖的 **输入文档 (Input)** 为空、不完整或未按照标准模板编写，**必须立即挂起任务并抛出异常**，严禁依靠大模型的预训练知识进行盲目编造。

### 4.6 任务分级路由机制 (Fast/Slow Lane Router)

> **铁律**：所有任务必须先经过 `{coordinator}` 的路由判断，由 **[用户 Confirm]** 后才能决定执行路径。

#### 4.6.1 分层路由机制 (Two-Layer Routing)

本系统采用**两层路由**机制，确保意图识别和复杂度评估分离：

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户输入                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  第一层：{pm} 意图判断 (Intent Classification)               │
│  ─────────────────────────────────────────────────────────────  │
│  判断用户意图属于哪个分支：                                       │
│  • Branch_1: 探索性对话（不落库）                                │
│  • Branch_2: 项目建站（跑脚本）                                  │
│  • Branch_3: Master PRD（战略级）                               │
│  • Branch_4: 蓝图规划（拆解模块）                                │
│  • Branch_5: 子领域 PRD（功能级）                               │
│  • Branch_6: 红蓝修补（PRD 修复）                               │
│  • Branch_7: 需求变更评估（影响分析）                            │
│  • Branch_8: Hotfix 模式（紧急修复）                            │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │ 快速路径 │   │ PRD 路径 │   │ 变更评估 │
        │ Branch 1 │   │ Branch 3-6│   │ Branch 7 │
        │ 直接执行 │   │           │   │ 输出报告 │
        └──────────┘   └──────────┘   └──────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  第二层：{coordinator} 复杂度路由 (Complexity Routing)                │
│  ─────────────────────────────────────────────────────────────  │
│  判断任务应该走快车道还是慢车道：                                 │
│  • 快车道：直接执行，不走流水线                                  │
│  • 慢车道：进入完整 Phase 1-6 流水线                            │
└─────────────────────────────────────────────────────────────────┘
```

**关键规则**：
1. **意图优先**：{pm} 的意图判断是**第一优先级**，决定工作流类型
2. **复杂度后置**：{coordinator} 的路由判断**仅在 PRD 路径**（Branch 3-6）中生效
3. **Hotfix 特殊**：Branch_8 走简化流程，跳过 {coordinator} 路由

#### 4.6.2 快/慢车道判断

**执行流程**：
```
接收任务 → {pm} PRD定稿 → {coordinator} 路由判断 → 输出路由建议 → [用户 Confirm] → 分发执行
```

**快车道条件**（满足任一即可）：
| 条件 | 说明 | 示例 |
|------|------|------|
| 单文件修改 | 仅涉及 1 个文件的改动，且非核心业务逻辑 | "修改 README 里的错别字" |
| 明确 Bug 修复 | 根因已定位，修复方案明确 | "第 45 行的变量名拼写错误" |
| 简单查询 | 不涉及代码生成，仅解释/查询 | "这个函数是做什么的？" |
| 文档微调 | 格式调整、错别字、补充说明 | "给 API 文档补充一个示例" |
| 配置变更 | 非生产环境配置调整 | "开发环境加一个环境变量" |

**慢车道条件**（满足任一必须走完整流水线）：
| 条件 | 说明 | 触发流水线 |
|------|------|----------|
| 新增业务模块 | 涉及新实体、新流程 | Phase 1 → 2 → 3 → 4 → 5 → 6 |
| 数据库变更 | 表结构、字段、索引的增删改 | Phase 3 → 4 → 5 → 6（DDL 审批流） |
| 权限/财务/状态机 | 高危操作 | Phase 2 → ... → 5 + **人类门禁** |
| 跨文件修改 | 涉及 2 个以上文件的联动修改 | Phase 3 → 4 → 5 |
| 需求不明确 | 用户描述模糊，需要进一步澄清 | 先进入 Phase 2 需求澄清 |
| **紧急热修** | 核心功能中断/安全漏洞/数据风险 | **简化 UAT** → 快速发版（hotfix/*） |

**与 PRD 动态分级的关系**：
- **任务路由 (本节)**：决定"要不要走流水线" → 快车道直接执行，慢车道进入流水线
- **PRD 分级 (§4.1)**：只有慢车道才会触发，决定"PRD 拆解到什么粒度" (L1-L4)

#### 4.6.3 术语对照表 (Terminology Glossary)

> ⚠️ **重要**：以下术语在本规范中有明确定义，禁止混淆使用

| 术语 | 英文 | 定义 | 使用场景 | 决策者 |
|------|------|------|---------|--------|
| **任务路由** | Task Routing | 判断任务是否需要走完整流水线 | 用户提出需求时 | {coordinator} |
| **快车道** | Fast Lane | 不走流水线，直接执行 | 简单修改、Bug 修复 | {coordinator} 判定 |
| **慢车道** | Slow Lane | 进入完整 Phase 1-6 流水线 | 新功能、跨模块修改 | {coordinator} 判定 |
| **PRD 分级** | PRD Leveling | 决定 PRD 文档的拆解粒度 | PRD 撰写时 | {pm} |
| **L1-L4** | Levels 1-4 | PRD 文档的四级粒度定义 | PRD 撰写时 | {pm} |
| **复杂度评估** | Complexity Assessment | 评估任务的并发/隔离/数据风险 | 任务路由判断时 | {coordinator} |
| **意图判断** | Intent Classification | 判断用户输入属于哪种工作流 | 用户输入时 | {pm} |

**常见混淆辨析**：
```
❌ 错误: "这个任务是 L2 级别，走快车道"
   → L2 是 PRD 分级，不是路由判定

❌ 错误: "这个需求复杂度高，走慢车道"
   → 应该说"触发慢车道条件，进入完整流水线"

✅ 正确: "{pm} 判断意图为 Branch_5（子 PRD），{coordinator} 判定走慢车道，PRD 拆解粒度为 L3（功能级）"
```

### 4.7 上下文雪崩防护 (Context Pruning)

> **问题**：大模型存在"迷失在中间"（Lost in the Middle）问题。无关信息过多会干扰模型注意力，导致准确率下降。

**Rerank 重排序机制**：
- 检索结果必须按**相关性分数降序排列**，只保留 Top-K 个片段
- 多个搜索结果合并时，必须去除重复内容，保留最相关的片段
- 代码片段优先级：**核心业务逻辑 > 配置文件 > 测试用例 > 文档注释**

**摘要压缩策略**：
- **触发条件**：`session_notes.md` 行数 > 200 行时，执行压缩
- **压缩规则**：
  1. 保留最近 3 天的完整记录
  2. 3 天前的记录压缩为单行：`[时间戳] 关键结论：xxx | 决策点：xxx | 待办：xxx`
  3. 删除超过 30 天的压缩记录
  4. 压缩后上限：≤ 300 行
- **压缩格式**：`[时间戳] 关键结论：xxx | 决策点：xxx | 待办：xxx`
- 禁止将完整历史对话无脑塞入上下文

**上下文构建原则**：
| 内容类型 | 最大占比 | 说明 |
|---------|---------|------|
| 系统规则 | 20% | `.ai/rules.md`、Agent 配置 |
| 当前任务文档 | 40% | PRD、LLD、API 契约 |
| 代码片段 | 30% | 仅限强关联文件 |
| 历史状态 | 10% | 压缩后的决策记录 |

### 4.8 活文档强制要求 (Living Documentation Mandate)

> **铁律**：交付给客户的不仅是代码和静态文档，而是一个**可审计、可追溯的知识资产**。

**三大强制产出**：
| 产出物 | 内容要求 | 存放位置 | 审批方式 |
|-------|---------|---------|---------|
| **推理路径记录 (Reasoning Trace)** | AI 如何得出每个关键结论的推理过程 | `{需求包}/reasoning/YYYYMMDD_reasoning_trace.md` | 🟡 人类抽检 |
| **原始数据索引 (Data Index)** | 列出所有引用的源文件、API 响应、数据库记录 | `docs/07_delivery/DATA_INDEX.md` | 🟡 人类抽检 |
| **版本说明 (Release Notes)** | 版本号、变更摘要、依赖版本、兼容性说明 | `docs/07_delivery/RELEASE_NOTES.md` | 🔴 **强制人类审批** |

**产出时机**：UAT Sign-off 通过后、`git tag` 前

**执行责任**：`{devops}` (DevOps) 负责生成上述三份文档，并确保 `RELEASE_NOTES.md` 纳入 UAT Sign-off 检查清单。

### 4.9 全局元数据与 DAG 驱动 (Metadata & DAG Driven)

本系统全面采用**机器可读的数据字典与 DAG 蓝图控制**，彻底取代过去完全依赖自然语言提示词的低效流转。

#### 4.9.1 YAML Metadata 强制要求
所有核心研发流转文档（如 `global-blueprint.md`, `PRD_*.md`, `LLD_*.md`, `step_plan.md` 及各项活文档）顶部**必须**包含标准的 YAML Frontmatter。
- 字段与枚举值必须严格遵循 `docs/00_meta/metadata-dictionary.md` 字典定义。
- Coordinator (`{coordinator}`) 将通过解析该区域的 `status`（如 Approved/Draft）和 `approved_by` 来作为硬性流转依据。

#### 4.9.2 基于 DAG 的依赖调度
- PM Agent 在 Phase 1 Step 2 输出的 `global-blueprint.md` 中，必须定义所有模块的 `depends_on` 依赖关系。
- 整个工作流被抽象为有向无环图（DAG）。
- Coordinator (`{coordinator}`) 负责读取拓扑关系，**当前策略为：按 DAG 拓扑排序进行严谨的串行唤醒与流转校验。**
- *（备注：此架构天然支持未来的并发并行执行扩展，各 Agent 互不干扰，完全依赖上游文档状态机作为输入源。）*

### 4.10 上下文硬隔离机制 (Context Hard Isolation)

> **背景**：借鉴 DeerFlow 架构，解决长会话导致的 Token 爆炸与上下文污染问题。

#### 4.10.1 硬隔离原则
- Coordinator 调用下游 Agent 时，**必须清空当前会话的 Message History**
- 只传递 `[Mount Context]` 指定的文档集作为输入
- 下游 Agent **必须读取文档中的 `key_decisions` 字段**，不得假设任何未落文档的上下文

#### 4.10.2 REASONING_TRACE 归档机制

**目录结构**：
```
docs//backend/prd/{层B}/
└── {层B}_{业务域X}/                        # 模块目录
    └── 20260321_Init/                    # 需求包
        ├── requirements/
        │   └── PRD_attendance.md
        ├── plan/
        │   ├── LLD_attendance.md
        │   └── step_plan.md
        └── reasoning/                    # 推理记录目录
            └── 20260323_reasoning_trace.md
```

**归档时机**：
| Phase | 触发动作 | 产出文件 |
|:---|:---|:---|
| Phase 2 | PRD 定稿 (Approved) | `reasoning/YYYYMMDD_reasoning_trace.md` |
| Phase 3 | LLD/Step_Plan 定稿 | 追加到同一文件（或新建） |
| Phase 6 | 发版完成 | 最终归档，状态设为 `Frozen` |

**YAML Frontmatter 示例**：
```yaml
---
doc_type: REASONING_TRACE
phase: Phase_2_Requirement
status: Frozen
module: attendance
created_at: {创建时间}
finalized_at: {完成时间}
---
```

#### 4.10.3 Coordinator 传递链
- 调用下游 Agent 前，Coordinator 必须传递 `reasoning_trace.md` 作为 Mount Context
- 确保下游 Agent 能获取上游的关键决策，实现上下文传递链

#### 4.11 Hotfix 简化流水线 (Emergency Fix Pipeline)

> **适用场景**：P0/P1 级别生产问题、安全漏洞、数据风险紧急修复

**触发条件**（满足任一）：
- 生产环境核心功能中断
- 安全漏洞（如 SQL 注入、XSS、敏感数据泄露）
- 数据丢失或损坏风险

**简化状态流转**：
```
正常流水线：Draft → Reviewing → Approved → WIP → In_Review → Testing → Ready_for_Release → Done
Hotfix流水线：Draft → Approved → WIP → Testing → Ready_for_Release → Done
                           ↑ 跳过 Reviewing 和 In_Review
```

**各 Agent 简化产出物**：
| Agent | 产出物 | 说明 |
|:---|:---|:---|
| {pm} | `PRD_hotfix.md` | 触发原因 + 影响模块 + 变更点 + 回滚方案 |
| {architect} | `LLD_delta.md` | 仅记录变更部分的架构决策 |
| {backend}/05 | 代码 + 注释内联 | 代码中标注 `// HOTFIX: #XXX` |
| {reviewer} | 快速审查 Checklist | 使用 `skills/HOTFIX_REVIEW_CHECKLIST.md`，跳过完整报告 |
| {qa} | `RELEASE_NOTES_hotfix.md` | 简版测试报告 + 发布说明 |
| {devops} | `skills/HOTFIX_RELEASE_CHECKLIST.md` | 发版检查清单（含回滚步骤） |

**PRD_hotfix 模板**：
```yaml
---
doc_type: PRD
status: Approved
hotfix: true
priority: P0|P1
module: [受影响模块]
created_at: YYYY-MM-DDTHH:MM:SS
---

## 🚨 热修变更说明
**触发原因**: [核心中断/安全漏洞/数据风险]
**影响模块**: [模块列表]
**影响范围**: [用户/系统/数据]

### 变更点
1. [变更描述]

### 回滚方案
- [回滚步骤]

### 验收标准
- [ ] 核心功能恢复
- [ ] 无副作用
```

#### 4.12 技术债管理 (Technical Debt Management)

**记录位置**：`docs/04_agent/memory/global/technical_debt.json`（全局活账本，跨 Phase 1~6）

**登记时机**：**每个 Gate 通过时**，本 Gate 产生的推迟/简化/妥协项必须登记入账。

**触发场景**：
- Gate 交付物遗漏（如 GLOSSARY 未产出）
- 功能推迟到下一版本（MVP 裁剪）
- 流程简化（如红蓝对抗合并执行）
- 硬编码推迟配置化（P0/P1/P2 硬编码项）
- 外部依赖未就绪（如外部数据 API 未采购）
- 骨架审批回退被用户拒绝
- 时间压力下妥协的临时方案

**状态流转**：
```
Open → In_Progress → Resolved
  ↓
Deferred（延期到下一版本）
```

**technical_debt.json 条目格式**：
```json
{
  "id": "DEBT-{NNN}",
  "title": "债务标题",
  "source": "功能推迟/流程简化/硬编码推迟/交付物遗漏/外部依赖",
  "source_phase": "Phase_X",
  "source_gate": "Gate_X",
  "description": "具体描述",
  "impact": "受影响的接口/功能",
  "risk": "高/中/低",
  "status": "Open|In_Progress|Resolved|Deferred",
  "target_version": "Gate_X / V1.5 / V2.0",
  "related_docs": [],
  "related_code": [],
  "resolved_at": null
}
```

**发版前检查**：
- {devops} 发版前检查 `technical_debt.json`
- 高风险（risk=高）技术债必须在发版报告中标注
- 过期未还的技术债需提醒用户

## **5\. 研发流程管控 (SOP)**

项目迭代执行严格遵循以下 8 个标准阶段，未经 PM 确认，不得跨阶段执行。

### **5.1 需求定义与边界确认 (Lean MVP \+ Docs-as-Code)**

1. 建立领域词汇表：优先在 `@internal/glossary.md` 中定义核心业务术语，确保全局沟通无歧义。  
2. 梳理业务诉求，确定核心用户故事 (User Story) 与系统角色权限划分。  
3. 提炼并输出需求说明书至 `@internal/PRD.md`，包含非功能性需求（NFR）与响应指标。  
4. **设立防蔓延锁 (Non-Goals)**：明确列出不在 MVP 核心路径上的功能，严禁 AI 越界开发。

### **5.2 架构设计与规范锁定 (UI/API Spec)**

1. 输出系统架构拓扑与时序图至 `@internal/HLD.md`。  
2. 制定数据库表结构与字段设计，输出至 `@internal/LLD.md`。  
3. 定义前后端通信 JSON 格式与状态码，输出至 `@internal/API_CONTRACT.md`。  
4. 检查 `.ai/rules.md`，确保已明确技术栈约束及全局规范。

### **5.3 任务拆解与看板管理 (Kanban \+ WIP Limit)**

1. 建立极简任务流：`Backlog (需求池)` \-\> `Doing (开发中)` \-\> `QA (测试)` \-\> `Done (已完成)`。  
2. 将需求拆解为包含具体**验收标准 (AC)** 的任务卡。  
3. **铁律 (WIP=1)**：**`Doing` 这一列永远只能有一张卡片！** 不将当前卡片彻底跑通并提交，绝对不允许开新坑。

### **5.4 编码执行与单元验证 (Harness Engineering & Agentic Workflows)**

1. **记忆恢复 (Memory Recovery)**：Agent 启动后，必须先读取 `docs/04_agent/memory/` 下的三层记忆结构（见 §6.5），恢复项目历史上下文。
2. **智能体角色激活 (Agent Activation)**：根据任务类型（需求、架构、编码），激活 `agents/` 中对应的 Agent 角色，确保 AI 以专业视角介入。
3. **计划具象化 (Plan as Artifact)**：要求 AI 在**需求包的 `plan/` 目录**下输出 `step_plan.md`，审查思路无破坏性后再批准动手。
4. **挂载上下文 (Context)**：精准引入当前任务相关的文档和组件，绝不让 AI 盲猜全局逻辑。
5. **多代理反思 (Agentic Reflection)**：核心代码生成后，Agent 通过其 `§0.5 Skill 加载路由` 加载对应 Skill（如 `skills/BACKEND_SELF_CHECK.md`、`skills/FRONTEND_SELF_CHECK.md`）进行逐条自检。
6. **强制自我验证 (Self-Correction)**：代码生成后，要求 AI 运行本地检查并自行阅读日志修复报错。
7. **记忆更新 (Memory Update)**：若过程中发现新的约定或踩坑，必须更新 `docs/04_agent/memory/` 对应文件。
8. **即时微小提交 (Micro-Commit)**：单张卡片验证通过，立刻在终端执行代码提交封存。

#### **5.4.1 并行开发安全守则 (Parallel Development Guardrails)**

本项目采用 **串行交接** 模式，确保质量可控。

* **禁止单会话多 Agent 并行**：在单个 CLI 会话中，严禁同时激活多个代码编写 Agent（`{backend}` / `{frontend}`）。Agent 不具备"上帝视角"，无法感知其他 Agent 的操作，会导致文件冲突和上下文污染。
* **允许并行的前提条件**：若确需前后端并行开发（如紧迫排期），必须满足以下全部条件：
  1. 接口契约（`API_CONTRACT.md`）已被 `{architect}` 锁定并提交至主干。
  2. 使用 Git Worktree 创建物理隔离的工作区（如 `../{PROJECT_NAME}-backend`、`../{PROJECT_NAME}-frontend`）。
  3. 每个 Worktree 拥有独立的 `step_plan.md` 副本。
  4. 开启多个终端窗口，每个窗口仅激活一个 Agent。
* **推荐策略**: MVP 阶段坚持串行交接（`Agent_03 → Agent_04 → Agent_05`），待流程稳定后再评估是否引入 Worktree 并行。

- **Mock 机制（伪并行开发）**： 为缓解 WIP=1 的串行阻塞，在 API 契约锁定后，前端可基于契约生成 Mock 数据先行开发。
  - **触发条件**： `API_CONTRACT.md` 已被 `{architect}` 锁定并提交至主干
  - **执行方式**: 使用 JSON Server / MSW (Mock Service Worker) 等工具生成 Mock API
  - **切换真实 API**: 后端实现完成后，修改 API Base URL 或 关闭 Mock 开关即可
  - **约束**: Mock 数据必须严格遵循 `API_CONTRACT.md` 中的数据结构

### **5.5 测试联调与验收**

1. 任务流转至 `QA` 阶段，进行手工黑盒测试，验证边界条件。  
2. **缺陷管理**：发现缺陷需携带完整错误复现路径及运行日志提交修复指令，修复后重新验证。
3. **缺陷分级与 SLA**（参见 `quality-gate.md` §1.4）：

| 级别 | 定义 | SLA |
|------|------|-----|
| P0 | 数据丢失 / 安全漏洞 / 跨租户泄漏 | 必须 **2h** 内修复 |
| P1 | 核心流程阻断 / 金额计算错误 | 必须 **24h** 内修复 |
| P2 | 功能降级 / 体验问题 | 下版本修复 |
| P3 | 优化建议 | 排期处理 |

### **5.6 自动化集成与部署 (DevOps 基建兜底)**

1. **版本发布**：发版时，DevOps 智能体打标 (Tag) 并 Push 至云端。
2. **高频云端同步**：每天结束工作后立刻推送主干分支 (`git push -u origin main`)，确保异地灾备。
3. 触发持续集成流水线，执行代码检查与测试构建。绿灯亮起的代码才允许部署至生产环境。

### **5.7 文档转化与版本发布**

1. 在版本控制系统中创建发布标签（如 `v1.0.0`）。  
2. 根据内部文档及代码实现，同步更新 `@delivery/USER_MANUAL.md` 等外部交付文档。  
3. 梳理并发布 `CHANGELOG.md` 更新日志。

### **5.8 迭代复盘与代码清理**

1. 版本发布后，针对代码库进行结构审查。  
2. 扫描冗余变量、未使用的组件库及历史遗留文件。将重构与优化项转化为标准任务卡片。

## **6\. AI 辅助开发管理要求**

### **6.1 文档结构化要求**

内部研发目录下的文档需采用标准化表单与固定层级格式，且强制要求 AI 在编码前校验 `glossary.md` 确保命名一致性。

### **6.2 上下文挂载限制**

限制单次引用的文件数量（建议不超过 4 个）。通常包含：全局规则、当前接口契约、待修改文件及强关联依赖文件。

### **6.3 数据库变更管控**

**禁止在日常业务开发环节要求 AI 直接修改数据库定义文件（Schema/DDL）**。凡涉及表结构变更，必须提交流程修改 `LLD.md`，经评估确认后再执行对应的数据库迁移操作。

#### **6.3.1 分层策略（借鉴 SAP / 金蝶 KDDM）**

| 层级 | 适用场景 | 管理方式 | 生效方式 |
|-----|---------|---------|---------|
| **核心业务表** | 产品团队设计的核心表（如订单、合同等） | Flyway/Prisma 版本化迁移 | 随版本发布，走 CI/CD |
| **租户扩展字段** | 租户自定义字段（如"VIP等级"、"跟进频率"） | 元数据驱动（JSONB/EAV） | 运行时生效，不重启 |

#### **6.3.2 迁移脚本规范**

| 项目 | 说明 |
|-----|------|
| **存放路径** | `src/backend/migrations/` 或 `prisma/migrations/` |
| **命名规范** | `{YYYYMMDDHHMMSS}_{description}.sql`（如 `20260321100000_add_contract_table.sql`） |
| **必含内容** | ① UP 脚本（正向变更）② DOWN 脚本（回滚）③ 变更说明注释 |
| **生成时机** | `{architect}` 设计 LLD 时同步生成迁移脚本 |

#### **6.3.3 租户扩展字段实现**

- 核心表预留 `ext_data` JSONB 字段（PostgreSQL）或 JSON 字段（MySQL）
- 或采用 EAV 模式（entity_attr_value 表）
- 由 {平台层} 层建模引擎管理元数据，提供配置界面

### **6.4 标准化排错流程**

采用结构化排错话术。必须包含：预期运行结果、实际异常表现、完整报错日志。明确要求 AI 先分析根本原因，输出解决方案经确认后再执行代码修正。

### **6.5 Agent 记忆持久化（三层结构）**

AI（如 Cursor/Claude）的上下文窗口有限，会话刷新后会遗忘历史上下文。`docs/04_agent/memory/` 目录采用**三层结构**持久化关键信息，确保 AI 在新会话中能够快速恢复项目上下文，避免"上下文爆炸"和"决策冲突"问题。

#### **6.5.1 三层目录结构**

```
docs/04_agent/memory/
├── global/                    # 全局层（长期，结构化）【豁免】
│   ├── decisions.json          # 原则性决策（工作方法论/产品哲学/核心概念定义，非具体方案）
│   ├── conventions.md         # 编码约定
│   ├── pitfalls.md            # 踩坑记录（按模块分类）
│   └── workflow_state.json     # 流程状态（Agent_02 维护）
│
├── modules/                   # 模块层（按领域）【豁免】
│   ├── UAC/
│   │   └── pitfalls.md
│   ├── Order/
│   └── Inventory/
│
└── current/                   # 当前迭代（临时）【计入限制】
    └── session_notes.md       # 本轮对话的结构化摘要
```

**加载策略**：
| 记忆文件 | 加载方式 | 文件限制 |
|---------|---------|---------|
| `current/session_notes.md` | **全文读取** | 计入 4 文件限制 |
| `global/` 目录 | **按需搜索** | **豁免**（不计入限制） |
| `modules/{模块}/` | **按需搜索** | **豁免**（不计入限制） |

#### **6.5.2 各层职责与生命周期**

| 层级 | 生命周期 | 用途 | Agent 行为 |
|------|---------|------|-----------|
| `global/` | 长期 | 结构化存储跨版本的关键决策、约定、踩坑 | 按主题结构化，新决策覆盖旧决策，底部保留变更历史 |
| `modules/` | 长期 | 模块级决策和踩坑，按领域隔离 | 按模块组织，发版时评估是否提升到 global |
| `current/` | 临时（单会话） | 本轮对话的结构化摘要 | 会话结束时压缩写入，避免对话历史膨胀 |

#### **6.5.3 global/ 文件说明**

| 文件 | 用途 | 示例内容 |
|------|------|---------|
| `decisions.json` | 原则性决策（仅限工作方法论/产品哲学/核心概念定义，三问门禁通过） | 为什么"AI 不暴露系统细节给租户" |
| `conventions.md` | 编码约定 | 时间格式统一使用 UTC，金额使用分为单位 |
| `pitfalls.md` | 踩坑记录（按模块分类） | pgvector 索引必须在数据导入后创建 |
| `workflow_state.json` | 流程状态追踪（Agent_02 维护），含 mermaid_text 字段 | 当前阶段、活跃 Agent、阻塞任务、流程历史 |

#### **6.5.4 记录格式规范**

**global/decisions.json 格式**（仅原则性决策，JSON 数组，参考 `_schemas/decisions_schema.json`）：

> **三问门禁**（写入前必须自问）：① 影响3+模块或推翻成本极高或方法论偏好？② 结论尚未写入任何PRD/ER/架构文档？③ 删掉后会导致重复争论？三条全通过才写入。具体业务方案归入对应 PRD/架构文档。

```json
[
  {
    "id": "D-087",
    "topic": "{原则标题}",
    "category": "methodology | product_philosophy | core_definition",
    "scope": "{适用范围/场景}",
    "decision": "{原则内容}",
    "reason": "{为什么这是原则而非具体方案}",
    "status": "confirmed"
  }
]
```

**global/pitfalls.md 格式**（按模块分类）：
```markdown
## 模块：{模块名称}

### [YYYY-MM-DD HH:mm] {踩坑标题}
**背景/规则**：具体内容
**原因**：为什么会有这个问题
**影响/适用范围**：带来的影响或适用场景
```

**current/session_notes.md 格式**（结构化摘要）：
```markdown
## [YYYY-MM-DD] 本轮对话摘要

**关键结论**:
- [时间戳] 决策点：xxx | 待办：xxx

**历史状态**（压缩）:
- [时间戳] 关键结论：xxx
```

#### **6.5.5 Agent 行为规范**

- **会话开始时**：先读取 `current/session_notes.md`，再按需搜索 `global/` 和 `modules/`
- **发现新约定/踩坑时**：更新 `global/` 或 `modules/{模块}/` 对应文件
- **原则性决策变更时**：在 `global/decisions.json` 中更新（须通过三问门禁，具体业务方案归入对应 PRD/架构文档）
- **会话结束时**：将本轮对话压缩写入 `current/session_notes.md`
- **发版时**：评估 `modules/` 中是否有值得提升到 `global/` 的记忆

### **6.6 AI 辅助开发话术模板库**

* **沙盒开发指令模板**：  
* “请阅读 `@DEV_STANDARDS.md` 的规范，在 `src/components/` 下新建  
* $$某组件$$  
* 。约束条件：绝对不允许修改全局 CSS，必须复用已有的  
* $$某基础组件$$  
* 。”  
* **自我纠错验证模板**：  
* “代码生成后，请运行本地语法检查与测试脚本。如果你发现有 UI 错位、TS 报错或终端警告，请自行读取日志并修复，直到无误后再向我报告最终结果。”

## **7\. 系统上线后变更管理流程**

### **7.1 变更定级与分流**

* **紧急缺陷 (Hotfix)**：导致核心业务中断或严重安全隐患，进入最高优先级热修复通道。  
* **需求变更 (Feature)**：新增功能或逻辑调整，按优先级纳入后续版本迭代计划。

### **7.2 文档先决更新 (Docs-First)**

在进行代码变更前，必须首先更新对应的规范文档（PRD/LLD/API契约等），并在“修订记录”中登记。

### **7.3 独立分支管理**

禁止在代码主干分支（如 `main`）进行直接修改。需创建独立的 `feature/` 或 `hotfix/` 分支。

### **7.4 受控编码与合并发版**

在独立工作区开发完毕并确保本地测试通过后，经由 PR 流程合并至主干。同步更新商业交付物并按规范升迁版本号。

## **8\. 系统运维与配套管理规范**

### **8.1 多环境运行规范**

建立本地开发环境（Local）、测试预发环境（Staging）与生产环境（Prod）的隔离机制。代码必须在测试环境验证后方准发布。

### **8.2 生产环境数据管控**

严禁开发人员直连线上数据库执行交互式修改。必须提交结构化的 SQL 脚本，经复核审查后由授权人员或自动化流程执行。

### **8.3 监控与告警机制**

建立持续的系统运行状况监控体系。设立合理的性能与错误阈值，触发异常时自动发出告警通知。

## **9\. 项目管理最佳实践**

### **9.1 需求变更控制与特性开关 (Feature Toggles)**

对系统上线后的零散需求保持审慎，必须走排期流程。对于影响面广的新功能，推荐引入特性开关机制实现灰度发布与毫秒级降级。

### **9.2 动态项目计划与风险管理 (工具优于文档)**

坚决避免使用静态 Markdown 维护项目进度和风险。应统一收口至 GitHub Projects 等动态看板工具中，与代码提交状态联动。

### **9.3 自动化门禁与审查清单 (Code Review)**

代码审查标准应直接转化为 `.github/pull_request_template.md` 模板，在发起合并请求时强制勾选确认，实现物理防呆设计。

### **9.4 本地提交前置检查机制 (Pre-commit Hooks)**

为确保代码质量与安全底线在开发源头得到贯彻，项目必须配置本地 Git 提交拦截机制（如引入 Husky、Lint-staged 以及 **Gitleaks/Trufflehog** 等工具链）。
在开发人员或 AI 智能体执行代码提交（`git commit`）动作时，系统需自动触发：
1. **安全防线扫描**：扫描并拦截任何疑似明文密码、云服务 AccessKey、JWT 密钥等硬编码泄露（防 AI 幻觉生成的假密钥被上传）。
2. **代码质量扫描**：静态代码分析（Linting）与代码格式化（Prettier）。凡存在未使用变量、语法错误或未通过自动化规则校验的代码，将从物理层面被拒绝提交入库，实现工程规范的强制落地。

## **10\. 商业级代码交付规范 (Enterprise-Grade Coding Standards)**

所有提交至代码主干的业务代码，必须满足以下六大商业级质量底线。违反任一原则的代码将在 Code Review 环节被强制驳回。

### **10.1 极端的健壮性与异常兜底 (Robustness & Stability)**

* **防御性编程**：严禁无条件信任外部输入、客户端传参及第三方接口响应。必须在系统边界进行严格的类型、格式与边界值校验。
* **API 强校验与脏数据物理拦截**：
  - 任何 Controller/网关层代码必须包含基于 DTO/Schema 的物理级脏数据拦截
  - 使用 Pydantic/Zod/Validation 注解进行类型、长度、正则与白名单校验
  - 一切校验失败的请求必须在 Controller 层直接返回 `HTTP 400 Bad Request`，绝不让畸形数据流入 Service 层和数据库
* **精准异常处理**：严禁使用全局或粗粒度的 `try-catch` 掩盖错误。必须捕获预期内的明确异常，并提供合理的降级逻辑（Fallback）或用户友好的错误码提示。

### **10.2 可维护性与命名自解释 (Readability & Maintainability)**

* **语义化命名**：变量与函数命名必须具备高度的自解释性（如 `calculateUserDiscount`），拒绝含糊不清的缩写。
* **克制且必要的注释**：代码结构应当做到”自注释”。常规代码不写”这是什么”，注释仅用于说明”为什么这么做”（如特殊的业务妥协、绕过特定 Bug 的机制）。

### **10.3 零容忍的安全底线 (Security)**

* **防注入与过滤**：所有涉及数据库查询的操作必须采用参数化查询或 ORM 安全机制，严防 SQL 注入。所有输出必须防范 XSS 攻击。
* **强鉴权与越权拦截**：所有涉及敏感数据读取或状态修改的接口，不仅需要验证用户的登录态（Token），必须进行严格的**水平/垂直越权校验**（校验该用户是否有权操作该资源 ID）。
* **异常行为阻断 (UBA 与防爆破)**：
  - 实施用户行为分析 (UBA)，对异常登录、异常操作模式进行实时监控与阻断
  - 敏感操作（如密码修改、权限变更）必须进行二次验证
  - 对暴力破解尝试实施 IP 封禁与账号锁定机制
* **生化隔离舱 (沙箱处理外部脏数据)**：
  - 处理网络爬虫、第三方 API、文件导入等外部数据时，必须先进行生化沙箱隔离
  - 所有外部 HTML/富文本必须经过 XSS 净化（DOMPurify 或等效库）
  - 外部导入数据应先存入临时隔离表，经校验后再合入主表
* **全局软删除原则**：
  - **绝对禁止物理删除**：全系统所有数据库表设计与数据操作，**绝对禁止使用 `DELETE FROM` 物理删除**
  - **必须使用软删除**：统一采用 `is_deleted` / `deleted_at` 软删除机制
  - 所有查询语句必须默认携带 `WHERE is_deleted = FALSE` 过滤条件
* **多租户数据隔离铁律 (Multi-Tenancy Isolation)**：
  - **强制 `tenant_id` 字段**：所有核心业务表必须包含 `tenant_id` 字段
  - **禁止业务层手动过滤**：绝对禁止在 Service/Controller 层手动拼接 `WHERE tenant_id = ?`
  - **持久层全局拦截**：必须在 ORM 拦截器或中间件层实现 `tenant_id` 的全局自动注入与过滤
  - **审查一票否决**：代码审查发现跨租户越权嫌疑时，无条件阻断流转

### **10.4 强制的可观测性 (Observability)**

* **规范日志记录**：关键业务节点（如订单流转、支付回调、认证授权）必须记录结构化日志，并携带全局唯一追踪标识（TraceID）串联请求链路。  
* **隐私数据脱敏**：系统日志中绝对禁止打印或记录用户的明文密码、完整手机号、身份证号及鉴权 Token。

### **10.5 测试驱动与可测试性 (Testability)**

* **单元测试覆盖**：系统的核心计算逻辑、复杂状态流转与金融交易相关模块，必须具备高覆盖率的自动化单元测试保障。
* **事件消费端幂等性测试**：所有事件消费端（Subscriber）**必须**编写重复消费场景下的幂等性验证用例，确保同一条消息被重复投递不导致业务状态异常。
* **依赖解耦**：代码架构应支持外部依赖（如数据库、第三方 API）的便捷 Mock，确保核心业务逻辑能在隔离环境下被充分测试。

### **10.6 性能防腐与无状态设计 (Performance & Scalability)**

* **规避性能陷阱**：严禁在循环（For/While）中发起数据库查询或外部网络请求，必须采用批量处理策略以规避 N+1 性能雪崩。  
* **应用层无状态**：应用服务节点应当保持无状态（Stateless），严禁在单机内存中持久化存储跨请求的业务上下文（如内存 Session），确保系统具备随时水平扩容（Scale-out）的能力。

## **11. Git 代码库与分支协作规范 (GitHub Flow)**

为保障核心业务代码的绝对安全与并行开发的互不干扰，本项目严格遵循业界标准的 GitHub Flow 分支协作流：

### **11.1 唯一主干原则 (Single Source of Truth Branch)**
* **废弃 master**：全面拥抱现代行业规范，以 `main` 作为代码库的唯一默认主干分支。
* **主干即生产**：`main` 分支上的代码必须永远处于“可随时部署至生产环境”的安全、稳定状态。

### **11.2 主分支物理保护机制 (Branch Protection Rules)**
必须在 GitHub 仓库设置中对 `main` 分支强制开启分支保护（Branch Protection），实施物理防呆拦截：
* **禁止直接推送 (Direct Push)**：任何开发人员严禁在本地 `commit` 后直接 `push` 到 `main` 分支。
* **强制代码审查 (Require PR)**：所有代码合入 `main` 必须通过新建合并请求（Pull Request）流转。
* **强制状态检查 (Status Checks)**：在 PR 合并前，必须等待 CI 自动化测试、Lint 静态检查全绿（Pass）。

### **11.3 隔离开发与标准协作流 (The Workflow SOP)**
一个需求/缺陷对应一个独立分支，严禁多任务混杂：
1. **拉取新分支**：基于最新的 `main` 分支，创建语义化命名的独立工作区（例如：新功能 `feature/ai-crawler` 或修复 `bugfix/auth-token-crash`）。
2. **独立环境试错**：在隔离分支中自由编码、高频微小提交（Micro-Commit），试错成本极低，且完全不影响主干稳定性。
3. **发起合并请求 (PR)**：开发与自测完成后，向 `main` 发起 PR，并关联对应的看板任务卡片。
4. **受控合并 (Merge)**：依据 `.github/pull_request_template.md` 逐项审查，确认代码逻辑、架构约束与安全规范无误后，方可执行合并。

### **11.4 强迫症级的环境清理 (Branch Cleanup)**
* **阅后即焚**：一旦 PR 被成功合并至 `main`，**必须立即删除**对应的 `feature/` 或 `bugfix/` 远程与本地分支。
* **保持整洁**：防止历史废弃分支堆积，彻底杜绝日后代码提交错位的风险，确保代码仓库绝对清爽。

