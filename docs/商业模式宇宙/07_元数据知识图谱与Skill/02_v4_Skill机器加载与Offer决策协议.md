# 商业模式宇宙 v4：Skill 机器加载与 Offer 决策协议

> 本文件在 v2 `03` 与 v3 `10` 上增量扩展，不替换已有 Skill。

## 一、v4 Skill 的目标

面对“某个商品比较贵，怎么获得更多客户？”时，不允许直接跳到“降价/做低价引流”。

必须经过：

```text
目标客户与付款方
→ 当前购买阻力
→ 可承担不同角色的产品/服务/权益候选
→ 场景/时间/渠道/库存/容量条件
→ 价格架构
→ Offer节点与转化边
→ 3~7个候选Offer Architecture
→ 前端/购物篮/Cohort单位经济
→ U19 Net Effective Economics
→ 品牌/渠道/履约/合规/欺诈风险
→ 最小实验
→ 排序/淘汰/扩量
```

---

# 二、v4 新增机器对象

```yaml
product_role_assignments:
  - offer_id:
    product_id:
    primary_role: PRxx
    secondary_roles: []
    role_reason:
    target_segment:
    role_kpis: []
    exit_conditions: []

price_architecture:
  reference_layer:
    list_price:
    reference_price:
    anchor_offer:
  entry_layer:
    free_or_paid:
    trial_price:
    intro_price:
    standard_repeat_price:
  fences:
    segment:
    eligibility:
    channel:
    geography:
    time:
    context:
  choice_architecture:
    tiers: []
    anchor:
    decoy:
    bundle:
    unbundle:
    add_ons: []
  meter_and_commitment:
    unit:
    included_usage:
    overage:
    credits:
    minimum_commitment:
    reserved_capacity:
  net_effective_economics:
    conditional_economics_ref:
    net_effective_price:

context_router:
  customer_state:
  lifecycle:
  time:
  season:
  holiday_event:
  location:
  weather:
  inventory_state:
  capacity_state:
  channel:
  current_intent:
  eligible_offer_ids: []

offer_architecture:
  nodes:
    - offer_id:
      role_ids: []
      price_mechanism_ids: []
      target_segment:
      trigger_context:
      economics:
      constraints:
  edges:
    - from_offer:
      to_offer:
      trigger_event:
      eligibility:
      conversion_rate:
      attach_rate:
      time_lag_days:
      incremental_revenue:
      incremental_contribution:
      evidence_level:
      confidence:

cohort_economics:
  front_end_revenue:
  cogs:
  packaging:
  fulfillment:
  delivery:
  spoilage_loss:
  direct_promotion_cost:
  front_end_contribution:
  attach_contribution:
  backend_contribution:
  membership_contribution:
  subscription_contribution:
  repeat_contribution:
  cross_sell_contribution:
  referral_contribution:
  supplier_conditional_economics:
  avoided_spoilage_or_capacity_value:
  cac:
  service_cost:
  refunds_returns:
  fraud_abuse:
  financing_cost:
  expected_clawback:
  true_cohort_contribution:
  payback_days:
  measurement_window_days:
  realized_vs_forecast:

promotion_experiment:
  hypothesis:
  population:
  assignment:
  treatment:
  control_holdout:
  primary_metric:
  guardrails: []
  observation_window:
  budget_cap:
  pass_condition:
  kill_condition:
  scale_condition:
  confounders: []
```

---

# 三、v4 新增 Skills

### `product-role-classifier`

输入产品/SKU/服务/权益与业务目标，输出 PR01-PR40 多标签角色；必须指定主角色、KPI、退出条件。

### `entry-offer-generator`

从目标客群、阻力、场景、现有商品、毛利、供应商条件、容量与库存中，生成 3~7 个不同入口策略，而不是只生成低价 SKU。

### `price-architecture-designer`

同时设计参照层、进入层、价格围栏、选择架构、计量/承诺和净有效价格；调用既有 `net-price-waterfall` 而不是重复实现返点。

### `context-offer-router`

基于用户状态 × 时间 × 季节 × 地点 × 天气 × 事件 × 生命周期 × 库存 × 容量，生成/筛选下一最佳 Offer。

### `conversion-graph-builder`

把 Free/Entry/Core/Profit/Upsell/Cross-sell/Recurring/Referral/Reactivation 表示为条件图，而不是强制线性漏斗。

### `basket-attach-analyzer`

计算购物篮、Attach Rate、Cross-sell、Upsell 的增量贡献，并区分“相关一起购买”与“促销导致的增量”。

### `cohort-economics-simulator`

同时计算 Front-end、Basket、True Cohort Contribution，以及 30/60/90/180/365 天回收情景。

### `loss-leader-guardrail`

低价/免费策略必须检查：目标客群重合、补贴上限、Attach/Backend、Payback、薅羊毛、品牌、渠道、库存、履约与 U19 条件经济。

### `promotion-incrementality-auditor`

判断活动是否真正带来净增量，而不是全价客户迁移、未来需求前置或自然回流；优先要求 control/holdout。

### `offer-portfolio-composer`

把多个商品角色组合成 3~7 套结构差异明显的 Offer Architecture，并允许不同客群/场景采用不同图。

### `offer-architecture-ranker`

对候选方案进行多目标排序，而不是单看转化率。

---

# 四、候选 Architecture 的强制输出格式

```yaml
candidate_id:
rank:
name:

who:
  target_segment:
  payer:
  user:

problem:
  primary_resistance:
  why_now:

entry:
  offer_id:
  role_ids: []
  price_mechanisms: []
  trigger_context:
  qualification_fences: []

conversion_graph:
  path_summary:
  critical_edges: []

backend_profit_pools:
  - source:
    expected_contribution:
    confidence:

conditional_economics:
  rebate_or_supplier_funding:
  net_effective_price:

unit_economics:
  front_end_contribution:
  basket_contribution:
  true_cohort_contribution:
  cac:
  ltv:
  payback:

fit_score:
  target_overlap:
  perceived_value:
  context_fit:
  backend_compatibility:
  repeatability:
  operational_feasibility:
  brand_fit:
  channel_fit:

risks:
  abuse:
  cannibalization:
  brand_dilution:
  channel_conflict:
  capacity_stockout:
  regulatory:

critical_assumptions: []
smallest_test:
pass_condition:
kill_condition:
evidence_level:
```

---

# 五、候选排序模型

默认评分不是“谁最便宜谁第一”。

建议：

```text
Opportunity Score
= 15% Target Segment Overlap
+ 10% Need/Perceived Value
+ 10% Context Fit
+ 10% Entry Friction Reduction
+ 15% Backend Contribution Potential
+ 10% Repeat/LTV Potential
+ 10% Payback Quality
+ 5% Supplier/Conditional Economics
+ 5% Operational Feasibility
+ 5% Brand/Channel Fit
+ 5% Evidence Confidence

Risk Penalty
= Abuse + Cannibalization + Brand + Channel + Capacity + Compliance
```

行业不同可以调整权重，但必须显示改变后的权重。

---

# 六、低价入口专用决策树

```text
是否存在高感知、高需求且客群重合的入口？
├─ 否 → 不使用Loss Leader；考虑Trial/Sample/Content/Channel/Finance等其他入口
└─ 是
   ↓
入口前端贡献是否为负？
├─ 否 → 可能只是Traffic/Hero/Entry Offer
└─ 是 → 标记PR03 Loss Leader
   ↓
是否存在可量化的Attach/Backend/Repeat/Conditional Economics？
├─ 否 → Kill
└─ 是
   ↓
True Cohort Contribution和Payback是否过门？
├─ 否 → 调价格/资格/数量/场景/后端，仍不过门则Kill
└─ 是
   ↓
品牌/渠道/欺诈/履约是否过门？
├─ 否 → 改用小规格、限新、限时、会员、bundle、supplier-funded等结构
└─ 是 → 最小实验
   ↓
Holdout增量贡献是否通过？
├─ 否 → Kill/重构
└─ 是 → 分阶段Scale并持续观察cohort
```

---

# 七、示例：精品果篮较贵

Skill 不应只返回“1分钱西瓜”。至少可以生成：

1. **季节性合格 Loss Leader**：夏季时令高感知 SKU → 限新/限量 → 果篮/其他水果 Attach → 会员/复购。
2. **Sample/Trust Architecture**：精品水果小份试吃/体验盒 → 正装礼盒 → 周期配送/会员。
3. **Entry Bundle Architecture**：低门槛迷你果篮 → 标准果篮 → 高端礼赠/加急配送/贺卡 Add-on。
4. **Enterprise Gift Architecture**：企业试用礼盒 → 企业礼赠合同 → 收件人个人复购。
5. **Membership Architecture**：首单权益 → 会员 → 会员价/配送/积分 → 高频水果 → 节庆礼盒。
6. **Context Router**：夏季西瓜、节日礼盒、公司庆典、探病/拜访等场景使用不同入口。
7. **Supplier-funded Architecture**：供应商战略/临期/高返点 SKU → 低净成本入口 → 后端标准毛利组合。

然后再按真实成本、库存、客群、渠道与实验数据排序。

---

# 八、机器加载兼容规则

v4 是增量加载：

```text
atoms = atoms.jsonl
      + atoms_v3_registry.json
      + atoms_v4_registry.json

patterns = patterns.jsonl
         + patterns_v3_extension_P131-P170.jsonl
         + patterns_v4_extension_P171-P200.jsonl

product_roles = product_roles_v4.json
schema = business_model_signature_v4.schema.json
```

`product_roles_v4.json` 是横向 taxonomy，不计入 L1/L2 atom 数。

---

# 九、Skill 的硬性拒绝条件

以下情况不得输出“建议低价引流”作为首选：

- 没有后端利润池；
- 目标客群与领取客群明显不重合；
- 无法控制补贴规模；
- 无法测量增量；
- 高端品牌价格锚点会被显著破坏；
- 渠道合同/价保不允许；
- 履约/库存/算力容量已经接近极限；
- 主要利润依赖未确认返点；
- 活动依赖欺诈、误导、未披露个人回扣或违法价格行为。
