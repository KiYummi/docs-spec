# {产品名称} 项目 AI 编程助手全局规则

> **Version:** V 1.0
> **Last Updated:** YYYY-MM-DD
> **协作者:** {agent_1} ~ {agent_N}

## 0. 全局角色与 Skills

> 通用角色定义参见 `agents/`（8 个角色），通用 Skills 检查清单参见 `agents/skills/`（12 个）。
> 本文件仅包含 {产品名称} 项目特有规则。Coordinator 角色负责团队建队和任务调度，参见 `agents/02_coordinator.md`。

---

## 0.1 残差保真规则（文档工程体系）

### 跳跃连接
- 所有下游文档（LLD/API 合约/数据模型）必须包含"需求溯源区"
- 溯源区直接锚定上游原文（PRD/Sub-PRD），实现跳跃连接
- 溯源区内容由人工或工具填充，LLM 不得修改

### 全链路索引
- 每个需求有唯一 ID（@req-id: R001）
- 所有制品必须标注承接的需求 ID
- 索引文件（index.json）是全局唯一事实源

### 补丁式修正
- 修改文档必须以结构化补丁形式提交
- 禁止直接重写文档正文
- 补丁必须包含：reason、source_requirement、impact

### 人在回路
- 溯源区内容：人确认
- 补丁签发：人审批
- 规则演化：人决策

### 主动确认规则（Active Learning）
- LLM 遇到不确定需求时，必须主动向人提问，不得假设
- 问题格式：`[待确认] {问题描述} → 选项 A / 选项 B / 选项 C`
- 人确认后才可继续执行

---

## 0.2 MOE 动态调度规则

### 门控机制
- Coordinator 是门控网络，根据任务类型动态选择执行 Agent
- PRD 类型 → 调用 pm
- 架构类型 → 调用 architect
- 技术文档类型 → 调用 docs
- 代码类型 → 调用 backend/frontend
- 审查 → 调用 reviewer
- 审计 → 调用 residual-auditor

### 稀疏激活
- 每次只激活相关的 Agent，不是全部
- 不相关的 Agent 不参与当前任务

---

## 0.3 日志系统规则

### 三层日志结构
```
docs/04_agent/logs/
├── README.md          # 日志系统说明
├── decisions/         # 决策日志
├── audits/            # 审计日志
└── changes/           # 变更日志
```

### 日志记录规则
| 日志类型 | 触发时机 | 记录者 | 记录内容 |
|---------|---------|--------|---------|
| 决策日志 | 每次人做决策时 | coordinator | 背景 → 选项 → 决策 → 理由 → 影响 |
| 审计日志 | 每次审计完成后 | residual-auditor | 范围 → 推理链 → 发现 → 补丁 → 反思 |
| 变更日志 | 每次规则变更时 | coordinator | 变更内容 → 变更前 → 变更后 → 预期效果 |

### 迭代飞轮
```
执行 → 记录日志 → 分析模式 → 改进规则 → 执行
```

---

## 1. 环境变量与路径锚点

本项目采用"代码库与文档库一体化"架构，文档库作为 `docs/` 子目录存在于项目根目录下。

**环境变量**（`.env` 文件）：
```
PROJECT_NAME={PROJECT_NAME}           # 项目名称
PROJECT_PATH={PROJECT_PATH}           # 项目根目录
DOCS_REPO_PATH=./docs                 # 文档库路径（相对路径）
```

> **注意**：`DOCS_REPO_PATH` 使用相对路径 `./docs`，指向项目根目录下的 docs/ 子目录。

---

## 2. Agent 记忆持久化（三层 + 归档层）

**⚠️ 重要**：AI 会话刷新后会遗忘历史上下文。每次开始工作前，**必须先读取**三层记忆结构恢复记忆：

> **位置**: `docs/04_agent/memory/`（即 `./docs/04_agent/memory/`）
>
> **说明**: Agent 记忆持久化存储在项目文档库中，与 PRD/LLD 等业务资产同源，便于版本联动。

```
docs/04_agent/memory/
├── global/                    # 全局层（长期，结构化）【豁免】
│   ├── decisions.json          # 原则性决策（工作方法论/产品哲学/核心概念定义），具体方案归入对应文档
│   ├── conventions.md         # 编码约定
│   ├── pitfalls.md            # 踩坑记录（按模块分类）
│   └── workflow_state.json    # 流程状态（Agent_02 维护，含 mermaid_text 字段）
│
├── modules/                   # 模块层（按领域）【豁免】
│   ├── {模块1}/
│   │   └── pitfalls.md
│   ├── {模块2}/
│   └── {模块3}/
│
├── current/                   # 当前迭代（临时）【计入限制】
│   └── session_notes.md       # 本轮对话的结构化摘要
│
└── per_release/               # 📦 归档层（Phase 6 发版后）
    └── vX.Y.Z/
        ├── summary.md           # 版本记忆快照
        └── {需求包}/reasoning/  # Reasoning Trace 归档（{devops} 维护）
```

**加载策略**：
| 记忆文件 | 加载方式 | 文件限制 |
|---------|---------|---------|
| `current/session_notes.md` | **全文读取** | 计入 4 文件限制 |
| `global/` 目录 | **按需搜索** | **豁免**（不计入限制） |
| `modules/{模块}/` | **按需搜索** | **豁免**（不计入限制） |
| `per_release/` | **不主动加载** | 仅版本回滚时使用 |

**恢复顺序**：
1. **全文读取** `current/session_notes.md`（如存在）恢复本轮对话上下文
2. **按需搜索** `global/` 和 `modules/` 中与当前任务相关的记忆片段
3. 若无相关记忆，跳过搜索步骤

**发现新约定或踩坑时**：更新 `global/` 或 `modules/{模块}/` 对应文件。
**会话结束时**：将关键结论压缩写入 `current/session_notes.md`。
**发版时**：评估 `modules/` 中是否有记忆值得提升到 `global/`，并归档到 `per_release/vX.Y.Z/summary.md`。

#### 2.0.1 session_notes.md 强制结构

`session_notes.md` **必须**包含以下章节（新会话启动检查点依赖这些章节）：

```markdown
# 会话记录 (Session Notes)
> **最后更新**：YYYY-MM-DD
> **当前角色**：agent_XX (角色名) — 上下文压缩后可切换角色

## 当前任务：{Gate 名 / 任务名}
### 任务来源：{Handoff 协议原文}
### 交接流程状态：{流程图，标注当前位于哪一步}

### 已完成的内容
- ✅/⚠️/🔄/⬜ {具体到文件路径、行数、端点数}

### 下一步动作（压缩后恢复用）
1. **{具体动作}**：{精确描述，包含文件路径和修改内容}

### 已确认的决策（本次会话相关）
- {编号}: {决策内容}

### 核心参考文档路径
| 文档 | 路径 |
```

**铁律**：每次更新 `session_notes.md` 时，**"下一步动作"章节必须精确到可执行级别**，确保新会话无需额外搜索即可直接执行。

#### 2.0.2 session_notes.md 压缩机制

**触发条件**：会话结束写入 `session_notes.md` 前，检查行数：
- ≤ 200 行：直接写入
- > 200 行：先压缩旧内容，再写入新内容

**压缩方式**：
1. 保留最近 3 天的完整记录
2. 3 天前的记录压缩为单行：`[时间戳] 关键结论：xxx | 决策点：xxx | 待办：xxx`
3. 删除超过 30 天的压缩记录

**压缩后上限**：≤ 300 行

---

## 3. 核心受控文档（SSOT 单一数据源）

> **强制元数据铁律**：所有业务输出文档的顶部**必须**保留并维护符合规范的 YAML Metadata（Frontmatter），严禁在修改时删除或篡改该区域格式！

以下文档为业务逻辑与架构规范的唯一准则，AI 必须在编码前阅读对应文档：

| 文档 | 路径 | 用途 |
|------|------|------|
| metadata-dictionary.md | `docs/00_meta/` | 全局元数据与状态机字典（强制遵循） |
| global-blueprint.md | `docs/00_meta/` | 全局架构蓝图与执行顺序规划 |
| master-prd.md | `docs/00_meta/` | 核心产品白皮书与 MVP 边界 |
| glossary.md | `docs/00_meta/` | 业务术语字典（命名必须遵循此表） |
| GLOBAL_HLD.md | `docs/02_backend/specs/` | 系统总体架构设计 |
| API_CONTRACT.md | `docs/03_api/` | 全局 API 契约与状态码 |
| DEV_STANDARDS.md | `docs/02_backend/specs/` | 开发规范与编码底线 |
| `frontend/` 目录 | `docs/01_frontend/` | 前端设计体系 SSOT（Token / 组件 / 布局 / 交互 / 主题 / 无障碍 / 工程化）。替代原单文件 |
| **State Machine Dictionary** | `docs/02_backend/data-model/state-machines/` | **业务状态机 SSOT**（值 + 转换 + 触发 + 副作用 + 逆向路径），禁止分散在 Enum 和 PRD |
| **Permission Registry** | `docs/03_api/permission-registry.json` | **权限码 SSOT**（permission_code + rate_limit_level + risk_level 全局注册） |
| **NFR Registry** | `docs/02_backend/specs/NFR_REGISTRY.md` | **非功能需求目标 SSOT**（性能/并发/缓存/DB约束数值），各 Sub PRD 链接引用 |
| **Security Baseline** | `docs/02_backend/specs/SECURITY_BASELINE.md` | **安全基线 SSOT**（P1-P16 修补基线），各 Sub PRD 链接引用，禁止重复抄写 |
| **dev-spec.md** | `docs/00_meta/` | **项目开发管理规范总纲**（流水线、铁三角、路由、回退、Agent 行为等完整定义） |
| **quality-gate.md** | `docs/04_agent/` | **质量门禁定义**（三级审查 L1/L2/L3、批次结构、测试门禁、Schema Freeze、缺陷 SLA、评估维度矩阵） |

---

## 4. AI 智能体协作流水线

本项目遵循 `agents/` 下定义的多智能体协作规范，检查清单已抽出为独立 Skill 文件（`agents/skills/`），Agent 通过各自 `§0.5 Skill 加载路由` 在特定 SOP 步骤触发时加载：

| Agent | 角色 | 职责 | Skill 文件 |
|-------|------|------|-----------|
| {pm} | PM | 需求定义、领域建模、PRD 撰写 | `PRD_QUALITY_CHECKLIST` |
| {coordinator} | Coordinator | 路由判断、阶段审查、UAT Sign-off | `GATE_AUDIT_CHECKLIST`, `UAT_SIGNOFF_CHECKLIST` |
| {architect} | System Architect | 架构设计、LLD、任务拆解 | `LLD_QUALITY_CHECKLIST` |
| {backend} | Backend Developer | 后端编码、单元测试 | `BACKEND_SELF_CHECK`, `CODE_REVIEW_CHECKLIST` |
| {frontend} | Frontend Developer | 前端开发、UI 组件化 | `FRONTEND_SELF_CHECK` |
| {reviewer} | Code Reviewer | 代码审查、安全审计 | `CODE_REVIEW_CHECKLIST`, `BATCH_CHECKLIST`, `SECURITY_AUDIT`, `HOTFIX_REVIEW_CHECKLIST` |
| {qa} | QA Engineer | 测试验证、缺陷管理 | `TEST_QUALITY_CHECKLIST`, `GATE9_TEST_CHECKLIST` |
| {devops} | DevOps Engineer | 发布部署、文档管理 | `RELEASE_CHECKLIST`, `HOTFIX_RELEASE_CHECKLIST` |
| **residual-auditor** | **残差审计员** | **残差保真度审计** | `RESIDUAL_AUDIT_CHECKLIST` |

详细流水线规范见：`docs/00_meta/dev-spec.md`
详细质量门禁定义见：`docs/04_agent/quality-gate.md`（三级审查体系）

### 4.1 三级审查体系（L1/L2/L3）

Phase 4 编码阶段采用三级审查，Phase 5 采用 L3 全量集成审查：

| 级别 | 时机 | 范围 | 执行 Agent |
|------|------|------|-----------|
| **L1 批次审查** | 每个编码批次完成后 | 仅本批次代码 | `{reviewer}` 独立执行 |
| **L2 层级累积审查** | 每个大层级完成后 | 本层 + 所有已完成层 | `{reviewer}` + `{coordinator}` 联合 |
| **L3 全量集成审查** | Phase 5 | 全系统 | `{reviewer}` + `{qa}` 联合 |

每个 L1 批次统一执行 6 步：编码 → 即时审查 → 单测 → API 契约检查 → 变更影响分析 → 修复回归。详见 `quality-gate.md` §五。

> **Hotfix 简化流程**：P0/P1 生产问题跳过 `Reviewing` 和 `In_Review` 阶段，各 Agent 产出简化版文档（见 dev_spec §4.11）

> **技术债管理**：全局活账本 `docs/04_agent/memory/global/technical_debt.json`，每个 Gate 通过时必须登记本 Gate 产生的推迟/简化/妥协项。状态流转 `Open → In_Progress → Resolved / Deferred`（见 dev_spec §4.12）

---

## 5. 编码铁律（Global Constraints）

### 5.1 命名规范
- 所有变量、函数、组件命名必须遵循 `docs/00_meta/glossary.md` 中的术语定义
- 禁止使用 GLOSSARY 未收录的缩写或自创术语

### 5.2 前端专属约束
- **设计系统优先**：编码前必须检查 `docs/01_frontend/` 中的 Token、组件和交互模式
- **禁止硬编码颜色**：必须使用设计 Token（CSS 变量）
- **禁止散装 HTML**：必须使用组件库或已有公共组件
- **禁止内联样式**：样式必须通过 CSS/SCSS/Tailwind 类名管理

### 5.3 后端专属约束
- **禁止绕过 API 契约**：接口路径、请求体、响应体必须符合 `API_CONTRACT.md`
- **禁止直连线上数据库**：开发环境必须使用本地或测试数据库
- **禁止跳过权限校验**：所有敏感接口必须包含水平/垂直越权检查
- **跨域联动禁止同步调用**：跨业务域的联动逻辑，**绝对禁止**使用同步 API 直接调用，必须采用 Pub/Sub 事件模型
- **事件消费端强制幂等**：所有事件消费端（Subscriber）的函数入口**必须实现幂等性（Idempotency）**，确保同一条消息重复消费不导致业务状态异常
- **消费端 TDD 先行**：编写事件消费端业务代码前，**必须先编写单元测试**，验证重复消费场景下的状态一致性
- **元数据驱动原则**：业务对象解析引擎必须基于声明式元数据（如 JSON Schema）驱动，**绝对禁止**在解析器中硬编码任何具体业务字段。解析器必须是纯粹的"元数据翻译器"，与业务语义 100% 解耦

### 5.4 安全底线
- 所有 SQL 查询必须使用参数化查询或 ORM（防注入）
- 所有用户输入必须进行类型与边界校验
- 日志禁止打印明文密码、Token、身份证号、手机号
- **动态公式引擎沙箱隔离**：动态公式或规则计算引擎**绝对禁止**使用 `eval()` 或直接执行原生脚本语言，必须使用安全的表达式解析引擎并在沙箱内执行，杜绝 RCE（远程代码执行）漏洞风险
- **缺陷修复 SLA**：P0 必须 2h 内修复、P1 必须 24h 内修复（参见 `quality-gate.md` §1.4）

### 5.5 全局安全与数据治理铁律

> **零信任数据铁律**：以下规则为系统级强制约束，任何 Agent 不得违反。

#### 5.5.1 软删除强制原则 (Soft Delete Mandate)
- **绝对禁止物理删除**：全系统所有数据库表设计与数据操作，**绝对禁止使用 `DELETE FROM` 物理删除**
- **必须使用软删除**：所有删除操作必须统一采用 `is_deleted` / `deleted_at` 软删除机制
- **查询过滤**：所有查询语句必须默认携带 `WHERE is_deleted = FALSE` 或 `WHERE deleted_at IS NULL`
- **唯一约束处理**：涉及唯一约束的软删除记录，需配合 `deleted_at` 时间戳或使用复合唯一索引

#### 5.5.2 外部数据生化隔离 (Biochemical Sandbox)
- **绝对零信任外部数据**：处理网络爬虫、第三方 API、文件导入等外部传入数据时，必须先进行生化沙箱隔离与净化
- **XSS 净化**：所有外部 HTML/富文本必须经过 DOMPurify 或等效库净化
- **SQL 注入隔离**：外部数据必须经过参数化处理，禁止直接拼接
- **恶意脚本检测**：对上传文件进行病毒扫描和 MIME 类型校验
- **隔离存储**：外部导入数据应先存入临时隔离表，经人工或规则校验后再合入主表

#### 5.5.3 入口强校验 (API Gateway Validation)
- **DTO/Schema 物理拦截**：任何 Controller/网关层代码必须包含基于强类型 DTO/Schema 的物理级脏数据拦截
- **白名单校验**：仅接受预定义字段，拒绝一切非预期字段（防止批量赋值攻击）
- **类型强校验**：使用 Pydantic/Zod/Validation 注解进行类型、长度、正则与范围校验
- **HTTP 400 物理拦截**：一切校验失败的请求必须在 Controller 层直接返回 `400 Bad Request`，绝不让畸形数据流入 Service 层和数据库

#### 5.5.4 多租户数据隔离铁律 (Multi-Tenancy Isolation)
- **强制 `tenant_id` 字段**：所有核心业务表**必须包含 `tenant_id` 字段**（{architect} 数据库设计时强制执行）
- **禁止业务层手动过滤**：**绝对禁止**在 Service/Controller 层手动拼接 `WHERE tenant_id = ?`
- **持久层全局拦截**：必须在 ORM 拦截器或中间件层实现 `tenant_id` 的**全局自动注入与过滤**
- **审查一票否决**：{reviewer} 代码审查发现跨租户越权嫌疑时，**无条件阻断流转**

---

## 6. 微共识铁律 (Micro-Consensus Protocol)

> **零信任铁律**：无论当前扮演哪个 Agent 角色，在进行系统架构设计、核心 PRD 撰写或复杂业务逻辑编码前，以下规则绝对适用。

### 6.1 禁止长篇输出
- **绝对禁止**一次性输出长篇大论或全量代码
- **必须采用**"输出大纲 (Outline) → 等待人类确认 → 局部生成"的循环模式
- **最大输出限制**：单次输出不超过 200 行代码或 1000 字文档

### 6.2 方案权衡必问 (Trade-off Questions)
在进行关键决策前，必须先抛出极端场景权衡问题：
- "如果 [极端场景]，系统应该如何处理？方案 A (xxx) vs 方案 B (yyy)，你倾向于哪个？"
- 等待人类回复 `Approve` 后，方可进行实质性生成

### 6.3 高危操作反向提问
当系统提示存在以下高危操作时，**必须**强制触发反向提问，要求人类给出明确的业务决策：
- **并发控制**：乐观锁 vs 悲观锁 vs 分布式锁？
- **权限分配**：谁可以访问/修改这个资源？
- **多租户数据过滤**：如何确保租户 A 看不到租户 B 的数据？
- **财务计算**：金额精度如何处理？折扣上限是多少？
- **状态机流转**：是否允许逆向流转？重复提交如何处理？

### 6.4 两段式审批回退机制 (Rollback Protocol)
> **铁律**：`step_plan.md` 采用两段式审批（骨架 → 血肉），血肉阶段发现骨架问题时必须执行回退。

**回退触发条件**：
- 血肉填充时发现需要新增/删除 Task
- AC 无法覆盖的边界场景需要调整骨架
- 用户主动提出需求变更影响骨架

**回退流程**：
```
发现骨架需要调整
    ↓
在 step_plan.md 记录 🔄 回退申请（含数据库影响标注）
    ↓
使用 @{coordinator} [Handoff: Branch_5] 请求回退评估（含数据库回滚检查）
    ↓
等待 [用户 Confirm]
    ↓
🆕 若涉及数据库变更 → 先执行 DOWN 脚本回滚数据库
    ↓
确认后：回退到骨架版本，重新走两段式审批
```

> ⚠️ **数据库回滚铁律**：若回退涉及数据库变更，**必须先执行 DOWN 脚本回滚物理环境**，避免"幽灵表"导致开发环境与文档状态不一致。

**变更类型判定**：
- **小范围变更**（仅影响 AC）：直接修改 AC，重新血肉审计
- **大范围变更**（影响骨架）：触发 Skeleton-Rollback，重走完整审批

### 6.5 Schema Freeze 铁律

> **触发时机**：Gate 7d（数据库迁移脚本验证通过）完成后。

进入表结构冻结期，任何后续 DDL 变更必须走 4 步审批流：
1. 在 `step_plan.md` 记录变更申请（含影响范围、回滚方案）
2. `{coordinator}` 评估影响
3. 等待 [用户 Confirm]
4. 新增迁移脚本（UP + DOWN）

详见 `quality-gate.md` §Gate 7d。

---

## 7. Git 协作规范（GitHub Flow）

- **唯一主干**：`main` 分支为生产就绪分支，禁止直接提交
- **分支命名**：`feature/xxx`、`bugfix/xxx`、`hotfix/xxx`
- **PR 必检**：合并前必须完成 `.github/pull_request_template.md` 检查清单
- **阅后即焚**：PR 合并后立即删除远程与本地分支

---

## 8. Token 预算约束与上下文雪崩防护

### 8.1 基础 Token 预算约束
- 单次任务上下文不超过 **4 个文件**
- 搜索结果不超过 **500 行代码片段**
- 超过 1000 行的文件必须先搜索定位，再分段读取

### 8.2 上下文雪崩防护 (Context Pruning)

> **问题**：大模型存在"迷失在中间"（Lost in the Middle）问题。无关信息过多会干扰模型注意力，导致准确率下降。

### 8.3 上下文压缩前保全协议（强制）

> **铁律**：当检测到以下信号时，**必须先执行保全再继续任何业务操作**：
> - 用户提示"上下文压缩"或"压缩"
> - 工具返回 token limit 警告
> - 会话轮次超过 30 轮
> - 主动判断上下文即将压缩

**保全三步**：

```
Step 1: 写入 session_notes.md
  - 更新"下一步动作"章节（精确到可执行级别）
  - 更新"交接流程状态"（标注当前精确位置）
  - 更新"已完成的内容"（含文件路径、行数、问题编号）

Step 2: 同步 workflow_state.json（parse → 修改字段 → serialize + 更新 mermaid_text）
  - 更新当前 Gate 进度
  - 更新活跃 Agent 状态
  - 追加流程历史

Step 3: 同步 decisions.json（parse → push 新条目 → serialize）（如有新的原则性决策，须通过三问门禁）
```

**保全完成后输出**：`[Context Checkpoint Saved] session_notes.md + workflow_state.json + decisions.json（如有原则性决策变更）已更新`

### 8.4 角色切换协议

> **适用场景**：用户指示切换 Agent 角色（如 "{coordinator} 审查" → "{architect} 继续"）

**切换前（当前角色）**：
1. 执行保全三步（§8.3）
2. 在 `session_notes.md` 写入：切换原因、切换前状态、切换后首个动作
3. 输出 `[Role Handoff: agent_XX → agent_YY] state saved`

**切换后（新角色）**：
1. 全文读取 `session_notes.md`
2. 读取 `workflow_state.json`
3. 读取对应 Agent 定义文件（含 `§0.5 Skill 加载路由`）
4. 按"下一步动作"章节执行（Skill 在具体 SOP 步骤触发时加载，不在 §0 预读）

**责任划分**：
| 操作 | 执行者 | Agent 职责 |
|------|--------|-----------|
| Rerank 重排序 | 检索工具（自动执行） | 无需操作，检索结果已按相关性排序 |
| 摘要压缩 | Agent（LLM） | session_notes.md > 200 行时压缩（保留最近 3 天，压缩后 ≤ 300 行） |
| 上下文配额 | 检索工具 | 遵循检索结果，不超限读取文件 |

**Agent 只需遵循**：
- 检索结果已按相关性排序，无需自行 Rerank
- 不主动读取超过配额的文件
- session_notes.md 行数 > 200 行时，执行压缩（保留最近 3 天，压缩后 ≤ 300 行）

**摘要压缩格式**：
- 压缩格式：`[时间戳] 关键结论：xxx | 决策点：xxx | 待办：xxx`
- 禁止将完整历史对话无脑塞入上下文

**上下文构建原则**：
| 内容类型 | 最大占比 | 说明 |
|---------|---------|------|
| 系统规则 | 20% | `.ai/rules.md`、Agent 配置 |
| 当前任务文档 | 40% | PRD、LLD、API 契约 |
| 代码片段 | 30% | 仅限强关联文件 |
| 历史状态 | 10% | 压缩后的决策记录 |

---

## 9. 自检清单（Pre-Commit）

> **注意**：本节是通用的最小化 Pre-Commit 检查。各 Agent 的完整自检清单已抽出为独立 Skill 文件（`skills/BACKEND_SELF_CHECK.md`、`skills/FRONTEND_SELF_CHECK.md` 等），由 Agent 在其 `§0.5 Skill 加载路由` 中按 SOP 步骤触发时加载。

在执行 `git commit` 前，必须确保：

- [ ] 代码通过 `npm run lint` / `cargo check` / `go vet` 检查
- [ ] 禁止使用 `--no-verify` 跳过 pre-commit hook
- [ ] 如被 hook 拦截，必须读取日志修复后重试

---

## 10. Prompt 调优警示 (Prompt Engineering Warning)

> **核心认知**：Prompt Engineering 的边际效用递减。过度调优 Prompt 是**反模式**。

### 10.1 边际效用递减定律

| Prompt 长度 | 边际效用 | 建议动作 |
|------------|---------|---------|
| < 500 字 | 高 | 继续优化 |
| 500-1500 字 | 中 | 适度精简 |
| 1500-2000 字 | 低 | 考虑拆分或换方案 |
| **> 2000 字** | **负** | **立即停止，问题不在 Prompt** |

### 10.2 超过 2000 字 Prompt 的根因排查清单

**如果 Prompt 超过 2000 字仍无法解决问题，请检查**：

1. **数据质量**（最常见）
   - RAG 检索到的内容是否相关？
   - 输入数据是否存在噪声或错误？
   - 是否缺少必要的上下文信息？

2. **流程拆解**
   - 任务是否过于复杂，需要拆分为多个子步骤？
   - 是否应该交给多个 Agent 协作完成？
   - 是否需要引入中间检查点？

3. **模型能力**
   - 当前模型是否胜任该任务？
   - 是否需要升级到更强的模型？
   - 是否需要引入外部工具（如代码执行、搜索）？

### 10.3 Prompt 优化优先级

```
1. 数据质量 (权重 50%)  ← 最重要！
2. 流程拆解 (权重 30%)
3. Prompt 措辞 (权重 15%)
4. 模型选择 (权重 5%)
```

**警示**：在数据质量和流程拆解优化之前，不要花时间微调 Prompt 措辞。

---

## 11. Prompt 设计规范

### 11.1 声明-执行闭环铁律

> **原则**：每条产出规范必须在某条具体步骤中被显式调用

- **声明**：在"标准产出"/"交付契约"中定义的文件
- **执行**：必须在某个 Agent 的具体 Step 中明确写出"产出 XXX"

**检查项**：
- [ ] 规范中要求的每个产出物，是否在某个步骤中显式提及？
- [ ] 步骤中的"产出 XXX"是否与规范定义一致？
- [ ] 菜单选项是否覆盖所有可用分支？

**反例**：
- 规范要求产出 `reasoning_trace.md`，但步骤中只有"写入 PRD"
- 菜单显示 7 个选项，但实际有 8 个分支

**修复模式**：
1. 发现声明与执行不一致
2. 在执行步骤中补全显式调用
3. 或在声明中删除无法执行的承诺

### 11.2 复杂脚本外置原则

> **原则**：超过 20 行的 Bash/Python 脚本不应内嵌于 Prompt 中

**原因**：
- LLM 执行内联脚本时易因引号转义、环境变量等问题失败
- 外置脚本可独立测试、版本控制、复用

**最佳实践**：
```bash
# 好的做法：调用外置脚本（新项目初始化）
# 注意：实际使用时需先设置 GLOBAL_TEMPLATES_PATH 环境变量
bash ${GLOBAL_TEMPLATES_PATH}/scripts/init_project.sh <PROJECT_NAME>

# 避免：在 Prompt 中内嵌长段脚本
```

**检查项**：
- [ ] 脚本是否超过 20 行？ → 外置
- [ ] 脚本是否包含复杂逻辑（循环、条件、变量替换）？ → 外置
- [ ] 脚本是否需要跨多个 Agent 复用？ → 外置
