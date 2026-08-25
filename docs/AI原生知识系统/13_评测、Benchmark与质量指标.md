# 评测、Benchmark 与质量指标

> 目标：避免“已建库／已向量化／已生成 Skill／Agent 跑了一次”被误认为完成。所有关键能力都需要可测、可回归、可解释。

当前阶段优先：

> **Synthetic Benchmark → Schema Validation → Framework Regression**

真实资料 Benchmark 受 `21_验证计划、样本清单与数据边界.md` 约束。

---

# 一、评测必须分三层

## 1.1 Problem-level：用户问题层

首先评测：

- 是否理解了用户真正的问题；
- 是否把问题范围界定正确；
- 是否发现了真正需要的知识；
- 是否遗漏关键未知；
- 是否在应该停止研究时停止；
- 最终结果是否帮助理解、判断、学习、决策或行动。

## 1.2 Capability-level：系统能力层

评测：

- 检索；
- 多来源综合；
- 证据判断；
- 去重与增量；
- 学习路由；
- 决策支持；
- 人机分工；
- 变化监测；
- 结果验证。

## 1.3 Component-level：知识工程组件层

评测：

- Source / provenance；
- Atom；
- Canonical；
- Relation；
- Schema；
- Routing object；
- 权限、版本、回滚等。

> **组件准确不等于用户问题解决。**

---

# 二、评测对象

## 2.1 用户问题与任务

- 问题澄清质量；
- 问题框定质量；
- 知识需求识别；
- 已知 / 未知 / 误解判断；
- 研究问题生成；
- 资料选择优先级；
- 多来源综合；
- 方案形成与比较；
- 决策支持；
- 行动转化；
- 结果验证；
- 新知识缺口发现；
- 停止研究判断。

## 2.2 知识与能力组件

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

# 三、Benchmark 六层结构

## B0 Schema / Invariant

测试字段、required、ID、enum 和不允许的状态组合。

## B1 Synthetic Component

人工构造答案明确的：

- 等价；
- 新条件；
- 新边界；
- 冲突；
- 伪多源；
- 主体价值；
- 学习差额；
- 实现路由。

## B2 Synthetic Problem / Task

人工构造完整用户问题，测试：

- 是否抓住真实问题；
- 是否识别知识需求；
- 是否选择正确研究路径；
- 是否保留关键条件与冲突；
- 是否形成有效方案；
- 是否在足够时停止；
- 是否真正回答用户最初的问题。

## B3 Controlled Real Sample

使用 Manifest 明确的小样本验证真实噪声、表达变化和数据复杂度。

当前不默认进入此层。

## B4 Scale / Performance

测试召回、latency、cost、candidate explosion、人工复核量和增量吞吐。

## B5 Outcome / Longitudinal

测试长期结果：

- 是否改善项目决策；
- 是否减少无效阅读与重复学习；
- 是否提高人工能力；
- 是否减少错误；
- 是否更快推进任务；
- 是否能稳定更新；
- 自动化是否降低总成本。

---

# 四、Problem-level 核心指标

## 4.1 问题理解

- true-problem identification rate；
- wrong-problem answer rate；
- scope error rate；
- missed constraint rate；
- success-criteria completeness。

## 4.2 知识需求

- critical knowledge need recall；
- prerequisite gap recall；
- irrelevant research rate；
- unknown-unknown discovery rate；
- unnecessary information expansion rate。

## 4.3 研究与综合

- critical source miss rate；
- redundant reading / processing rate；
- condition/boundary preservation rate；
- unresolved conflict preservation；
- decision-changing increment recall；
- research stop accuracy。

## 4.4 用户结果

- answer usefulness；
- decision support quality；
- actionability；
- task progress impact；
- time saved；
- avoided attention waste；
- downstream correction rate；
- user outcome success rate。

---

# 五、知识工程核心质量指标

## 5.1 Canonical / 去重

- duplicate candidate recall；
- false merge rate；
- missed equivalence rate；
- wrong alias rate；
- condition/boundary preservation rate；
- provenance retention rate。

## 5.2 增量

- new mechanism recall；
- new condition recall；
- new boundary recall；
- new counterexample recall；
- new independent evidence recall；
- decision-changing increment recall；
- false novelty rate。

## 5.3 Evidence

- primary source tracing accuracy；
- evidence independence accuracy；
- source fidelity error rate；
- weak-evidence-as-fact rate；
- conflict preservation rate；
- unsupported upgrade rate。

## 5.4 Retrieval / RAG

- Recall@K；
- Precision@K；
- MRR / NDCG；
- critical source miss rate；
- filter accuracy；
- context redundancy；
- citation correctness；
- evidence coverage；
- unsupported inference rate；
- minimum sufficient context quality。

## 5.5 Subject Value / Routing

- high-value miss rate；
- low-value attention waste；
- false human-learning recommendation；
- false automation recommendation；
- existing-tool miss rate；
- Agent over-routing rate；
- Software over-productization rate。

## 5.6 Learning

- delayed recall；
- concept discrimination；
- boundary recognition；
- standard execution；
- edge-case adaptation；
- cross-context transfer；
- confidence calibration；
- real-task performance。

## 5.7 Lifecycle / Governance

- stale detection latency；
- impacted-object recall；
- local update correctness；
- version lineage completeness；
- rollback success；
- human takeover success；
- unauthorized-action rate；
- audit completeness。

---

# 六、Error Taxonomy

除已有知识工程错误外，必须新增用户问题层错误：

## Problem Errors

- wrong problem framing；
- premature solutioning；
- missed knowledge need；
- over-research；
- under-research；
- wrong stopping；
- high-quality answer to wrong question；
- synthesis without actionability；
- solution detached from user constraints；
- no outcome verification。

## Knowledge / System Errors

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

不同错误必须有 severity，不得只看平均准确率。

---

# 七、Benchmark Case 必须有 Forbidden Outcomes

不能只写“期望答案”。

```yaml
benchmark_case:
  case_id: SYN-P02
  requirement: "..."
  problem_refs:
    - P-L2-01-04
    - P-L2-02-01
  expected:
    true_problem: "..."
    research_needed: true
    stop_when: "..."
  forbidden:
    - answer_surface_question_without_reframing
    - default_agent_solution
    - scan_unapproved_real_corpus
  severity_if_failed: high
```

Forbidden Outcomes 对防止危险捷径尤其重要。

---

# 八、P-L1/P-L2 覆盖要求

`22_遗漏、反例与回归测试.md` 应维护问题宇宙覆盖矩阵。

最低要求：

- 每个 P-L1 至少存在 Synthetic Case；
- P0 P-L2 必须有直接案例；
- 高风险 P-L2 必须有 Forbidden Outcome；
- 一个完整任务案例应跨多个 P-L1，而不是只测单组件。

---

# 九、人工 Gold 与 LLM Judge 分工

- 明确结构化案例：规则 / 人工 Gold；
- 语义边界案例：人工专家 Gold + 多模型辅助；
- 大规模低风险监测：LLM Judge 可辅助；
- 高风险 merge/replaces/automation：人工复核；
- 用户问题是否真正解决：优先使用任务结果、人工判断和真实 outcome，而不是只让 LLM 自评。

任何 LLM Judge 本身也需要校准和版本记录。

---

# 十、回归触发器

以下变化应触发相关 Regression Set：

- P-L1 / P-L2 问题分类变化；
- Requirement Pattern 变化；
- Schema 变化；
- Embedding / Reranker / LLM 变化；
- Prompt / Skill 变化；
- relation taxonomy 变化；
- routing rule 变化；
- threshold 变化；
- time/version logic 变化；
- permission policy 变化；
- 用户任务主链变化。

---

# 十一、真实样本进入 Gate

进入真实样本层前必须：

- 已定义要验证的 P-L1/P-L2 或能力；
- 已通过对应 Synthetic Set；
- 已创建 Validation Sample Manifest；
- 已列出样本和读取范围；
- 已定义 allowed / prohibited operations；
- 已定义输出位置；
- 已定义停止条件。

未满足则不得默认扫描现有资料库。

---

# 十二、停止与验收原则

- 不以文件数、向量数、Wiki 页数、Skill 数或 Agent 数作为完成指标；
- 不以单次 Demo 成功作为能力通过；
- 不以组件准确率替代用户结果；
- 优先判断真实问题能否被正确理解、研究、解决、执行和验证；
- 在边际知识价值持续很低时允许停止继续研究；
- 高风险错误即使平均指标很好，也可以一票否决。

---

# 十三、一票否决候选

- 回答了错误的问题且没有发现；
- 高风险任务漏掉关键约束；
- 未经授权读取真实知识资产；
- 丢失 provenance；
- 自动删除唯一来源；
- 把条件不同的知识错误合并；
- 把弱证据自动升级为事实；
- 把高风险 AI 能力自动授权执行；
- 错误版本替代且无法回滚；
- 工具成功被误判为用户任务完成。

> **最终 Benchmark 的最高层问题始终是：系统有没有更可靠、更经济地帮助用户解决真正的问题。**
