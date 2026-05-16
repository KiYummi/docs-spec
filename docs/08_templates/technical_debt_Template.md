---
doc_type: TECHNICAL_DEBT
source_phase: Phase_X
source_gate: Gate_X
status: Open
module: [模块名]
created_at: YYYY-MM-DDTHH:MM:SS
---

# 技术债条目

> **记录位置**：`docs/04_agent/memory/global/technical_debt.json`（全局活账本，跨 Phase 1~6）
> **登记时机**：每个 Gate 通过时，本 Gate 产生的推迟/简化/妥协项必须登记入账

### DEBT-{NNN}: [债务标题]

| 字段 | 内容 |
|:---|:---|
| **来源** | [功能推迟 / 流程简化 / 硬编码推迟 / 交付物遗漏 / 外部依赖] |
| **来源 Phase/Gate** | Phase_X / Gate_X |
| **描述** | [具体描述] |
| **影响范围** | [受影响的接口/功能] |
| **风险等级** | 高/中/低 |
| **还债目标** | [Gate_X / V1.5 / V2.0] |
| **关联文档** | [PRD/LLD 链接] |
| **关联代码** | [代码路径] |

<!-- 修复后添加以下字段 -->
### 解决记录
| 字段 | 内容 |
|:---|:---|
| **解决版本** | vX.Y.Z |
| **解决日期** | YYYY-MM-DD |
| **解决PR** | #XXX |
