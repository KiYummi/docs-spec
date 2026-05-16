---
name: interaction-protocol
description: Agent 交互协议 — 角色间流转关系、Diff Summary、Handoff 格式
---

# Agent 交互协议

## 角色间流转关系

```
PM → Coordinator → Architect → Developer(Backend/Frontend) → Reviewer → QA → DevOps
                     ↑                                         ↓
                     └──── 发现问题退回 ──────────────────────┘
```

## Diff Summary 格式

每次完成任务后回传审查时，必须携带标准化 Diff Summary：

```
**变更范围 (Scope)**: [如：修改 src/xxx.py, 新增 tests/test_xxx.py]
**核心逻辑变更 (Delta)**:
- 新增: [如：实现 XX 接口 CRUD 逻辑]
- 删除: [如：无]
- 修改: [如：调整 YY 模块的数据校验规则]
**风险自评**:
- [ ] 涉及数据库 DDL 变更
- [ ] 涉及权限/越权逻辑
- [ ] 涉及核心金额计算
- [x] 无高风险变更
**关联 AC**: [对应任务验收标准]
```

## Handoff 交接格式

向下游交接时：

```
@<角色> <任务摘要>

[Diff Summary]
（上方格式）

[Mount Context]
1. <相关文件路径 1>
2. <相关文件路径 2>
```

## 审查读取优先级

| 优先级 | 读取内容 | 触发条件 |
|--------|---------|---------|
| P1（必须） | Diff Summary + 验收标准 | 每次审查必读 |
| P2（按需） | 源文件 | Diff 涉及高危逻辑时 |
| P3（禁止） | 无差别全量读取 | 绝对禁止 |
