---
doc_type: "ADR"
module_id: "global_architecture"
version: "V 1.0"
phase: "Phase_3_Architecture"
status: "Draft"
complexity: "L1"
author_agent: "{architect}"
reviewer_agent: "{coordinator_agent}"
last_updated: "YYYY-MM-DDTHH:mm:ssZ"
approved_by: ""
depends_on: []
acl_dependencies: []
---

# 架构决策记录 (Architecture Decision Record)

## 标题: [如：ADR-001: 采用 PostgreSQL 的 JSONB 字段存储动态表单数据]
**状态**: [ ] 提议中 / [ ] 评审中 / [x] 已接受 / [ ] 已废弃
**日期**: YYYY-MM-DD
**决策人**: [{修订人}或Tech Lead名字]

## 1. 背景与上下文 (Context)
*描述引发这个架构决策的具体业务场景或技术痛点。*

## 2. 决策考量因素 (Decision Drivers)
*列出做决定时需要考虑的核心指标（例如：性能、开发成本、可维护性、云{管理端}锁定）。*
- [因素A，如：查询性能]
- [因素B，如：团队熟悉度]

## 3. 可选方案 (Considered Options)
*至少列出两个可选方案。*
- **方案 1**: [如：使用 MongoDB]
- **方案 2**: [如：使用 PostgreSQL JSONB]
- **方案 3**: [如：使用传统的 EAV 关系型表结构]

## 4. 最终决定 (Decision)
*明确写出最终选择了哪个方案，以及为什么选它（结合上述的考量因素）。*

## 5. 预期后果 (Consequences)
### 正面影响 (Positive)
*列出这个决定带来的好处。*

### 负面影响/妥协 (Negative/Compromises)
*列出这个决定带来的坏处或后续需要解决的技术债。*
