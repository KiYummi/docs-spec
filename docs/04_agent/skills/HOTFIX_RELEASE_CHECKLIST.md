---
name: HOTFIX_RELEASE_CHECKLIST
trigger: Hotfix 发版时
contributors: [{devops}]
scope: Phase 6 Hotfix 紧急发版
---

# Hotfix 发版检查清单

Hotfix 紧急发版时逐条检查，确保功能恢复、回滚就绪、文档同步。

## 检查项

### 功能验证

- [ ] 核心功能恢复验证通过 — 修复目标已达成
- [ ] 无副作用确认 — 修改不影响其他功能
- [ ] 监控告警正常 — 无新增异常

### 回滚与灰度

- [ ] 回滚方案就绪 — 可快速回退
- [ ] 灰度策略 — 白名单租户 → 确认无 P0/P1 → 扩大范围 → 全量开放 + Feature Flag

### 文档同步

- [ ] CHANGELOG 更新 — 含 Hotfix 记录
- [ ] 监控看板更新 — 新增告警规则
- [ ] 事后复盘记录 — 已写入 session_notes

## 参考

| # | 文档 | 读取范围 | 用途 |
|---|------|---------|------|
| R1 | `docs/05_plans/quality-gate.md` §Gate 10 Hotfix | ~30 行 | Hotfix 发版标准 |

## 红旗

> 停止打勾，先解决：

- 核心功能未恢复 → 阻断发版
- 无回滚方案 → 先准备回滚
- 监控告警异常 → 先排查
