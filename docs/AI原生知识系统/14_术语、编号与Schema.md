# 术语、编号与 Schema

> 本文件把框架从“人能读的文档”升级为“机器可处理的统一协议”。Markdown 语义定义仍是当前事实源；`schemas/` 保存可执行的 v0.x JSON Schema。

Schema 只约束数据合同，不证明知识真实或路由正确。

---

## 一、编号规则

### Framework

- `L1-xx`：一级空间；
- `L2-xx-yy`：二级维度；
- `L3-xx-yy-zz`：三级指标。

### Knowledge Objects

- `S-*`：Source；
- `F-*`：Raw Fragment；
- `A-*`：Normalized Knowledge Atom；
- `K-*`：Canonical Knowledge；
- `E-*`：Evidence；
- `EG-*`：Independent Evidence Group；
- `R-*`：Relation Assertion。

### Demand / Subject / Decision

- `D-*`：Requirement / Demand Instance；
- `SP-*`：Subject Profile；
- `LG-*`：Learning Gap；
- `C-*`：Consumption / Capability Ownership / Routing Decision；
- `IR-*`：Implementation Routing Decision。

### Validation / Runtime

- `BC-*`：Benchmark Case；
- `BR-*`：Benchmark Run；
- `VM-*`：Validation Sample Manifest；
- `VR-*`：Validation Run / Data Usage Log；
- `ACT-*`：processing/adjudication activity；
- `INC-*`：Increment Decision。

---

## 二、对象链

```text
D Requirement
→ S Source
→ F Raw Fragment
→ A Knowledge Atom
→ K Canonical Knowledge
→ E Evidence / R Relation Assertion / INC Increment Decision
→ SP Subject Profile / LG Learning Gap
→ C Consumption Routing
→ IR Implementation Routing
→ BC/BR Validation
```

这些对象不能压成一个巨型 `knowledge-node`。

---

## 三、Source 最小字段族

```yaml
source_id:
carrier_type:
title:
author_or_org:
source_level:
published_at:
observed_at:
version:
location:
upstream_source_refs: []
independence_group:
license:
access_class:
credibility_state:
created_at:
updated_at:
```

Source 是来源对象，不代表其中所有 Claim 的可信度相同。

---

## 四、Raw Fragment 最小字段族

```yaml
fragment_id:
source_id:
locator:
raw_text_or_ref:
language:
parser_version:
parse_quality:
created_at:
```

`locator` 必须能回到页面、章节、时间戳、代码行或其他原始位置。

---

## 五、Knowledge Atom 最小字段族

```yaml
atom_id:
fragment_refs: []
knowledge_type:
normalized_statement:
labels: []
conditions: []
scope: []
temporal: {}
extraction_confidence:
created_by_activity:
```

Atom 是候选语义单元，不等于 Canonical，也不等于已经验证为真。

---

## 六、Canonical Knowledge 最小字段族

```yaml
knowledge_id:
knowledge_type:
canonical_label:
aliases: []
canonical_statement:
type_payload: {}
conditions: []
scope: []
boundaries: []
exceptions: []
source_refs: []
fragment_refs: []
evidence_refs: []
relation_refs: []
provenance: {}
epistemic_state:
temporal_state: {}
version:
created_at:
updated_at:
```

`type_payload` 根据 Concept / Claim / Mechanism / Method / Procedure / DecisionRule 等类型采用不同结构。

---

## 七、Evidence 最小字段族

```yaml
evidence_id:
target_claim_refs: []
evidence_type:
direction:
source_refs: []
primary_source_ref:
independence_group:
directness:
method_quality:
limitations: []
applicable_scope: []
temporal: {}
```

---

## 八、Relation Assertion 最小字段族

```yaml
relation_id:
subject_id:
relation_type:
object_id:
evidence_refs: []
rationale:
adjudication_status:
confidence:
created_by:
created_at:
reviewed_at:
supersedes_relation_id:
```

Relation 本身可以被修订和推翻。

---

## 九、Requirement Instance 最小字段族

```yaml
requirement_id:
patterns: []
actor:
intent:
target:
project_stage:
time_horizon:
scope:
mastery_depth:
latency_tolerance:
failure_cost:
evidence_need:
recurrence:
uncertainty:
constraints: []
prior_priority:
```

`prior_priority` 是需求侧先验，不是系统最终处理优先级。

---

## 十、Subject Profile / Learning Gap

```yaml
subject_profile:
  subject_id: SP-...
  knowledge_states: []
  skill_states: []
  verified_at:

learning_gap:
  gap_id: LG-...
  subject_id:
  knowledge_id:
  current_level:
  target_level:
  known_components: []
  missing_components: []
  misconceptions: []
  missing_prerequisites: []
  estimated_cost: {}
```

---

## 十一、Consumption / Capability Routing

```yaml
routing_decision:
  decision_id: C-...
  requirement_id:
  knowledge_id:
  epistemic_gate: {}
  subject_utility: {}
  learning_gap_ref:
  substitution: {}
  capability_ownership: {}
  primary_route:
  secondary_routes: []
  rationale: []
  review_triggers: []
  computed_at:
```

同一知识面对不同主体和目标可以有不同 Routing Decision。

---

## 十二、Implementation Routing

```yaml
implementation_routing:
  route_id: IR-...
  requirement_id:
  capability:
  task_characteristics: {}
  candidates: []
  selected: {}
  rejected: []
  constraints: []
  review_triggers: []
  computed_at:
```

必须保留 rejected alternatives，防止只留下“用了 Agent”却不知道为什么。

---

## 十三、Benchmark Case

```yaml
benchmark_case:
  case_id: BC-...
  category:
  description:
  inputs: []
  expected: {}
  forbidden: []
  severity_if_failed:
  rationale:
  status:
```

---

## 十四、Validation Manifest

```yaml
validation_manifest:
  manifest_id: VM-...
  validation_goal: []
  sample_selection: {}
  samples: []
  prohibited_scope: []
  allowed_operations: {}
  output_location: []
  promotion_rule: {}
  stop_conditions: []
```

没有 Manifest 不进入真实资料内容处理。

---

## 十五、Relation Type 候选

### Concept

`alias_of`、`broader_than`、`narrower_than`、`related_to`、`overlaps_with`

### Proposition / Mechanism

`equivalent_to`、`paraphrase_of`、`contains`、`refines`、`adds_condition`、`adds_boundary`、`adds_scope`、`adds_mechanism`、`supports`、`weakens`、`conflicts_with`、`counterexample_to`

### Provenance / Version

`derived_from`、`quoted_from`、`revision_of`、`alternate_representation_of`、`has_primary_source`、`supersedes`

### Capability

`prerequisite_of`、`depends_on`、`complements`、`substitutes_for`、`implemented_by`

---

## 十六、Unknown / Null / Not Applicable 必须区分

禁止模型遇到空字段就自动补成确定事实。

建议至少区分：

- `unknown`：当前不知道；
- `not_evaluated`：尚未评估；
- `not_applicable`：该字段对当前对象无意义；
- `null`：仅在 Schema 明确定义语义时使用。

不能把“没有证据字段”理解成“证据为零”，也不能把“未评估风险”理解成“无风险”。

---

## 十七、状态对象与知识本体分离

以下内容不应永久嵌死在 Canonical identity：

- 主体价值；
- Learning Gap；
- Consumption Route；
- Implementation Route；
- AI capability；
- current project relevance。

它们随主体、时间、项目和工具变化，应作为独立状态/决策对象。

---

## 十八、Schema 基线

当前首批可执行 Schema 使用：

```json
"$schema": "https://json-schema.org/draft/2020-12/schema"
```

Schema version 与领域对象 version 分开：

- `schema_version`：数据合同版本；
- `version`：对象自身版本。

---

## 十九、Schema 演进原则

1. Markdown 先固定语义，再更新 JSON Schema；
2. 不因某个 LLM 输出方便而扭曲领域语义；
3. 新增字段前先判断是否可由现有对象/维度表达；
4. 字段变化考虑历史迁移和 backward compatibility；
5. 机器评分必须可回到 L2/L3，不保留不可解释总分；
6. Schema 校验成功只说明结构合法，不代表语义正确；
7. 重要对象尽量有 stable ID、version、provenance；
8. 关系和路由必须可修订，不允许不可逆内嵌。

---

## 二十、主流标准映射

当前保持轻量内部模型，同时预留：

- Concept label/hierarchy → SKOS-compatible；
- provenance / derived / revision → W3C PROV-compatible；
- machine contract → JSON Schema 2020-12；
- AI lifecycle risk → NIST AI RMF-aligned governance principles。

详细记录见 `research-notes/2026-08-25_主流框架校准.md`。
