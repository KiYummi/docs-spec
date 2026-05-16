---
name: LLD_QUALITY_CHECKLIST
trigger: LLD/血肉填充完成后
contributors: [{architect}]
scope: Phase 3 LLD 编写
---

# LLD 质量检查清单

LLD/血肉填充完成后逐条自检，确保数据模型与架构合规。

## 检查项

### 数据模型合规

- [ ] 语义检查 — 实体与字段命名已在 glossary.md 中定义
- [ ] ER 一致性 — 新增/修改的表已注册到全局 ER 图，跨层依赖方向正确
- [ ] 枚举注册 — 新增的枚举值已注册到 Enum JSON，无同名不同义冲突
- [ ] 状态机字典 — 有状态机的实体已注册到 `state-machines/`，含 states + transitions + side_effects + inverse_path
- [ ] 防腐字段覆盖 — 所有表包含 id/tenant_id/is_deleted/deleted_at/created_by/created_at/updated_at/ext_json

### 权限与安全

- [ ] 权限注册 — 每个端点的 permission_code 已注册到 `permission_registry.json`，含 risk_level + rate_limit_level
- [ ] 安全基线链接 — Sub PRD 中 P1-P16 安全基线已改为链接引用 `SECURITY_BASELINE.md`，非全文抄写

### NFR 与架构

- [ ] NFR 数值聚合 — 本模块的 NFR 数值（缓存TTL/批量上限/并发阈值）已聚合到 `NFR_REGISTRY.md`
- [ ] 硬编码扫描 — 流程定义、角色名、待办类型通过配置而非硬编码
- [ ] ACL 映射 — 每个权限点已标注 {平台层} 层来源
- [ ] 契约完整性 — API 的 JSON 结构与状态码已写入 api/contracts/
- [ ] 架构合规性 — 系统拓扑满足无状态设计
- [ ] 沙盒合规性 — Mount Context 文件数量限制在 4 个以内
- [ ] ACL 完整性 — 所有第三方依赖已定义防腐层接口
- [ ] 决策持久化 — 原则性决策已写入 decisions.json（三问门禁通过），具体方案已落地到对应文档

## 参考

| # | 文档 | 读取范围 | 用途 |
|---|------|---------|------|
| R1 | `docs/00_meta/global-blueprint.md` 依赖矩阵 | ~40 行 | 模块依赖方向验证 |
| R2 | `.ai/rules.md` §5.5 | ~30 行 | 安全铁律 |

## 红旗

> 停止打勾，先解决：

- 新增表未注册到全局 ER → 后续所有 Agent 都会遗漏
- 发现硬编码枚举值 → 改为配置化再继续
- 原则性决策未写入 decisions.json → 后续可能重复争论同一问题
- 状态机未注册到 state-machines/ → 开发时无法校验转换合法性
- permission_code 未注册到 permission_registry.json → 权限校验缺失
