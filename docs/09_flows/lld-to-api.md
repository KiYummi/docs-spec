# LLD → API 流程

> **适用范围**：文档工程体系（docs-spec）
> **最后更新**：2026-05-16
> **涉及 Agent**：docs, coordinator, residual-auditor
> **涉及思想**：跳跃连接、Grounding

---

## 一、流程概述

```
LLD（低层设计文档）
    ↓
docs：填写溯源区
    ↓
docs：生成 API 合约
    ↓
residual-auditor：审计
    ↓
人：确认审计结果
```

---

## 二、详细步骤

### 步骤 1：填写溯源区（docs）

**职责**：docs 在 API 合约中填写需求溯源区

**操作**：
1. 读取 LLD 中的溯源区内容
2. 在 API 合约中创建"需求溯源区"章节
3. 将每条需求的 ID、语义要素、原文填入表格
4. **Grounding**：溯源区内容必须逐字复制上游原文，不得改写

**输出**：

```markdown
## 需求溯源区

| 原子需求 ID | 语义要素 | 来源（原文） | 推导链 |
|------------|---------|-------------|--------|
| @req-id: R001 | {要素描述} | {LLD 原文} | {API 设计推理过程} |
```

**规则**：
- 溯源区必须覆盖所有相关原子需求
- 溯源区内容必须逐字复制上游原文
- 溯源区由人工或工具填充，LLM 不得修改

### 步骤 2：生成 API 合约（docs）

**职责**：docs 根据 LLD 生成 API 合约

**操作**：
1. 读取 LLD 中的 API 设计
2. 生成 API 合约（OpenAPI/Swagger）
3. 包含：端点、请求/响应结构、错误码、权限码
4. 添加 `x-req-ids` 扩展字段，标注需求 ID

**输出**：API 合约文档

**规则**：
- API 合约必须承接 LLD 中的所有 API 设计
- 每个端点必须标注 `x-req-ids`
- 错误码必须符合 error-codes.json
- 权限码必须符合 permission-registry.json

### 步骤 3：审计（residual-auditor）

**职责**：residual-auditor 审计 API 合约的保真度

**操作**：
1. 提取原子需求基线
2. 检查语义覆盖率
3. 检查术语一致性
4. 检查数据流一致性
5. 输出审计报告

**输出**：审计报告 + 补丁建议

**规则**：
- 审计必须覆盖所有原子需求
- 审计结论必须包含推理链
- 补丁必须遵循 patch_schema.json

### 步骤 4：人确认审计结果（人在回路）

**职责**：人确认审计结果和补丁建议

**操作**：
1. 检查审计报告
2. 审批补丁建议
3. 确认或修改

**规则**：
- 人有最终决策权
- 人可以审批、拒绝、修改补丁
- 人确认后才可继续

---

## 三、API 合约中的需求标注

### 3.1 x-req-ids 扩展字段

在 API 合约中，每个端点必须包含 `x-req-ids` 扩展字段，标注该端点承接的需求 ID。

**示例**：

```yaml
paths:
  /api/v1/users:
    post:
      summary: 创建用户
      x-req-ids:
        - "@req-id: R001"
        - "@req-id: R002"
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: 创建成功
```

### 3.2 标注规则

- 每个端点必须标注 `x-req-ids`
- `x-req-ids` 必须是数组格式
- 每个需求 ID 必须符合 `@req-id: R{序号}` 格式
- 一个端点可以承接多个需求

---

## 四、检查清单

- [ ] 溯源区是否存在？
- [ ] 溯源区是否覆盖所有相关原子需求？
- [ ] 溯源区内容是否逐字复制上游原文？
- [ ] 每条需求是否标注了唯一 ID？
- [ ] API 合约是否承接了 LLD 中的所有 API 设计？
- [ ] 每个端点是否标注了 `x-req-ids`？
- [ ] 错误码是否符合 error-codes.json？
- [ ] 权限码是否符合 permission-registry.json？
- [ ] 审计是否通过？
- [ ] 人是否确认了审计结果？
