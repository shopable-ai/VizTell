# schemas

本目录保存 `AI原生知识系统` 的机器可读 Schema、枚举、样例与迁移说明。

语义事实源仍是：

- `../14_术语、编号与Schema.md`
- `../15_需求模式与场景矩阵.md`
- `../16_知识原子、标准知识与关系模型.md`
- `../17_海量知识去重、增量与饱和协议.md`
- `../18_知识价值、学习投入与消费路由.md`
- `../19_知识到Search-RAG-Skill-Workflow-Agent-软件的能力路由.md`
- `../21_验证计划、样本清单与数据边界.md`
- `../22_遗漏、反例与回归测试.md`

---

## 当前版本

当前首批 Schema 为：

> **v0.1 experimental**

用途：

- 验证对象边界；
- 支持 Synthetic Benchmark；
- 暴露字段冲突与遗漏；
- 为后续原型提供稳定接口候选。

不代表：

- 所有枚举已经冻结；
- 所有 L4 权重和阈值已经确定；
- 真实书库已经开始批处理。

---

## Schema dialect

统一采用：

```json
"$schema": "https://json-schema.org/draft/2020-12/schema"
```

---

## v0.1 文件

- `source.schema.json`
- `evidence.schema.json`
- `knowledge-atom.schema.json`
- `canonical-knowledge.schema.json`
- `relation-assertion.schema.json`
- `learning-gap.schema.json`
- `routing-decision.schema.json`
- `implementation-routing.schema.json`
- `benchmark-case.schema.json`
- `validation-manifest.schema.json`

后续可能新增：

- raw-fragment；
- subject-profile；
- increment-decision；
- benchmark-run；
- data-usage-log；
- capability-registry；
- version-migration。

---

## Schema 使用纪律

1. Schema 校验成功只表示**结构合法**，不表示知识正确。
2. `unknown`、`not_evaluated`、`not_applicable` 不应被模型随意补成确定值。
3. 主体价值、学习差额、路由不得永久写死在 Canonical identity 中。
4. Relation Assertion 与 Routing Decision 必须可版本化和重算。
5. 真实资料只有在 `validation-manifest.schema.json` 对应 Manifest 建立后才能进入受控内容验证。
6. v0.x 允许破坏性调整，但每次调整必须同步回归 `../22_遗漏、反例与回归测试.md`。
