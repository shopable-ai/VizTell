# 商业模式宇宙 Benchmark：A-E 对照、消融、错误分类与回归

> 机器清单：`../08_机器数据与Schema/benchmark_manifest_v1.json`。
>
> Benchmark 的核心问题不是“模型有没有遵守格式”，而是：**商业模式宇宙的知识、检索和 Workflow 是否对真实商业决策产生可重复的增量价值。**

---

# 一、必须回答的五个问题

1. 普通模型本身能做到什么？
2. 单个专题文档增加多少价值？
3. 整个宇宙本体增加多少价值？
4. Workflow / Retrieval / Data Gate 增加多少价值？
5. 外部研究 + 真实项目数据再增加多少价值？

如果没有 A-E 对照，就无法区分：

> “模型本来就会” 和 “商业模式宇宙让它变得更好”。

---

# 二、A-E 五组标准条件

## A. 普通模型 + 简单任务提示词

不给商业模式宇宙。

目的：建立 Base Model Baseline。

## B. 普通模型 + 单个最相关专题文件

例如 T01 只给：

> `09_专题商业模式/电子书商业模式.md`

目的：测“一个高相关长文档”本身的增量。

## C. 商业模式宇宙 + 无完整 Workflow

给相关本体知识，但不强制端到端工作流。

目的：测“知识资产”的增量。

## D. 商业模式宇宙 + 完整 Workflow

增加：

- Task Router；
- Context Builder；
- Data/Evidence Gate；
- 候选生成；
- 经济模型；
- 反方；
- 实验；
- Decision Artifact。

目的：测“组织推理过程”的增量。

## E. 宇宙 + Workflow + External Research + Project Data

增加：

- 当前市场/竞品/平台/规则；
- 真实成本；
- CAC/转化/复购；
- 合同/返点；
- Cohort；
- 项目约束。

目的：测“从通用推理到真实决策”的最后一段价值。

---

# 三、实验公平性

A-E 必须尽量控制：

- 同一基础模型；
- 同一模型版本；
- 同一温度/采样设置；
- 同一任务原始输入；
- 同一输出预算；
- 同一评分 Rubric；
- 不把 Gold Answer 泄漏给被测系统；
- 评审不知道答案来自 A/B/C/D/E（可盲评时尽量盲评）。

否则比较的是：

> 模型差异 / Prompt 长度 / 输出预算

而不一定是商业模式宇宙。

---

# 四、评分 Rubric：100 分

| 维度 | 权重 | 核心判断 |
|---|---:|---|
| 需求理解 | 7 | 是否识别真正决策，而非只复述主题 |
| 机会召回 | 8 | 是否发现主要可行机会源 |
| 隐藏利润发现 | 8 | 是否超越 SKU 毛利看到后端/条件经济/容量/现金等 |
| 上下游覆盖 | 6 | 是否看到价值链和相邻利润池 |
| 方案差异 | 6 | 候选是否结构不同，而非同一方案换折扣 |
| 经济逻辑 | 8 | 收入、成本、激励、风险是否闭环 |
| 单位经济 | 7 | 是否正确处理贡献、CAC、LTV、Payback 等 |
| Cash/Cohort/Conditional | 8 | 是否处理现金、Cohort、返点/credits/账期等 |
| 竞争与壁垒 | 6 | 是否考虑竞争反应和真实控制点 |
| 风险与失败 | 6 | 是否发现关键失效条件 |
| 事实与证据 | 8 | 事实准确、来源/时效合理 |
| 假设透明 | 5 | 是否把未知与事实分开 |
| 实验质量 | 6 | 是否能验证关键假设且有对照/阈值 |
| 可执行性 | 5 | 下一步能否执行 |
| 创新但不幻想 | 3 | 新颖性不能来自无事实支撑 |
| 遗漏控制 | 3 | 是否漏掉任务关键模块 |

总计 100。

---

# 五、惩罚项：错误但自信必须重罚

答案不能因为“提出 30 个赚钱方式”就得高分。

建议惩罚：

| 错误 | 最大扣分 |
|---|---:|
| 自信给出逻辑不成立的商业结论 | -25 |
| 虚构/过期事实冒充当前事实 | -20 |
| 重大财务/单位经济计算错误 | -15 |
| 缺真实数据却给伪精确数值 | -10 |
| 把明显违法/违规技巧当正常商业模式 | -15 |
| Benchmark Gold 泄漏/照抄 | -20 |

### 评分原则

> 8 个高质量、可验证的机会，可以高于 30 个混杂大量错误的“赚钱点子”。

---

# 六、评分不能只靠一个 Judge

建议三层：

## L1 Deterministic Checks

机器可判：

- 是否区分 Fact/Assumption；
- 是否包含真实数据门；
- 是否输出候选；
- 是否有单位经济；
- 是否有 Kill Condition；
- 是否引用不存在的 Atom/Pattern；
- 公式是否能运行；
- 路由/召回是否覆盖必需资产。

## L2 Model Judge

用于：

- 机会质量；
- 候选差异；
- 反方质量；
- 可执行性；
- 解释质量。

Model Judge 自己也要有校准集。

## L3 Human / Outcome Review

高价值任务最终需要：

- 专业人工评审；
- 或真实实验结果；
- 或业务数据。

最终目标不是“Judge 喜欢”，而是：

> 决策更好、错误更少、实验更有效。

---

# 七、Benchmark Case 的结构

每个 Case 至少包含：

```yaml
id:
name:
query:
decision_required:
input_assets:
known_facts:
unknowns:
real_data_fields:
required_capabilities:
forbidden_assumptions:
critical_failure_modes:
rubric_overrides:
gold_evidence_notes:
quality_status:
```

Gold 不应是一篇固定“标准答案”。

更合适的是：

> **Gold Requirements + Gold Evidence + Critical Omissions + Invalid Claims**

因为商业问题可能存在多个合理方案。

---

# 八、Benchmark Quality Gate

新增 `B1 Benchmark Failure`，避免测试本身污染结论。

每个题进入正式回归前检查：

## Q1 是否欠定义？

任务是否缺少模型合理无法推断的必要条件？

## Q2 是否过度限制？

评分是否要求某个唯一措辞/唯一方案，而任务其实允许多种正确答案？

## Q3 覆盖是否不足？

一个明显不完整答案是否也可能通过？

## Q4 Prompt 是否误导？

提示词与评分要求是否冲突？

## Q5 Gold 是否泄漏？

被测条件是否已经包含 Gold 中才应验证的答案？

## Q6 是否可区分能力？

A-E 是否全部轻易满分，或全部失败？如果是，题目没有测量价值。

## Q7 是否存在时效污染？

当前平台费率/法规类事实必须绑定 `as_of_date`，否则回归会被时间变化误判。

---

# 九、Ablation：哪些资产真的有用

完整 D/E 系统跑出结果后，逐个移除：

```text
Atom
Pattern
Product Role / Offer
Opportunity Lens
Value Chain / Ecosystem
U19 / Real Economics / Cohort
Topic / Case
External Research
Counterargument / Failure
Experiment Layer
```

重新运行。

### 需要记录的不只是总分

例如移除 U19 后：

- 总分下降 4；
- 但 Hidden Profit 下降 12；
- Financial Error +2；
- 对“返点型业务”下降 20；
- 对普通 SaaS 几乎不变。

这样的结果才有意义。

---

# 十、Asset Contribution Matrix

长期应形成：

| Asset | T01 | T02 | T03 | … | 平均增量 | 特定任务增量 | 使用率 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Atom |  |  |  |  |  |  |  |
| Pattern |  |  |  |  |  |  |  |
| Product Role |  |  |  |  |  |  |  |
| U19 |  |  |  |  |  |  |  |
| Value Chain |  |  |  |  |  |  |  |
| Cases |  |  |  |  |  |  |  |

这样可以发现：

- 高价值资产；
- 低使用资产；
- 只对某类任务有价值的资产；
- “文件很多但几乎无增量”的资产。

低贡献不等于删除，先判断：

> 没价值，还是 R1/W1 导致没被正确使用？

---

# 十一、Retrieval Benchmark 单独评测

不要把 Retriever 和 Generator 混成一个分数。

至少记录：

## Route Accuracy

任务族/旗标是否正确。

## Domain Recall

需要的 U 域是否被覆盖。

## Asset Recall

关键横向文件/专题是否召回。

## Atom Recall@K

Gold/专家标注的关键 Atom 是否进入 Top-K。

## Pattern Recall@K

关键 Pattern 是否进入 Top-K。

## Context Precision

加载的内容有多少真正用于决策。

## Context Cost

Token/字符/延迟/检索成本。

这允许：

> Generator 答案失败 → 先看 Retriever 是否真的给过相关知识。

---

# 十二、Context Ablation

同一知识资产还需要测试：

- Top-5 vs Top-10 vs Top-20；
- 只 BM25；
- 只 Embedding；
- Hybrid；
- Hybrid + Rerank；
- Full Universe；
- Minimum Sufficient Context。

核心问题：

> **更多上下文是否真的更好？**

如果 Full Universe 反而使遗漏/混淆增加，就不应以“上下文窗口够大”为理由全塞。

---

# 十三、Regression

每次修改：

```text
Knowledge / Router / Retrieval / Workflow / Schema
↓
Deterministic Validation
↓
Active Benchmark Set
↓
与上一个 Baseline 比较
↓
Case-level Regression Check
↓
Ablation Sanity Check
↓
通过 → 更新基线
失败 → 错误分类 → 修复
```

### 不能只看平均分

例如：

> 新版本平均 +3，但 T04 返点业务 -18。

这不能自动视为通过。

至少检查：

- 平均；
- 最差 Case；
- 每个核心任务族；
- 特定高风险任务；
- 错误率；
- 成本。

---

# 十四、重复运行与统计不确定性

生成模型有随机性。

正式比较建议：

- 每个条件重复 3-10 次；
- 同时报告均值/中位数；
- 报告方差或区间；
- 记录模型版本与日期；
- 不用单次极好答案证明提升。

高成本任务可以先跑少量 Canary，只有发现信号再扩大。

---

# 十五、当前仓库内置 Harness 测什么

`../../scripts/benchmark_business_model_universe.py` 的第一版只承担确定性基线：

1. v4 稳定资产和 ID 数量没有丢；
2. Task Router 能否把 T01/T02 路由到正确任务族；
3. Cross-cutting Flags 是否触发；
4. 必需 U 域是否进入候选；
5. 必需知识资产是否进入最小上下文；
6. 静态上下文是否超过预算；
7. 基础 Atom/Pattern 可否加载并产生 Top-K；
8. 检索层消融是否能看到 coverage 下降。

它**不负责冒充 A-E 商业答案质量评测**。

A-E 的真正数值需要：

- 模型 Runner；
- 隔离条件；
- 输出保存；
- Judge/Human；
- 多次运行。

---

# 十六、第一阶段通过条件

当前最小闭环通过要求：

- v4 结构完整性继续通过；
- T01/T02 Route 正确；
- 必需资产 Recall = 100%；
- 必需 Domain Recall = 100%；
- 静态 Knowledge Context 不全库加载；
- Harness Score ≥ 90；
- 输出明确“这是运行时 Harness 分数，不是商业答案分数”；
- GitHub 回归 Workflow 能在 `main` 执行。

---

# 十七、研究方法依据

本评测体系吸收以下方法思想：

- 真实任务比纯格式测试更能衡量实际价值；
- 评分需要层次化 Rubric；
- Retriever 与 Generator 应分开诊断；
- Benchmark 自身需要质量审计；
- 随机模型的单次结果不应当作稳定提升。

参考：

- https://evals.openai.com/
- https://openai.com/index/separating-signal-from-noise-coding-evaluations/
- https://arxiv.org/abs/2309.15217
- https://arxiv.org/abs/2307.03172
