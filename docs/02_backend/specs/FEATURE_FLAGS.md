# 特性开关 (Feature Flags)

> **doc_type**: FEATURE_FLAGS
> **phase**: Phase_3
> **用途**: 定义功能开关规范

---

## 1. 开关分组

| 分组 | 说明 | 控制范围 |
|------|------|---------|
| Group A | 核心链路 | {说明} |
| Group B | 增强功能 | {说明} |
| Group C | 后续迭代 | {说明} |

## 2. 开关注册表模板

| flag_code | 名称 | Group A | Group B | Group C | 说明 |
|-----------|------|---------|---------|---------|------|
| `{feature}.{name}` | {名称} | on/off | on/off | on/off | {说明} |

## 3. 使用规范

- 代码中只认 `feature_code`，禁止硬编码版本名
- 开关状态通过配置中心动态下发
- 开关变更必须有灰度策略
