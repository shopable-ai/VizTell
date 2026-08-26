# schemas

本目录保存 `AI原生知识系统` 的机器可读 Schema、枚举、样例、派生生成器与迁移说明。

语义事实源仍是 Markdown 正式文件。特别是问题宇宙：

- `../01A_用户旅程、需求与高频问题现象宇宙.md`：用户阶段、场景与原话；
- `../01B_标准用户问题与专业问题映射.md`：SUP、主映射与关联映射；
- `../01_需求宇宙.md`：canonical P-L1 / P-L2、人话问题地图与 legacy alias；

其他机器对象的语义事实源包括：

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

当前 Schema 仍为：

> **v0.1 experimental**

用途：

- 验证对象边界；
- 支持 Synthetic Benchmark；
- 暴露字段冲突与遗漏；
- 为后续原型提供稳定接口候选；
- 对 canonical P-L2、SUP 主映射、多阶段/多场景标签和迁移别名进行机器审计。

不代表：

- 所有枚举已经冻结；
- 所有权重和阈值已经确定；
- 真实书库已经开始批处理；
- JSON/JSONL 可以取代人话 Markdown 事实源。

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
- `problem-registry.schema.json`

问题注册表同时提供：

- `generate_problem_registry.py`

它从 `01 / 01B / 22` **派生** canonical P-L2 JSONL，而不是要求人工维护第二套事实源。

默认输出：

```text
schemas/problem-registry.generated.jsonl
```

运行：

```bash
python docs/AI原生知识系统/schemas/generate_problem_registry.py --check
python docs/AI原生知识系统/schemas/generate_problem_registry.py
```

生成器当前硬性检查：

- 151 个 canonical P-L2；
- 32 个 legacy alias / 降级项；
- 94 个 SUP；
- canonical ID 不得与 legacy alias 重叠；
- `primary_p_l1` 必须与 P-L2 编号主空间一致；
- 人话问题、后果、用户需求、理想结果不能为空。

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

1. Schema 校验成功只表示**结构合法**，不表示知识正确或分类一定正确。
2. `unknown`、`not_evaluated`、`not_applicable` 不应被模型随意补成确定值。
3. 主体价值、学习差额、路由不得永久写死在 Canonical identity 中。
4. Relation Assertion 与 Routing Decision 必须可版本化和重算。
5. Problem Registry 的人工语义必须先修改 `01 / 01B`，再重新生成；禁止直接修改 generated JSONL 制造并行事实源。
6. 一个问题跨阶段、场景或主体时，优先增加标签和关联，不得因为标签变化复制 canonical P-L2。
7. 真实资料只有在 `validation-manifest.schema.json` 对应 Manifest 建立后才能进入受控内容验证。
8. v0.x 允许破坏性调整，但每次调整必须同步回归 `../22_遗漏、反例与回归测试.md`。
