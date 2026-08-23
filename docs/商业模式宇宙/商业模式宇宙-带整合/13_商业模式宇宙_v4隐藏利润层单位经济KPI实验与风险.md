# 商业模式宇宙 v4：隐藏利润层、Cohort Economics、KPI、实验与风险

> 目的：把“前端不赚钱、整体赚钱”从营销口号变成可计算、可审计、可停止的经济模型。

## 一、利润不能只在 SKU 毛利中寻找

一个 Offer 的真实利润至少可能分布在六层：

### E1 单笔交易层

- 商品毛利；
- 加购/Add-on；
- Upsell；
- Cross-sell；
- 套餐结构；
- 配送/服务/安装费；
- 支付手续费或价差；
- 延保/风险产品；
- 礼品包装、加急、优先服务等增值项。

### E2 Cohort 后端层

- 后续复购；
- 订阅；
- 会员费；
- 会员带来的频次/购物篮提升；
- 生命周期延伸；
- 企业采购/礼赠；
- 推荐带来的新 cohort；
- 唤醒后的恢复价值。

### E3 条件性经济层

继续继承 U19/06：

- 采购返点；
- 增长返点；
- 年终返点；
- MDF / Co-op；
- free goods；
- cloud/ad/service credits；
- 账期价值；
- 渠道奖励；
- 价格保护/chargeback；
- 供应商承担的促销预算；
- partner tier/认证权益；
- threshold cliff；
- clawback。

### E4 库存、容量与损耗层

- 避免 spoilage；
- 降低库存持有成本；
- 清季末库存；
- 利用原本会过期的座位/房间/时段/算力/工时；
- 通过更高密度降低配送或服务单位成本；
- 通过预约、预付和承诺提高可预测性。

因此一个“低价” Offer 可能账面毛利下降，但因避免损耗或利用闲置容量而增加**增量贡献**。

### E5 现金流、Breakage 与资产负债表层

- 预付；
- 年付；
- 礼品卡/储值；
- credits；
- float；
- 供应商账期；
- 应收融资；
- breakage；
- 未使用权益；
- FX/结算周期。

注意：**现金提前流入 ≠ 当期利润；breakage ≠ 可以人为制造兑换困难。** 必须遵守会计、消费者保护、储值与支付监管。

### E6 数据、渠道、生态与非现金层

- 第一方数据；
- 用户识别与后续可触达关系；
- 渠道交换价值；
- 合作伙伴等级；
- 联合营销资源；
- 推荐网络；
- 内容/UGC；
- 生态分成；
- 品牌心智和搜索份额。

这些只有在未来价值能够被验证时才能计入决策，不应随意折算成“虚拟利润”。

---

# 二、三层贡献利润模型

## 2.1 前端贡献 Front-end Contribution

```text
Front-end Revenue
- COGS
- Packaging
- Fulfillment
- Delivery / Last-mile
- Payment Cost
- Spoilage / Loss
- Direct Promotion Subsidy
- Incremental Support Cost
= Front-end Contribution
```

### 解释

- `Discount` 不应重复扣两次：若 Revenue 已使用实际成交价，则折扣已体现在收入中。
- 免费商品要按其真实增量成本/机会成本进入模型。
- 配送、客服、仓内拣货、算力等经常是“1分钱商品”最容易漏掉的成本。

## 2.2 购物篮/会话贡献 Basket/Session Contribution

```text
Front-end Contribution
+ Same-order Add-on Contribution
+ Cross-category Contribution
+ Upsell Contribution
+ Service/Delivery Contribution
+ Conditional Supplier Funding Allocated to Order
= Basket Contribution
```

## 2.3 Cohort 真贡献 True Cohort Contribution

```text
Basket Contribution
+ Backend Product Contribution
+ Membership Contribution
+ Subscription Contribution
+ Repeat Purchase Contribution
+ Lifecycle Extension Contribution
+ Referral-derived Contribution
+ Reactivation Contribution
+ Expected Supplier Rebate / MDF / Credits Value
+ Avoided Spoilage / Capacity Value
+ Other Verifiable Conditional Economics

- Acquisition Cost
- Promotion Operations Cost
- Incremental Customer Service
- Returns / Refunds
- Fraud / Abuse
- Loyalty / Reward Cost
- Financing / Working-capital Cost
- Expected Clawback
= True Cohort Contribution
```

必须同时输出：

- 30/60/90/180/365 天 cohort contribution；
- Payback；
- 置信区间或场景区间；
- 尚未发生但被模型预测的部分；
- 已实现现金与会计收入的差异。

---

# 三、促销应该视为“可替代 CAC 渠道”

低价/免费 Offer 的促销成本不能藏在商品毛利里。

```text
Promotion Acquisition Cost
= Incremental Discount Cost
+ Free Goods Cost
+ Coupon Cost
+ Delivery Subsidy
+ Extra Fulfillment/Support
+ Promotion Media/Creative/Tech Cost
+ Abuse/Fraud Loss

Qualified Promo CAC
= Promotion Acquisition Cost
÷ Incremental Qualified New Customers
```

然后与：

- Paid Ads CAC；
- Affiliate CAC；
- Creator CAC；
- Sales CAC；
- Channel CAC；
- Referral CAC；

比较。

**领取人数、曝光、到店人数都不能直接作为分母，除非目标本身就是这些行为。**

---

# 四、入口品选择评分器

候选 Traffic/Hook/Loss Leader 不应凭直觉选“最便宜的”。

建议评分：

```text
Entry Offer Score
= Target Segment Overlap
× Need Intensity
× Perceived Value Gap
× Context Fit
× Discoverability
× Shareability
× Backend Compatibility
× Repeat Potential
× Supply Reliability
× Operational Simplicity
× Incremental Margin Recovery Potential

÷ (Subsidy Cost
 + Fulfillment Burden
 + Spoilage Risk
 + Fraud Risk
 + Brand Conflict
 + Channel Conflict
 + Cannibalization Risk)
```

实际实现不要机械相乘所有百分比；可采用 1-5/1-10 归一化加权评分，并把最敏感变量单独做情景分析。

---

# 五、核心 KPI 字典

## Acquisition

- Impressions / Reach；
- Qualified Visits；
- Lead Capture Rate；
- Activation Rate；
- New Customer Conversion；
- Qualified CAC；
- Promotion CAC；
- Referral CAC。

## Basket / Conversion

- AOV / Basket Size；
- Units per Transaction；
- Attach Rate；
- Upsell Rate；
- Cross-sell Rate；
- Bundle Mix；
- Target-tier Choice Share；
- Checkout Conversion。

## Retention / LTV

- Repeat Rate；
- Reorder Interval；
- Subscription Conversion；
- Churn；
- Net Revenue Retention；
- Reactivation Rate；
- Membership Renewal；
- Referral Rate；
- LTV。

## Economics

- Front-end Contribution；
- Basket Contribution；
- True Cohort Contribution；
- Contribution Margin；
- Incremental Contribution；
- Price Realization；
- Net Effective Price；
- Supplier-funded Share；
- Payback；
- Promotion ROI。

## Rights/credits/capacity

- Redemption；
- Breakage；
- Credit Burn Rate；
- Top-up Rate；
- Overage Rate；
- Capacity Utilization；
- Revenue per Available Unit；
- Spoilage / Markdown Recovery；
- Stockout Rate。

## Guardrails

- Refund/Return；
- Fraud/Abuse；
- Complaint Rate；
- NPS/CSAT；
- Service SLA；
- Fulfillment Cost；
- Brand Lift/Dilution proxy；
- Channel Complaint/Price Protection Cost；
- Normal-price Cannibalization。

---

# 六、最小实验协议

任何重要 Offer Architecture 在大规模投放前至少形成：

```yaml
hypothesis:
  mechanism:
  expected_increment:

population:
  target_segment:
  exclusions:
  new_or_existing:

assignment:
  unit: user|store|region|account|time_window
  treatment:
  control_or_holdout:
  randomization_or_quasi_experimental_method:

measurement:
  primary_metric:
  guardrails:
  observation_window:
  attribution_window:
  pre_period:

unit_economics:
  promo_budget_cap:
  max_subsidy_per_qualified_customer:
  expected_payback:

pass_condition:
kill_condition:
scale_condition:

confounders:
  seasonality:
  stockouts:
  concurrent_promotions:
  channel_changes:
  competitor_actions:
```

## 必测 Incrementality

最危险的假象是：

> “用了优惠的人买了很多，所以优惠有效。”

真正问题是：

> **如果没有这个优惠，他们本来会不会买？**

所以至少要尝试：

- randomized holdout；
- store/region matched control；
- pre/post + difference-in-differences；
- switchback（时间轮换）；
- geo experiment；

并把无法随机化的局限写进证据等级。

---

# 七、Failure Modes：低价引流的 16 种常见失败

1. 目标客群重合度低，只吸引价格敏感人群；
2. 入口商品有需求，但没有明确后端下一步；
3. Attach Rate 很低；
4. 高客流导致履约/客服/配送成本爆炸；
5. 低价 SKU 本身易损耗，促销反而增加报损；
6. 原本全价客户被促销蚕食；
7. 用户形成“等活动”心智，标准价接受度下降；
8. 高端品牌因超低价入口被稀释；
9. 经销/平台/直营网店之间发生价格冲突；
10. 多账号、代领、转售、机器人或虚假新客套利；
11. 活动只是把未来需求提前；
12. 供应商返点/MDF未满足条件或被 clawback；
13. 会员/订阅权益成本被低估；
14. 复购发生太慢，Payback 超出现金承受能力；
15. 库存、容量或地域限制使模型无法规模化；
16. 竞争对手跟价后，入口优势消失而补贴成为行业常态。

---

# 八、品牌与渠道冲突门

当项目存在 Premium/高端定位时，低价 Offer 优先考虑：

- 小规格/sample，而不是同一核心品永久降价；
- 限资格/限首次；
- 限时间/场景；
- Bundle value，而非直接砍价；
- 渠道独占包装/不同 SKU；
- 会员权益；
- 服务/credits；
- Supplier-funded benefits；

目标是降低**进入门槛**，而不是无条件降低**价值锚点**。

---

# 九、隐藏利润层审计清单

分析任何项目，除 U19 返点外继续问：

1. 是否有未利用的预付/礼卡/credits 经济？
2. 是否存在 breakage，但会计与法规如何处理？
3. 是否有闲置/易腐容量可在低峰变现？
4. 是否有临期、季末、尾货、退货或二手残值？
5. 是否有供应商愿意共同承担引流成本？
6. 是否有包装、配送、安装、维护、延保、回收等后端服务？
7. 是否有渠道、流量或数据可以交换而非现金采购？
8. 是否有支付、结算、账期、float、FX 等财资价值？
9. 是否存在企业礼赠、员工福利、政府/保险等第三方付款方？
10. 是否能把一次购买延伸为耗材、订阅、会员、补货或生命周期需求？
11. 是否有退货/回收/二手/翻新形成第二次价值捕获？
12. 是否存在合同 minimum commitment、auto-renew、SLA credits、价格锁定或退出权改变经济性？
13. 是否有非现金 partner benefits 可以可靠量化？
14. 是否有未披露/个人级利益冲突？若有，进入风险审计而不是利润优化。

---

# 十、证据强度与停止规则

每个候选 Architecture 标记：

- `E0`：纯机制假设；
- `E1`：跨行业理论/公开研究支持；
- `E2`：行业案例支持；
- `E3`：自身历史数据支持；
- `E4`：自身受控实验支持；
- `E5`：规模化后持续 cohort 数据支持。

停止/淘汰条件：

> 连续实验显示增量贡献 ≤0；Payback 超上限；品牌/渠道/合规 guardrail 触发；或规模扩大后履约成本使贡献反转。
