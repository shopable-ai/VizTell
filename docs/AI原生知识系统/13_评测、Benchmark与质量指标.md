# 评测、Benchmark 与质量指标

> 目标：避免“已建库／已向量化／已生成 Skill／Agent 跑了一次”被误认为完成。所有关键能力都需要可测、可回归、可解释。

当前阶段优先：

> **Synthetic Benchmark → Schema Validation → Framework Regression**

真实资料 Benchmark 受 `21_验证计划、样本清单与数据边界.md` 约束。

## 0. 本文件与 P-L1 / P-L2 的正式边界

`01_需求宇宙.md` 现在只保存用户与知识使用过程中的专业问题。

以下内容**不再创建 P-L2**，统一由本文件和 `22_遗漏、反例与回归测试.md` 承担：

- false merge / false split；
- false novelty；
- 来源、证据、引用判断错误；
- 学习建议错误；
- 委托 / 人机分工建议错误；
- 实现路由错误；
- Agent over-routing / Software over-productization；
- 模型、检索或批处理成本失控；
- AI 大规模处理把错误判断规模化放大。

正式关系：

```text
用户能感知的后果
→ 01A / 01B / 01

系统内部为什么判错、错率多少、成本多少
→ 13 / 22
```

---

## 一、评测必须分层

### 1.1 Problem-level：用户问题层

首先评测：

- 是否理解用户真正的问题；
- 是否把范围界定正确；
- 是否发现真正需要的知识；
- 是否遗漏关键未知；
- 是否在应该停止研究时停止；
- 最终结果是否帮助理解、判断、学习、决策或行动。

### 1.2 Capability-level：系统能力层

评测：

- 检索；
- 多来源综合；
- 证据判断；
- 去重与增量；
- 学习与委托路由；
- 决策支持；
- 变化监测；
- 结果验证。

### 1.3 Component-level：知识工程与实现组件层

评测：

- Source / provenance；
- Atom / Canonical / Relation；
- Schema；
- Routing object；
- Retrieval / RAG；
- Skill / Workflow / Agent；
- 权限、版本、回滚等。

> **组件准确不等于用户问题解决。**

### 1.4 Outcome-level：用户结果层

最终还必须观察：

- 用户是否更快完成任务；
- 是否减少无效阅读；
- 是否降低错误；
- 是否形成真正掌握；
- 是否改善决策和行动结果；
- 是否能长期重新找到、重新判断和更新。

---

## 二、Benchmark 六层结构

### B0 Schema / Invariant

测试字段、required、ID、enum 和不允许的状态组合。

### B1 Synthetic Component

人工构造答案明确的：

- 等价；
- 新条件；
- 新边界；
- 冲突；
- 伪多源；
- 主体价值；
- 学习差额；
- 委托边界；
- 实现路由。

### B2 Synthetic Problem / Task

测试：

- 是否抓住真实问题；
- 是否识别知识需求；
- 是否选择正确研究路径；
- 是否保留条件与冲突；
- 是否形成有效方案；
- 是否在足够时停止；
- 是否真正回答用户最初的问题。

### B3 Controlled Real Sample

使用 Manifest 明确的小样本验证真实噪声、表达变化和数据复杂度。

### B4 Scale / Performance

测试：

- recall / precision；
- latency；
- cost；
- candidate explosion；
- 人工复核量；
- 增量吞吐；
- 大规模错误放大。

### B5 Outcome / Longitudinal

测试长期结果：

- 是否改善项目决策；
- 是否减少无效阅读与重复学习；
- 是否提高人工能力；
- 是否减少错误；
- 是否更快推进任务；
- 是否能稳定更新；
- 委托或自动化是否降低总成本且不削弱必要人工能力。

---

## 三、Problem-level 核心指标

### 3.1 问题理解

- true-problem identification rate；
- wrong-problem answer rate；
- scope error rate；
- missed constraint rate；
- success-criteria completeness。

### 3.2 知识需求

- critical knowledge need recall；
- prerequisite gap recall；
- irrelevant research rate；
- unknown-unknown discovery rate；
- unnecessary information expansion rate。

### 3.3 研究与综合

- critical source miss rate；
- redundant reading / processing rate；
- condition/boundary preservation rate；
- unresolved conflict preservation；
- decision-changing increment recall；
- research stop accuracy。

### 3.4 用户结果

- answer usefulness；
- decision support quality；
- actionability；
- task progress impact；
- time saved；
- avoided attention waste；
- downstream correction rate；
- user outcome success rate。

---

## 四、知识工程核心质量指标

### 4.1 Canonical / 去重

- duplicate candidate recall；
- false merge rate；
- missed equivalence rate；
- wrong alias rate；
- condition/boundary preservation rate；
- provenance retention rate。

### 4.2 增量

- new mechanism recall；
- new condition recall；
- new boundary recall；
- new counterexample recall；
- new independent evidence recall；
- decision-changing increment recall；
- false novelty rate。

### 4.3 Evidence

- primary source tracing accuracy；
- evidence independence accuracy；
- source fidelity error rate；
- weak-evidence-as-fact rate；
- citation correctness；
- conflict preservation rate；
- unsupported upgrade rate。

### 4.4 Retrieval / RAG

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

### 4.5 Subject Value / Learning / Delegation

- high-value miss rate；
- low-value attention waste；
- false human-learning recommendation；
- false delegation recommendation；
- missing human-judgment requirement；
- existing-tool/service miss rate；
- capability-degradation risk miss。

### 4.6 Learning

- delayed recall；
- concept discrimination；
- boundary recognition；
- standard execution；
- edge-case adaptation；
- cross-context transfer；
- confidence calibration；
- real-task performance。

### 4.7 Lifecycle / Governance

- stale detection latency；
- impacted-object recall；
- local update correctness；
- version lineage completeness；
- rollback success；
- human takeover success；
- unauthorized-action rate；
- audit completeness。

### 4.8 Implementation Routing

- unnecessary RAG rate；
- Agent over-routing rate；
- Software over-productization rate；
- existing-tool miss rate；
- unstable-workflow automation rate；
- cost / latency regression；
- failure-detection rate；
- recovery success rate。

---

## 五、Error Taxonomy

### 5.1 Problem Errors

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

### 5.2 Knowledge / Evidence Errors

- false merge；
- false split；
- false novelty；
- missed boundary；
- missed counterexample；
- false conflict；
- conflict collapse；
- source lineage collapse；
- stale knowledge served；
- citation mismatch；
- weak evidence upgraded to fact；
- lost provenance。

### 5.3 Learning / Delegation Errors

- high-value knowledge ignored；
- low-value knowledge interrupts human；
- human-learning overinvestment；
- human-learning underinvestment；
- unsafe delegation；
- missing human verification；
- critical capability degradation。

### 5.4 Implementation / Runtime Errors

- wrong implementation routing；
- Agent over-routing；
- Software over-productization；
- automation overreach；
- model / retrieval cost explosion；
- batch error amplification；
- unauthorized action；
- irreversible wrong action。

不同错误必须有 severity，不得只看平均准确率。

---

## 六、Benchmark Case 必须有 Forbidden Outcomes

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

---

## 七、P-L1/P-L2 覆盖要求

`22_遗漏、反例与回归测试.md` 维护 17 个 P-L1 的问题覆盖矩阵，同时另设 System Error 回归。

最低要求：

- 每个 P-L1 至少存在 Synthetic Case；
- 高优先 P-L2 必须有直接案例；
- 高风险 P-L2 必须有 Forbidden Outcome；
- 完整任务案例应跨多个 P-L1；
- Implementation Case 不得伪装成 P-L1 覆盖。

---

## 八、人工 Gold 与 LLM Judge 分工

- 明确结构化案例：规则 / 人工 Gold；
- 语义边界案例：人工专家 Gold + 多模型辅助；
- 大规模低风险监测：LLM Judge 可辅助；
- 高风险 merge / replaces / delegation / automation：人工复核；
- 用户问题是否真正解决：优先任务结果、人工判断和真实 outcome，而不是只让 LLM 自评。

---

## 九、回归触发器

以下变化应触发相关 Regression Set：

- P-L1 / P-L2；
- SUP；
- Requirement Pattern；
- Schema；
- Embedding / Reranker / LLM；
- Prompt / Skill；
- relation taxonomy；
- learning / delegation rule；
- implementation routing rule；
- threshold；
- time/version logic；
- permission policy；
- 用户任务主链。

---

## 十、真实样本进入 Gate

进入真实样本层前必须：

- 已定义要验证的问题或能力；
- 已通过对应 Synthetic Set；
- 已创建 Validation Sample Manifest；
- 已列出样本和读取范围；
- 已定义 allowed / prohibited operations；
- 已定义输出位置；
- 已定义停止条件。

未满足则不得默认扫描现有资料库。

---

## 十一、停止与验收原则

- 不以文件数、向量数、Wiki 页数、Skill 数或 Agent 数作为完成指标；
- 不以单次 Demo 成功作为能力通过；
- 不以组件准确率替代用户结果；
- 优先判断真实问题能否被正确理解、研究、解决、执行和验证；
- 在边际知识价值持续很低时允许停止继续研究；
- 高风险错误即使平均指标很好，也可以一票否决。

> **P-L1/P-L2 负责“有哪些问题”，13/22 负责“系统会怎样把这些问题解决错”。**
