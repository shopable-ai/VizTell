# 商业模式宇宙：元数据、知识图谱与 Skill 协议

## 1. 统一对象结构

一个新项目至少要表示为：

```yaml
project:
  name:
  domain:
  maturity:

actors:
  - role:
    pays:
    uses:
    supplies:
    owns:
    acquires_customers:

problem:
  pains:
  current_alternatives:
  switching_barriers:

offer:
  value_propositions:
  rights_packaging:
  front_end_wedge:

delivery:
  channels:
  supply_structure:
  fulfillment:
  trust_mechanisms:

economics:
  pricing:
  payer:
  revenue_streams:
  subsidy_source:
  variable_costs:
  fixed_costs:
  gross_margin:
  cac:
  ltv:
  payback:
  cash_in_timing:
  cash_out_timing:


conditional_economics:
  list_price:
  invoice_price:
  base_discount:
  eligibility_metric:
  aggregation_scope:
  threshold_type:
  tiers:
  retroactive_or_incremental:
  cash_rebate:
  non_cash_benefits:
  MDF_coop:
  credits:
  payment_term_value:
  cap_floor:
  clawback:
  claim_window:
  beneficiary:
  disclosure_level:
  net_effective_price:

retention:
  repeat_driver:
  switching_cost:
  control_points:

growth:
  replication:
  network_effects:
  flywheels:

digital_assets:
  data:
  ip:
  software:
  ai:
  api:

constraints:
  prerequisites:
  regulations:
  risks:
  failure_modes:

evidence:
  facts:
  source_claims:
  assumptions:
  hypotheses:
  confidence:
```

## 2. Skill 不应按“行业名字”检索

推荐流程：

```text
输入项目
→ 抽取18维模式签名
→ 找最缺的价值/收入/成本/现金流环节
→ 匹配L2原子
→ 召回L3组合模式
→ 检查模式前置条件
→ 检查互补/冲突关系
→ 构造3~7个候选组合
→ 单位经济性审计
→ 现金流审计
→ 参与方激励审计
→ 合规/风险审计
→ 设计最小实验
→ 选择/淘汰
```

## 3. 推荐结果必须解释“为什么”

每个推荐模式输出：

```yaml
pattern:
why_fit:
required_atoms:
economic_logic:
who_pays:
who_subsidizes:
customer_acquisition:
supply_source:

conditional_economics:
  list_price:
  invoice_price:
  base_discount:
  eligibility_metric:
  aggregation_scope:
  threshold_type:
  tiers:
  retroactive_or_incremental:
  cash_rebate:
  non_cash_benefits:
  MDF_coop:
  credits:
  payment_term_value:
  cap_floor:
  clawback:
  claim_window:
  beneficiary:
  disclosure_level:
  net_effective_price:

retention:
cashflow:
critical_assumptions:
risks:
smallest_test:
pass_condition:
kill_condition:
```

## 4. 事实、推断、假设分离

```yaml
fact:
  statement:
  source:
  verification_status:

source_claim:
  statement:
  source:
  verified: false

mechanism_inference:
  statement:
  confidence:

transfer_hypothesis:
  statement:
  test_required: true
```

案例中的“融资XX亿”“一年赚XX”等绝不能直接成为通用规则。

## 5. 相似度不是文本相似度

模式迁移相似度建议按：

```text
参与方结构
+ 付款方结构
+ 毛利结构
+ 边际成本
+ 使用频次
+ 复购结构
+ 供给碎片度
+ 渠道结构
+ 信任需求
+ 资产所有权
+ 现金流时序
+ 网络效应
+ 监管强度
```

两家公司行业完全不同，也可能拥有高度相似的商业模式签名。

## 6. 知识图谱节点类型

- Actor
- Segment
- Pain
- Job
- Offer
- Resource
- Asset
- Activity
- Partner
- Channel
- Transaction
- TrustMechanism
- PricingMechanism
- Payment
- RevenueStream
- CostDriver
- CashflowMechanism
- DataAsset
- IPAsset
- ControlPoint
- GrowthLoop
- NetworkEffect
- Risk
- Regulation
- KPI
- Evidence
- Atom
- Pattern
- Case
- Experiment

## 7. Skill 角色拆分

### `business-model-extractor`
从文章、案例、公司或项目中抽取模式签名。

### `business-model-classifier`
映射到 L1/L2/L3，不做单一互斥分类。

### `business-model-matcher`
对新项目召回可用原子和组合模式。

### `business-model-composer`
组合新的商业模式候选。

### `business-model-economics-auditor`
审查收入、成本、CAC/LTV、毛利、Payback和现金流。

### `business-model-risk-auditor`
审查监管、欺诈、补贴、平台去中介、AI成本等风险。

### `business-model-transfer`
寻找跨行业经济结构相似案例并生成迁移方案。

### `business-model-experiment-designer`
把模式转成可验证实验，而不是只给概念建议。



## 8. 条件经济性与返点 Skill

### `rebate-extractor`
抽取合同/渠道政策中的门槛、基数、阶梯、资格、结算与clawback。

### `net-price-waterfall`
计算标价、前台折扣、后台返点、credits、MDF、free goods和账期后的实际净价。

### `threshold-optimizer`
计算是否值得为了跨过下一档返点而增加采购/投放。

### `rebate-auditor`
发现漏领、错算、过期、互斥/重复激励和集团量未聚合。

### `hidden-economics-risk-auditor`
检查未披露代理利益、个人回扣、principal trading、dual rate card、排他返点与利益冲突。
