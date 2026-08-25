# 评测、Benchmark 与质量指标

> 目标：避免“已建库／已向量化／已生成 Skill／Agent 跑了一次”被误认为完成。所有关键能力都需要可测、可回归、可解释。

当前阶段优先：

> **Synthetic Benchmark → Schema Validation → Framework Regression**

真实资料 Benchmark 受 `21_验证计划、样本清单与数据边界.md` 约束。

---

# 一、评测对象

- 来源解析质量；
- provenance 完整性；
- Knowledge Atom 类型识别；
- Canonical Resolution；
- 重复／改写／条件／边界／冲突关系判断；
- 知识增量判断；
- 来源与证据判断；
- 主体价值排序；
- 学习适配与 Knowledge Gap；
- Human / AI / Tool 能力归属；
- Full-text／Semantic／Hybrid Retrieval；
- RAG 最小充分上下文；
- Skill／Workflow／Agent 路由；
- AI Capability 可靠性；
- 人工学习后的回忆、辨别、应用与迁移；
- 时间更新、过时和替代识别；
- Impact Propagation；
- 风险、权限、人工关口和回滚。

---

# 二、Benchmark 五层结构

## B0 Schema / Invariant

测试：

- 字段是否合法；
- required 是否满足；
- ID / enum 是否正确；
- 不允许的状态组合是否被发现。

## B1 Synthetic Semantic

人工构造答案明确的：

- 等价；
- 新条件；
- 新边界；
- 冲突；
- 伪多源；
- 主体价值；
- 学习差额；
- 实现路由。

见 `22`。

## B2 Controlled Real Sample

使用 Manifest 明确的小样本验证真实噪声、表达变化和数据复杂度。

当前不默认进入此层。

## B3 Scale / Performance

测试：

- 召回；
- latency；
- cost；
- candidate explosion；
- 人工复核量；
- 增量处理吞吐。

## B4 Outcome / Longitudinal

测试真实长期结果：

- 是否帮助项目决策；
- 是否减少重复学习；
- 是否提高人工能力；
- 是否降低错误；
- 是否能稳定更新；
- 自动化是否节约总成本。

---

# 三、核心质量指标

## 3.1 Canonical / 去重

- duplicate candidate recall；
- false merge rate；
- missed equivalence rate；
- wrong alias rate；
- condition/boundary preservation rate；
- provenance retention rate。

## 3.2 增量

- new mechanism recall；
- new condition recall；
- new boundary recall；
- new counterexample recall；
- new independent evidence recall；
- decision-changing increment recall；
- false novelty rate。

## 3.3 Evidence

- primary source tracing accuracy；
- evidence independence accuracy；
- source fidelity error rate；
- weak-evidence-as-fact rate；
- conflict preservation rate；
- unsupported upgrade rate。

## 3.4 Retrieval

- Recall@K；
- Precision@K；
- MRR / NDCG 类排序；
- critical source miss rate；
- metadata/time/permission filter accuracy；
- candidate set size。

## 3.5 RAG

- answer correctness；
- citation correctness；
- evidence coverage；
- context redundancy；
- conflict handling；
- unsupported inference rate；
- minimum sufficient context quality。

## 3.6 Subject Value / Routing

- high-value miss rate；
- low-value attention waste；
- false human-learning recommendation；
- false automation recommendation；
- existing-tool miss rate；
- Agent over-routing rate；
- Software over-productization rate。

## 3.7 Learning

- delayed recall；
- concept discrimination；
- boundary recognition；
- standard execution；
- edge-case adaptation；
- cross-context transfer；
- confidence calibration；
- real-task performance。

## 3.8 Lifecycle / Governance

- stale detection latency；
- impacted-object recall；
- local update correctness；
- version lineage completeness；
- rollback success；
- human takeover success；
- unauthorized-action rate；
- audit completeness。

---

# 四、Error Taxonomy

评测不能只看平均准确率，至少记录：

- false merge；
- false split；
- false novelty；
- missed boundary；
- missed counterexample；
- false conflict；
- conflict collapse；
- source lineage collapse；
- stale knowledge served；
- high-value knowledge ignored；
- low-value knowledge interrupts human；
- human-learning overinvestment；
- automation overreach；
- wrong softwareization；
- lost provenance；
- irreversible wrong action。

不同错误需要不同 severity。

---

# 五、Benchmark Case 必须有 Forbidden Outcomes

不能只写“期望答案”。

例如：

```yaml
benchmark_case:
  case_id: SYN-R02
  inputs: []
  expected:
    relation_type: adds_condition
    canonical_merge: false
  forbidden:
    - paraphrase_equivalent
    - automatic_delete
  severity_if_failed: high
```

Forbidden Outcomes 对防止危险捷径尤其重要。

---

# 六、人工 Gold 与 LLM Judge 分工

高价值 Benchmark 不能完全让被测 LLM 自己当裁判。

建议：

- 明确结构化案例：规则/人工 Gold；
- 语义边界案例：人工专家 Gold + 多模型辅助；
- 大规模低风险监测：LLM Judge 可以辅助；
- 高风险 merge/replaces/automation：保留人工复核。

任何 LLM Judge 本身也需要校准和版本记录。

---

# 七、回归触发器

以下变化都应触发相应 Regression Set：

- Schema 变化；
- Embedding 变化；
- Reranker 变化；
- LLM 变化；
- Prompt/Skill 变化；
- relation taxonomy 变化；
- routing rule 变化；
- threshold 变化；
- time/version logic 变化；
- permission policy 变化。

---

# 八、当前 Synthetic Benchmark

正式合成回归案例维护于：

`22_遗漏、反例与回归测试.md`

当前至少覆盖：

- paraphrase vs adds_condition；
- boundary/counterexample；
- alias vs homonym；
- evidence independence；
- real vs apparent conflict；
- knowledge quality vs subject value；
- individual learning gap；
- AI capability vs automation permission；
- Search/RAG/Workflow/Agent/Software route；
- valid time / superseded / impact propagation；
- rollback / governance。

---

# 九、真实样本进入 Gate

进入 B2 前必须：

- 已定义要验证的能力；
- 已通过相应 Synthetic Set；
- 已创建 Validation Sample Manifest；
- 已列出样本和读取范围；
- 已定义 allowed/prohibited operations；
- 已定义输出位置；
- 已定义停止条件。

未满足则不得默认扫描现有资料库。

---

# 十、停止与验收原则

- 不以文件数量作为完成指标；
- 不以向量条数、Wiki 页数、Skill 数量或 Agent 数量作为完成指标；
- 不以单次 Demo 成功作为能力通过；
- 以真实需求能否稳定找到、判断、学习、调用、验证、更新和恢复正确知识为核心；
- 在新增资料边际知识价值持续很低时允许停止全量深处理；
- 高风险错误即使平均指标很好，也可能触发一票否决。

---

# 十一、一票否决候选

以下任一严重问题都不能用平均分掩盖：

- 丢失 provenance；
- 自动删除唯一来源；
- 把条件不同的知识错误合并；
- 把弱证据自动升级为事实；
- 把高风险 AI 能力自动授权执行；
- 错误版本替代且无法回滚；
- 未授权读取/处理真实知识资产；
- 工具成功被误判为任务完成。
