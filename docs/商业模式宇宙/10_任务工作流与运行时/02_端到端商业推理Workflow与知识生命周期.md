# 端到端商业推理 Workflow、可观测性与知识生命周期

> 机器对应：`../08_机器数据与Schema/commercial_reasoning_runtime_v1.json`。
>
> 本文件的目标不是重复 v2/v3/v4 Skill，而是把现有知识与 Skill **装配成端到端运行协议**。

---

# 一、标准总链

```text
Task Intake
→ Task Router
→ Project Signature
→ Data / Evidence Gate
→ Information Gap
→ Context Builder
→ External Research（按需）
→ Opportunity / Gap Scan
→ U01-U27 Domain Scan（按需）
→ Atom Retrieval
→ Pattern Retrieval
→ Product Role / Price / Offer（按需）
→ Value Chain / Profit Pool / Ecosystem
→ Conditional Economics / Accounting Truth
→ Candidate Generation
→ Unit / Basket / Cohort / Cashflow
→ Competition / Moat / Risk / Counterargument
→ Experiment
→ Rank / Kill / Scale
→ Decision Artifact
→ Trace
→ Benchmark / Error Classification
→ Knowledge Feedback / Lifecycle
```

这不是一条必须每次全部执行的流水线。

正确理解是：

> **固定主骨架 + 条件模块 + 回退/扩检索 + 数据门 + 验收关口。**

---

# 二、S01 Task Intake：先定义决策，不先给答案

至少抽取：

```yaml
user_goal:
decision_to_make:
object:
scope:
time_horizon:
constraints:
success_criteria:
explicit_non_goals:
```

关键区别：

- “研究 AI API 商业模式”是主题；
- “决定免费额度和 Commit 怎样设计，避免负毛利”才是决策。

如果只有主题，没有决策，Workflow 应先生成：

> 可能的决策树 + 当前最有价值的决策问题。

---

# 三、S02 Task Router

使用 `task_router_v1.json`：

```text
Query
→ Primary Family
→ Alternate Routes
→ Cross-cutting Flags
→ Primary Domains
→ Required Knowledge Assets
```

如果多个任务混合，例如：

> “低价引流以后怎样提高复购，还想看供应商返点？”

可以输出：

```yaml
primary_family: pricing_offer_portfolio
secondary_family: growth_retention_ltv
flags:
  - low_price_entry
  - conditional_economics
```

不要因为存在多个意图就直接退化成全库加载。

---

# 四、S03 Project Signature

复用现有 `business_model_signature_v4.schema.json`。

本阶段先建立当前项目的最小 Signature：

- Actor / Payer / User / Beneficiary；
- Problem / Job；
- Current Offer；
- Delivery；
- Revenue / Costs；
- Channel；
- Constraints；
- Known Evidence；
- Existing Atoms/Patterns（如已知）。

对于“已有业务优化”，Current-state Signature 是强制项。

对于“从0设计”，Current-state 可以是：

> 当前替代方案 / 客户今天怎样解决 / 没有产品时的行为。

---

# 五、S04 Data / Evidence Gate

建立四张表：

## A. Known Facts

已经有可靠证据的事实。

## B. Project Data

真实业务参数。

## C. Unknowns

当前无法知道的内容。

## D. Research Questions

可以通过外部资料、访谈、实验或数据库补齐的问题。

任何候选方案如果关键收益依赖 Unknown：

> 必须把 Unknown 变成 Assumption，并进入实验或敏感性分析。

---

# 六、S05 Information Gap 与 External Research

先问：

> **为了做这个决策，真正还缺什么？**

而不是泛搜一堆资料。

信息缺口按价值排序：

1. 会改变候选方向的事实；
2. 会改变单位经济正负的参数；
3. 会触发法律/平台/合同不可行的约束；
4. 会改变竞争反应的事实；
5. 只是增加背景知识但不改变决策的信息。

优先研究 1-4。

---

# 七、S06 Context Builder

运行协议：

```text
Primary Family
+
Flags
+
Project Signature
↓
Relevant Domains
↓
Top Atoms
↓
Top Patterns
↓
Horizontal Assets
↓
Topic / Case
↓
Rerank / Deduplicate
↓
Minimum Sufficient Context
```

### 扩检索触发条件

- 关键问题没有机制解释；
- 需要的 U 域不在路由结果；
- 候选方案高度同质；
- 反方审计发现遗漏；
- Benchmark 暴露 R1；
- 外部事实与知识库冲突。

### 停止扩检索条件

- 主要决策变量已经覆盖；
- 新增上下文只产生同义建议；
- 关键限制已经由真实数据而非更多知识决定；
- Context Precision 明显下降。

---

# 八、S07 Opportunity / Gap Scan

复用 `01/06_机会来源_差异捕获与商业模式变换算子.md`。

输出不只是“赚钱方式”，而是：

```yaml
opportunity_source:
observed_gap_or_mismatch:
customer_value_created:
transformation_operator:
who_benefits:
who_pays:
why_now:
required_atom_or_pattern:
profit_pool:
main_risk:
evidence_state:
```

如果一个机会只有：

> “这里价格低，那里价格高”

但没有持续客户价值、交易结构、风险与可持续捕获方式，则不应升级为商业模式候选。

---

# 九、S08 Structure Analysis

这一层把机会放回完整系统。

至少检查：

## Value Chain

- 原料/内容/技术/供给；
- 生产/加工；
- 聚合；
- 分发；
- 交易；
- 履约；
- 售后；
- 数据/金融/基础设施。

## Profit Pool

- 哪一环节收入大；
- 哪一环节贡献利润大；
- 哪一环节资本占用高；
- 哪一环节风险被低估；
- 哪一环节拥有客户/数据/标准/分发。

## Ecosystem

- 参与方；
- 直接交换；
- 间接交换；
- 补贴方向；
- 规则制定者；
- 风险承担者；
- 绕平台路径。

## Control Points

- 客户关系；
- 标准；
- 数据；
- 稀缺供给；
- 牌照；
- 网络；
- 分发；
- 资本；
- IP；
- Switching Cost。

---

# 十、S09 Candidate Generation

默认生成 3-7 个**结构差异明显**的候选。

禁止：

> 方案 A 打九折；方案 B 打八折；方案 C 打七折。

候选差异至少来自一个结构变量：

- 谁付款；
- 卖什么权利；
- 谁拥有资产；
- 谁承担风险；
- 收入来自哪里；
- 定价计量；
- 渠道；
- 前端与后端关系；
- 订阅/交易/结果/分成；
- 平台/直营/经纪；
- 自营/伙伴；
- 现金流/合同；
- 条件性经济。

每个候选都记录 `mechanism_trace`：

```text
Opportunity Source
→ Atoms
→ Patterns
→ Product Roles（如适用）
→ Profit Pool
→ Economics
```

这样消融时才能知道候选依赖了哪些资产。

---

# 十一、Offer / Product Role / Price 是条件模块

只有这些任务强制进入：

- 定价；
- 低价/免费；
- Entry Offer；
- 商品组合；
- Upsell/Cross-sell；
- 订阅/会员；
- Next-best Offer。

执行：

```text
Product Role
→ Price Architecture
→ Offer Nodes
→ Conditional Edges
→ Context Router
→ Front-end/Basket/Cohort
→ Incrementality Guardrail
```

一个“价值链纵向整合”问题可以不生成 Offer Graph。

---

# 十二、S10 Economics：所有方案必须落回真实经济

按适用范围计算：

## Front-end

```text
成交收入
- COGS
- 履约
- 支付
- 促销增量成本
- 支持
= Front-end Contribution
```

## Basket

```text
Front-end
+ Add-on
+ Upsell
+ Cross-sell
+ Same-session Service
+ Order-level Conditional Funding
= Basket Contribution
```

## Cohort

```text
Basket
+ Repeat
+ Subscription / Membership
+ Backend
+ Referral
+ Reactivation
+ Verified Rebate / MDF / Credits
+ Capacity / Spoilage Value
- CAC
- Service
- Refund
- Abuse
- Financing
- Clawback
= True Cohort Contribution
```

## Cashflow

同时检查：

- 收钱时间；
- 付款时间；
- Deferred obligation；
- 应收；
- 库存；
- 账期；
- CapEx；
- Working Capital。

## Scenario

缺真实参数时至少：

> Conservative / Base / Upside

并做最敏感 3-5 个变量。

---

# 十三、S11 Strategy / Competition / Counterargument

每个候选必须回答：

1. 如果有效，竞争者会怎么反应？
2. 供应商会不会涨价/绕过？
3. 客户会不会套利/多归属？
4. 渠道会不会冲突？
5. 低价会不会蚕食原价？
6. 增长是否需要越来越高补贴？
7. 壁垒是真壁垒还是暂时红利？
8. 规模增加后单位经济变好还是变坏？
9. 哪个假设一旦错，整个模型失效？

强制输出：

```yaml
best_counterargument:
most_likely_failure_mode:
competitive_response:
fragile_assumptions: []
```

---

# 十四、S12 Experiment / Rank / Kill / Scale

不是“先做再看”。

每个高不确定候选至少定义：

```yaml
hypothesis:
critical_metric:
baseline:
treatment:
control_or_counterfactual:
window:
budget_cap:
pass_condition:
kill_condition:
scale_condition:
```

### Kill Condition 特别重要

示例：

- 90 天 True Cohort Contribution 持续为负；
- 入口优惠带来的 70% 用户是本来会全价买的客户；
- 退款/薅羊毛超过阈值；
- 推理成本使高用量用户贡献为负；
- 供应商返点必须达到极高门槛才能盈利且概率低；
- 合规/平台政策使模式不可持续。

---

# 十五、S13 Decision Artifact

最终交付不是“商业模式列表”，而是决策文件。

至少有：

```text
1. 要做的决策
2. 关键事实
3. 关键未知
4. 当前结构/问题
5. 候选方案
6. 经济模型
7. 条件经济
8. 风险/竞争/反方
9. 关键假设
10. 实验与Kill
11. 排序/淘汰
12. 下一步
```

如果数据不足以选唯一方案，可以给：

> **条件式决策树**

而不是为了“给结论”伪造确定性。

---

# 十六、Trace 与 Observability

每次 Workflow 运行必须能回答：

- 为什么路由到这个任务族？
- 为什么加载这些 U 域？
- 哪些 Atom/Pattern 被召回？
- 哪些实际进入了方案？
- 哪些知识加载了但没有使用？
- 真实数据缺什么？
- 哪些结论依赖假设？
- 哪些外部来源被使用？
- Context 大小是多少？
- 错误发生在哪一层？

未来应统计：

```text
Asset Usage Rate
Asset Unique Contribution
Retrieval Recall
Context Precision
Average Context Cost
Route Accuracy
Candidate Diversity
Financial Error Rate
Evidence Error Rate
Regression Rate
```

这些指标比“仓库有多少 Markdown”更能判断系统是否进步。

---

# 十七、错误分类与修复路径

## K1 Knowledge Gap

修复：研究机制 → 判断是否新 Atom/Pattern/专题/案例。

## R1 Retrieval Failure

修复：关键词、别名、metadata、BM25、embedding、rerank、domain route。

## W1 Workflow Failure

修复：模块顺序、强制关口、条件分支、输出契约。

## C1 Context Failure

修复：减少噪声、提高 top-K、重排、补上下文、解决冲突。

## E1 Evidence Failure

修复：来源、时间、证据等级、Fact/Assumption 分离、freshness。

## F1 Financial Failure

修复：公式、会计口径、数据类型、单位、现金/收入/贡献分离。

## S1 Strategy Failure

修复：竞争反应、多方激励、壁垒、替代方案和反方审计。

## T1 Tool Failure

修复：工具重试、降级策略、数据源替代、错误显式化。

## O1 Output Failure

修复：Decision Artifact、优先级、Next Action、摘要与附录分离。

## B1 Benchmark Failure

修复 Benchmark 本身，而不是“训练系统适应错误题”。

---

# 十八、知识反馈 Router

真实任务出现新发现时：

```text
New Finding
↓
已有 Atom？ ─ 是 → 补证据/别名/关系，不新建
↓ 否
已有 Pattern？ ─ 是 → 补实例/边界，不新建
↓ 否
只是已有 Atom 的新组合？ ─ 是 → Candidate Pattern / Case
↓ 否
只是行业实例？ ─ 是 → 04 案例
↓ 否
只是证据？ ─ 是 → Case/Evidence/90 Source
↓ 否
只是专题知识？ ─ 是 → 09 专题
↓ 否
只是时效规则？ ─ 是 → Freshness asset / 外部事实层，不进稳定本体
↓ 否
跨行业可迁移且无法由现有机制表达？ ─ 是 → Candidate Atom/Pattern
```

---

# 十九、知识生命周期

新增对象默认不能直接 `stable`。

## `candidate`

刚发现，尚未证明需要独立对象。

## `experimental`

已经有多个任务出现，正在测试是否可复用。

## `verified`

证据与 Benchmark 表明它有独立贡献。

## `stable`

进入长期稳定接口；ID 不轻易改变。

## `deprecated`

仍兼容，但不再推荐新任务使用。

## `superseded`

被更准确对象替代，保留映射。

## `historical`

只用于历史解释，不进入当前默认检索。

### 时效知识额外字段

```yaml
valid_from:
valid_to:
as_of_date:
source:
freshness_class:
recheck_trigger:
```

平台规则、费率、促销、法规不能与“订阅”“Marketplace”这样的稳定机制采用同一生命周期。

---

# 二十、版本升级规则

只有满足以下条件之一，才值得升级运行时或本体版本：

1. Benchmark 显示稳定提升；
2. 修复高频 K/R/W/C/E/F/S 类失败；
3. 新对象在多个真实任务中证明不可被旧对象表达；
4. 新 Schema 解决了真实数据/决策表达问题；
5. 有明确 Migration / Regression 计划。

不应该因为：

- 文档变长；
- Pattern 数增加；
- 新增了几个名词；

就宣称系统升级。

---

# 二十一、长期闭环

最终运行循环固定为：

```text
知识
→ Workflow
→ 真实任务
→ Trace
→ Benchmark
→ 错误分类
→ 根因
→ 修知识/检索/流程/数据/测试
→ Regression
→ 新一轮真实任务
→ 知识反馈
→ 生命周期与版本治理
```

这才是“商业模式宇宙”从知识本体进入商业推理系统阶段的核心变化。
