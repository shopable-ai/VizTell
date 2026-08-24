# 端到端商业推理 Workflow、可观测性与知识生命周期

> 机器对应：`../08_机器数据与Schema/commercial_reasoning_runtime_v1.json`。
>
> 本文件是**后台运行时协议**，负责把 Router、Retriever、商业模式宇宙、经济性、Trace、Benchmark 与知识生命周期装配起来。
>
> 普通创业者和业务人员的默认入口已经迁移到：
>
> [`项目商业推理工作流/00_总览_怎样使用项目商业推理工作流.md`](./项目商业推理工作流/00_总览_怎样使用项目商业推理工作流.md)
>
> 人工业务主干见：
>
> [`项目商业推理工作流/01_P01-P20项目商业推理总工作流.md`](./项目商业推理工作流/01_P01-P20项目商业推理总工作流.md)

---

# 一、标准总链：中文业务含义 + 后台英文节点

## 1. 完整中文对应

```text
任务接收
→ 任务路由
→ 建立项目商业画像
→ 真实数据与证据门
→ 识别高价值信息缺口
→ 构建最小充分上下文
→ 按需研究外部现实市场
→ 扫描机会、错配与未满足价值
→ 按需扫描 U01-U27 设计域
→ 检索原子机制
→ 检索组合模式
→ 按需调用商品角色、价格架构与 Offer
→ 分析价值链、利润池与生态
→ 分析条件性经济与真实会计口径
→ 生成结构不同的候选商业方案
→ 计算单次交易、订单、用户群与现金流经济性
→ 分析竞争、壁垒、风险与最强反方观点
→ 设计最小实验
→ 排序、淘汰与扩大
→ 形成商业决策输出
→ 记录推理与证据轨迹
→ Benchmark / 错误分类
→ 知识反馈与生命周期治理
```

## 2. 对应后台节点名

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

两条链一一对应。中文链用于人工理解，英文节点名用于机器协议、Schema、Trace 和兼容既有 runtime-v1。

这不是每次必须跑全的流水线，而是：

> **固定主骨架 + 条件模块 + 回退/扩检索 + 数据门 + 验收关口。**

业务层怎样按现实输入跳转，由 `项目商业推理工作流/02_真实项目与现实输入入口.md` 决定。

---

# 二、S01 任务接收（Task Intake）：先定义决策

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

“研究 AI API 商业模式”只是主题；“决定免费额度、Commit、Overage 怎样设计，避免高用量用户造成负毛利”才是可执行决策。

如果只有主题，先生成可能决策树，并选当前最有价值的决策问题。

---

# 三、S02 任务路由（Task Router）

复用 `../08_机器数据与Schema/task_router_v1.json`：

```text
Query
→ Primary Family
→ Alternate Routes
→ Cross-cutting Flags
→ Primary Domains
→ Required Knowledge Assets
```

多个意图可以有 primary / secondary family 和 flags，但不能因此退化成全库加载。

人工输入类型与 P01-P20 起点，以业务目录 `02_真实项目与现实输入入口.md` 为准；后台 Router 是实现机制，不替代人工业务入口。

---

# 四、S03 项目商业画像（Project Signature）

复用 `business_model_signature_v4.schema.json`，至少覆盖：

- Actor / Payer / User / Beneficiary；
- Problem / Job；
- Current Offer；
- Delivery；
- Revenue / Costs；
- Channel；
- Constraints；
- Known Evidence；
- Existing Atoms/Patterns（如已知）。

已有业务必须建立 Current State；从 0 设计时 Current State 可以是客户今天的替代方案。

人工输出应优先使用“项目商业画像/项目商业特征”，不要把 `Project Signature` 生硬翻成“项目签名”。

---

# 五、S04 真实数据与证据门（Data / Evidence Gate）

统一分四类：

```text
Known Facts：有可靠证据的事实
Project Data：当前项目真实经营参数
Unknowns：当前不知道的内容
Research Questions：可通过研究、访谈、数据或实验补齐的问题
```

业务层进一步区分：

```text
Fact / Inference / Assumption / Unknown
```

任何候选如果关键收益依赖 Unknown，必须转成 Assumption，并进入实验、情景或敏感性分析。

---

# 六、S05 高价值信息缺口与外部研究

先问：

> **为了做当前决策，真正还缺什么？**

优先级：

1. 会改变候选方向的事实；
2. 会改变单位经济正负的参数；
3. 会触发法律、平台、合同不可行的约束；
4. 会改变竞争反应或证据评级的事实；
5. 只增加背景、不会改变决策的信息。

优先研究 1-4。市场研究具体业务规则见 `项目商业推理工作流/03_市场研究_成功失败与证据判断.md`。

---

# 七、S06 最小充分上下文（Context Builder）

```text
Primary Family
+ Flags
+ Project Signature
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

## 扩检索触发

- 关键问题没有机制解释；
- 必需 U 域不在初次路由；
- 候选高度同质；
- 反方审计发现遗漏；
- Benchmark 暴露 R1；
- 外部事实与知识库冲突。

## 停止扩检索

- 主要决策变量已经覆盖；
- 新上下文只产生同义建议；
- 决策已经受真实数据约束；
- Context Precision 开始下降。

---

# 八、S07 机会与错配扫描（Opportunity / Gap Scan）

复用 `../01_核心机制与组合模式/06_机会来源_差异捕获与商业模式变换算子.md`。

输出至少包含：

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

只有价差而没有持续客户价值、交易结构、风险和可持续价值捕获，不能升级为正式候选。

---

# 九、S08 结构分析（Value Chain / Profit Pool / Ecosystem）

## 价值链

检查原料/内容/技术/供给、生产/加工、聚合、分发、交易、履约、售后，以及数据/金融/基础设施。

## 利润池

检查收入、真实贡献、资本占用、隐藏风险，以及谁控制客户、数据、标准、分发、稀缺供给或合同。

## 生态

检查参与方、直接/间接交换、补贴方向、规则制定者、风险承担者和绕平台路径。

## 控制点

检查客户关系、标准、数据、稀缺供给、牌照、网络、分发、资本、IP、Switching Cost。

业务层的详细人工方法见 `项目商业推理工作流/04_利润池_上下游与相邻机会.md`。

---

# 十、S09 候选生成（Candidate Generation）

后台可广扫，但人工最终只保留 3-5 套结构明显不同的候选。

候选差异至少来自：

- 付款方；
- 卖的权利/结果；
- 资产所有权；
- 风险承担；
- 收入来源；
- 定价计量；
- 渠道；
- 前后端关系；
- 订阅/交易/结果/分成；
- 平台/直营/经纪；
- 自营/伙伴；
- 现金流/合同；
- 条件性经济。

记录 `mechanism_trace`：

```text
Opportunity Source
→ Atoms
→ Patterns
→ Product Roles（按需）
→ Profit Pool
→ Economics
```

这样才能做消融和知识贡献判断。

---

# 十一、商品角色 / 价格 / Offer 是条件模块

这些任务强制进入：

- 定价；
- 免费/低价；
- Entry Offer；
- 商品组合；
- Upsell/Cross-sell；
- 订阅/会员；
- Next-best Offer。

后台：

```text
Product Role
→ Price Architecture
→ Offer Nodes
→ Conditional Edges
→ Context Router
→ Front-end / Basket / Cohort
→ Incrementality Guardrail
```

人工层统一转译成“卖什么、谁买、为什么买、怎样收费、前后端怎样连接”。

---

# 十二、S10 真实经济性（Economics）

## 前端贡献

```text
成交收入
- COGS
- 履约
- 支付/渠道
- 促销增量成本
- 支持/退款
= Front-end Contribution
```

## 订单贡献

```text
Front-end
+ Add-on
+ Upsell
+ Cross-sell
+ Same-session Service
+ 已确认 Order-level Conditional Funding
= Basket Contribution
```

## 用户群真实贡献

```text
Basket
+ Repeat
+ Subscription / Membership
+ Backend
+ Referral / Reactivation
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

## 现金流

检查收钱/付款时间、Deferred Obligation、应收、库存、账期、CapEx、Working Capital。

缺真实参数时使用 Conservative / Base / Upside，并做最敏感变量和 Break-even；不得因为缺数据停止，也不得伪造精确 LTV。

---

# 十三、S11 战略、竞争与最强反方

每个重要候选至少回答：

1. 竞争者会怎样反应？
2. 供应商会不会涨价或绕过？
3. 客户会不会套利/多归属/绕过？
4. 渠道会不会冲突或改规则？
5. 低价会不会蚕食原价？
6. 增长是否需要越来越高补贴？
7. 壁垒是真壁垒还是暂时红利？
8. 规模增加后单位经济变好还是变坏？
9. 哪个假设一旦错，整个模型失效？

```yaml
best_counterargument:
most_likely_failure_mode:
competitive_response:
fragile_assumptions: []
```

---

# 十四、S12 实验、排序、淘汰与扩大

高不确定候选至少定义：

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

Kill 可以针对价格、渠道、用户群、后端或整套方案，不等于“整个项目永远失败”。

人工层统一使用 A-E 商业验证等级和 First / Second / Third / 暂不推荐输出，见 `项目商业推理工作流/06_竞争风险_证据评级与排序.md`。

---

# 十五、S13 商业决策输出（Decision Artifact）

最终交付不是“商业模式列表”。至少包括：

```text
1. 当前要做的决策
2. 关键事实
3. 关键未知
4. 当前结构/问题
5. 3-5 套候选
6. 经济模型
7. 条件性经济
8. 风险/竞争/反方
9. 关键假设
10. 实验与 Kill
11. 排序/淘汰
12. 下一步真实行动
```

数据不足时可以给条件式决策树，不要伪造唯一确定答案。

人工可读输出优先使用“商业决策输出”，不使用生硬的“决策工件”。

---

# 十六、Trace 与可观测性

每次后台运行应能回答：

- 为什么路由到该任务族；
- 为什么加载这些 U 域；
- 哪些 Atom/Pattern 被召回；
- 哪些实际进入候选；
- 哪些加载但未使用；
- 真实数据缺什么；
- 哪些结论依赖假设；
- 使用了哪些外部来源；
- Context 大小；
- 错误发生在哪一层。

长期可统计：Asset Usage Rate、Asset Unique Contribution、Retrieval Recall、Context Precision、Average Context Cost、Route Accuracy、Candidate Diversity、Financial Error Rate、Evidence Error Rate、Regression Rate。

这些指标服务于提高真实项目结果，而不是替代真实项目结果。

---

# 十七、错误分类与修复路径

- **K1 Knowledge Gap**：研究机制，再判断是否新 Atom/Pattern/专题/案例；
- **R1 Retrieval Failure**：关键词、别名、metadata、BM25、embedding、rerank、domain route；
- **W1 Workflow Failure**：模块顺序、强制关口、条件分支、输出契约；
- **C1 Context Failure**：减噪、top-K、重排、补上下文、解决冲突；
- **E1 Evidence Failure**：来源、时间、证据等级、Fact/Assumption、freshness；
- **F1 Financial Failure**：公式、会计口径、数据类型、单位、现金/收入/贡献；
- **S1 Strategy Failure**：竞争反应、多方激励、壁垒、替代和反方；
- **T1 Tool Failure**：重试、降级、数据源替代、显式错误；
- **O1 Output Failure**：商业决策输出、优先级、Next Action、摘要/附录分离；
- **B1 Benchmark Failure**：修 Benchmark 本身，不训练系统适应错误题。

真实项目业务层应先按：项目理解 → 商业问题 → 市场研究 → 利润池 → 上下游 → 候选 → 经济性 → 排序 → 行动 → P20 状态继承定位，最后才判断 K1。

---

# 十八、知识反馈 Router

```text
New Finding
↓
已有 Atom？ → 补证据/别名/关系
↓ 否
已有 Pattern？ → 补实例/边界
↓ 否
只是已有 Atom 新组合？ → Candidate Pattern / Case
↓ 否
只是行业实例？ → 04 案例
↓ 否
只是证据？ → Case / Evidence / 90 Source
↓ 否
只是专题知识？ → 09 专题
↓ 否
只是时效规则？ → Freshness / 外部事实层
↓ 否
跨行业可迁移且无法由现有机制表达？ → Candidate Atom/Pattern
```

T03/T04 真实测试没有发现必须立即新增本体对象的问题，因此本轮不扩 U/Atom/Pattern/Schema。

---

# 十九、知识生命周期

稳定对象采用：

```text
candidate
→ experimental
→ verified
→ stable
→ deprecated / superseded / historical
```

时效知识额外保留：

```yaml
valid_from:
valid_to:
as_of_date:
source:
freshness_class:
recheck_trigger:
```

平台规则、费率、促销、法规不能和“订阅”“Marketplace”等稳定机制使用相同生命周期。

---

# 二十、版本升级规则

只有以下情况值得升级运行时或本体版本：

1. Benchmark 显示稳定提升；
2. 修复高频 K/R/W/C/E/F/S 类失败；
3. 新对象在多个真实项目中证明不能由旧对象表达；
4. 新 Schema 解决真实数据/决策表达问题；
5. 有明确 Migration / Regression 计划。

文档变长、Pattern 增加或新增名词，不构成版本升级理由。

---

# 二十一、长期闭环

后台长期循环：

```text
知识
→ Workflow
→ 真实任务
→ Trace
→ Benchmark
→ 错误分类
→ 根因
→ 修知识 / 检索 / 流程 / 数据 / 测试
→ Regression
→ 新一轮真实任务
→ 知识反馈
→ 生命周期与版本治理
```

人工经营循环则是：

```text
真实项目/现象
→ P01-P20 按需运行
→ 第一推荐
→ 真实交易/实验
→ P20 新结果
→ 只重跑受影响阶段
```

两者共同构成“项目商业推理工作流”：前者保证系统长期可靠，后者保证普通用户能真正拿它做商业决策。