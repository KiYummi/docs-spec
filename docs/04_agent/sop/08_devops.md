# Devops — {产品名称} 项目 SOP

> 通用角色定义：`agents/08_devops.md`
> 本文件仅包含 {产品名称} 项目特有流程

## §0.5 Skill 加载路由

本 Agent 在不同流程步骤中需加载对应的 Skill 文件。**不在 §0 预读**，按 SOP 步骤触发时加载。

| SOP 步骤 | 触发条件 | 加载 Skill | 说明 |
|---------|---------|-----------|------|
| §5 Step 9 发版前 | 永远 | `skills/RELEASE_CHECKLIST.md` | 发版前置检查 |
| §3.2 Hotfix 发版 | hotfix=true | `skills/HOTFIX_RELEASE_CHECKLIST.md` | Hotfix 简化检查 |

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
3. 确认任务类型（发版执行 / 热修发版 / 回滚执行 / CI/CD 配置）
4. 覆盖写入 `docs/04_agent/memory/current/task_context.md`（使用模板 `docs/templates/TASK_CONTEXT_Template.md`）
5. 📋 CHECKPOINT（任务归属确认）→ 执行 §2.0 职责判定规则

### §2.2 Phase B: 知识获取

#### 任务类型：发版执行（Branch_3）

**必读项**：

| # | 知识项 | 来源 | 读取范围 | 预估行数 |
|---|--------|------|---------|---------|
| K1 | 发版指令 | step_plan.md | 版本信息 + 依赖 | ~20 |
| K2 | 变更历史 | Git Log / PR 记录 | 自上一 Tag 以来的全部 | ~50 |
| K3 | API 契约 | api/contracts/ | 新增/变更接口概要 | ~60 |
| K4 | 测试报告 | {qa} 产出 | 结论 + 性能基线 | ~30 |
| K5 | 质量门禁 | quality-gate.md §Gate 10 | 全文 | ~40 |

**按需项**：

| # | 知识项 | 来源 | 读取范围 | 触发条件 |
|---|--------|------|---------|---------|
| K6 | 迁移脚本 | plan/migrations/*.sql | 全文 | 涉及 DDL 变更 |
| K7 | 灰度配置 | Feature Flag 配置 | 白名单 | 灰度发布 |

### §2.3 Phase C: 规则执行

**准入条件**：Phase B 必读项全部已读。

1. 按任务类型执行对应流程（§3 特殊流程 / §5 SOP）
2. **发版前** → **读取 `skills/RELEASE_CHECKLIST.md`**，逐条检查并标记 ✅/⚠️/❌
3. **Hotfix 发版** → **读取 `skills/HOTFIX_RELEASE_CHECKLIST.md`**
4. 遇到不确定的条目 → 按参考表格查阅知识层
5. 输出执行结果

### §2.4 Phase D: 完成与流转

1. 将发版结论写入 session_notes.md
2. 更新文档 YAML 状态为 `Done`
3. 清除/标记 `docs/04_agent/memory/current/task_context.md`
4. 执行记忆归档
5. → 回到 §2.1 Phase A

---

## §3 特殊流程

### §3.1 灰度发布策略（MVP 轻量版）

> **详细定义**：参见 `quality-gate.md` §Gate 10。

**MVP 灰度策略**：租户白名单开关

1. 初始仅对白名单租户开放新功能
2. 确认无 P0/P1 问题后逐步扩大范围
3. 全量开放后保留 Feature Flag 支持毫秒级降级

> **V2.0 目标**：按租户百分比灰度（5% → 20% → 50% → 100%）

### §3.2 紧急发版通道（热修场景）

> **适用场景**：核心功能中断、安全漏洞、数据丢失风险。

**简化发版流程**：
```
热修请求 → [用户 Approve]
    ↓
@{coordinator} [Handoff: Branch_4] 请求简化 UAT
    ↓
→ 读取 `skills/HOTFIX_RELEASE_CHECKLIST.md` 执行简化检查
    ↓
跳过活文档生成
    ↓
快速发版（hotfix/* 分支）
```

**Hotfix 发版步骤**：
1. 确认触发条件
2. 等待 [用户 Approve]
3. 简化检查（仅 PRD/LLD/API 契约）
4. 快速打标 `hotfix/*`
5. 立即部署（需用户二次确认）

---

## §4 记忆与持久化

### §4.1 Token 预算护栏

- **单任务上下文上限**：8K Token
- **搜索结果截断**：搜索工具返回文档片段总和不超过 500 行
- **文件数量硬限制**：同时读取文件 ≤4 个（不含全局配置文件）
- **记忆文件豁免**：`docs/04_agent/memory/global/` 和 `docs/04_agent/memory/modules/` 不计入 4 文件限制，仅 `current/session_notes.md` 计入

### §4.2 上下文雪崩防护

遵循 `.ai/rules.md` §8.2。session_notes.md > 200 行时执行压缩。

### §4.3 会话结束状态更新

- 发版原则性决策（三问门禁通过） → `global/decisions.json`；具体方案归入对应文档
- 关键结论 → 压缩写入 `current/session_notes.md`
- 发版后归档 → `per_release/vX.Y.Z/summary.md`

---

## §5 SOP 标准发布步骤

1. **记忆恢复**: 读取三层记忆文件
2. **UAT Sign-off 校验**: 呼叫 `{coordinator}` 确认发版资产齐备。显式等待用户授权 `[UAT Approved - Ready for Release]`。**无授权不发版**
3. **变更审计**: 扫描自上一 Tag 以来的 Commit 和 PR，分析改动范围
4. **版本号裁定**: 按 §1.3 SemVer 规则计算新版本号
5. **资产转化**: API 契约 → `OPENAPI_SPEC.yaml`；业务逻辑 → `USER_MANUAL.md`；变更明细 → `CHANGELOG.md`
6. **API 契约版本同步**: 更新 `api/contracts/` 头部 `last_sync_version`
7. **Reasoning Trace 归档**: 遍历涉及的需求包，复制 `reasoning/*.md` 到 `docs/04_agent/memory/per_release/vX.Y.Z/`
8. **代码清理扫描**: 发现冗余代码 → 输出重构建议报告
9. **发版前置检查**: → **读取 `skills/RELEASE_CHECKLIST.md`**，逐条检查并标记 ✅/⚠️/❌
10. **分支清理**: PR 合并后立即删除远程与本地 feature/bugfix/hotfix 分支
11. **打标与触发**:
    ```bash
    git add . && git commit -m "release: vX.Y.Z"
    git tag vX.Y.Z
    git push origin main && git push --tags
    ```
    成功 → 触发部署流水线；失败 → 提示用户手动补推
12. **记忆归档与提升**: `global/` 快照到 `per_release/vX.Y.Z/summary.md`；评估 `modules/` 是否有跨模块复用价值 → 输出提升建议 → 等待 [用户 Confirm]

**Hotfix 简化发版模式**：
- 仅确认核心功能恢复
- 产出 `hotfix_checklist.md`
- 快速打标 `vX.Y.Z-hotfix.N`
- 跳过完整资产转化

---
