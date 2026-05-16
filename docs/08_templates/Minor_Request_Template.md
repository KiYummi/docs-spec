---
doc_type: "Minor_Request"
module_id: "ops_ticket_XXX"
version: "V 1.0"
phase: "Phase_2_Requirement"
status: "Draft"
priority: "P2"
complexity: "L1"
author_agent: "{pm_agent}"
reviewer_agent: "{coordinator_agent}"
last_updated: "YYYY-MM-DDTHH:mm:ssZ"
approved_by: ""
depends_on: []
# === 小需求特有字段 ===
request_type: "feature"  # feature | bugfix | config | data | ops
estimated_effort: "S"    # S(0.5d) | M(1-2d) | L(3-5d)
related_prd: ""          # 关联的 PRD 模块 ID（如有）
---

# [工单标题] - Minor Request

## 变更记录
| 日期 | 版本 | 变更摘要 | 操作人 |
| :--- | :--- | :--- | :--- |
| YYYY-MM-DD | v1.0.0 | 初始提交 | - |

## 1. 需求背景 (Context)
*简述为什么需要这个小需求/工单，关联的业务场景。*

## 2. 需求描述 (Description)
*清晰描述具体要做什么，可以是功能点、配置变更、数据修复等。*

### 2.1 当前状态 (Current State)
*描述当前的问题或现状。*

### 2.2 期望状态 (Expected State)
*描述完成后的期望效果。*

## 3. 验收标准 (Acceptance Criteria)
- [ ] 标准 1: [可验证的验收条件]
- [ ] 标准 2: [可验证的验收条件]

## 4. 影响范围评估 (Impact Analysis)
| 影响维度 | 评估结果 | 说明 |
| :--- | :--- | :--- |
| 涉及模块 | [模块名] | |
| 数据库变更 | 是/否 | 如有，说明表/字段 |
| 接口变更 | 是/否 | 如有，说明 API |
| 配置变更 | 是/否 | 如有，说明配置项 |
| 上下游依赖 | 是/否 | 如有，说明依赖方 |

## 5. 实施方案 (Implementation)
*简述实施步骤，复杂度 L1 的情况可以省略详细设计。*

## 6. 测试要点 (Test Points)
- [ ] 测试点 1
- [ ] 测试点 2

## 7. 回滚方案 (Rollback Plan)
*如果上线后出问题，如何快速回滚。*
