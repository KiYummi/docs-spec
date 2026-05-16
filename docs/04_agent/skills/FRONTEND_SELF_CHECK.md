---
name: FRONTEND_SELF_CHECK
trigger: 编码完成、提交前自检
contributors: [{frontend}]
scope: Phase 3~5 前端编码
---

# 前端商业级代码自检清单

前端编码完成提交前逐条自检，覆盖安全、规范、测试全维度。

## 检查项

### 安全与健壮性

- [ ] 安全兜底 — 无 v-html / dangerouslySetInnerHTML
- [ ] 表单防抖 — 提交按钮防抖，输入框前端正则校验
- [ ] 健壮性 — 异步操作有 loading/error 状态，无未捕获异常

### 规范与契约

- [ ] 规范性 — 组件拆分合理，无未使用导入
- [ ] 契约对齐 — API 路径/Method/请求体与 api/contracts/ 完全一致
- [ ] 设计系统同步 — 新建基础/业务组件已更新 

### 测试与 Mock

- [ ] TDD 用例全绿 — test_cases/ 测试大纲全部通过
- [ ] Mock 状态更新 — Mock 开发已标记 Pending，后端就绪后标记 Verified

### 组件与防腐

- [ ] 新建组件检查 — 在 src/components/，已区分基础/业务组件
- [ ] 防腐层确认 — LLD 防腐层接口已定义，通过接口而非直接依赖
- [ ] 无状态 — 无跨请求内存状态，状态管理集中在 store

## 参考

| # | 文档 | 读取范围 | 用途 |
|---|------|---------|------|
| R1 | `.ai/rules.md` §5.5 | ~30 行 | 安全铁律 |
| R2 | `docs/00_meta/dev-spec.md` §10 | ~50 行 | 编码标准 |
| R3 | `docs/00_meta/` | 按需 | 设计系统规范 |

## 红旗

> 停止打勾，先解决：

- 发现 v-html 或 dangerouslySetInnerHTML → 替换为安全渲染
- API 路径硬编码 → 改为从契约文件生成
- 测试未全部通过 → 不提交
