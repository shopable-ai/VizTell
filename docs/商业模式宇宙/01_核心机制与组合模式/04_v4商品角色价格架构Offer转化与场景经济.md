# 商业模式宇宙 v4：商品角色、价格架构、Offer 转化与场景经济

> v4 不新增一级域。它把既有 U03/U04/U06/U10/U11/U13/U18/U19/U21/U22 等原子重新连接为可供人类与 Skill 直接推理的横向系统，解决“有 Loss Leader/Freemium 原子，但不会自动设计完整 Offer 链”的缺口。

## 一、核心结论

商品不是天然只有“卖出赚钱”一个角色。同一个 SKU 在不同客群、时间、渠道和生命周期中可以承担不同角色；角色属于**交易上下文**而不是商品本体。

统一分析链：

> **目标用户 → 当前阻力 → 商品角色 → 价格机制 → 进入动作 → 转化边 → 后端利润池 → 留存/复购 → 条件经济性 → Cohort Contribution → 风险 → 最小实验**

因此应把：

- `Product`：卖什么；
- `Product Role`：它在当前商业系统中承担什么任务；
- `Pricing Mechanism`：怎样计价；
- `Offer`：对谁、在什么条件下，以什么价格/权益组合呈现；
- `Offer Architecture`：多个 Offer 如何按条件连接；
- `Business Model`：整个价值创造、交付、捕获与持续系统；

严格区分。

---

# 二、商品角色宇宙：五大角色族

机器稳定 ID 见 `product_roles_v4.json`。一个 Offer 可多标签，但必须指定 `primary_role`，否则 Skill 容易把所有好处都贴到一个商品上。

## A. 获客、注意力与首次行动角色 PR01-PR07

| ID | 角色 | 核心任务 |
|---|---|---|
| PR01 | Traffic Product / 流量品 | 最大化合格访问、到店、搜索或点击，不要求自身高毛利。 |
| PR02 | Hook / Lead Magnet / 钩子品 | 用高感知价值换注册、加好友、留资、下载或进入销售流程。 |
| PR03 | Loss Leader / 亏损引流品 | 允许前端贡献为负，但必须由购物篮或后端 Cohort Contribution 回收。 |
| PR04 | Trial / Experience / 体验品 | 降低首次使用与信任门槛，核心 KPI 是体验后付费转化。 |
| PR05 | Sample / 样品 | 用小规格、局部能力或试吃试用证明质量，控制采样成本。 |
| PR06 | Hero / Signature SKU / 超级爆品 | 负责心智、搜索、口碑和规模流量，可同时是利润品。 |
| PR07 | Seasonal/Event Hook / 时令事件入口品 | 在季节、天气、节日或事件需求峰值中承担入口角色。 |

## B. 认知、信任、定位与选择架构角色 PR08-PR13

| ID | 角色 | 核心任务 |
|---|---|---|
| PR08 | Trust Product / 信任品 | 用透明、低风险、标准化交付或代表性质量建立购买信任。 |
| PR09 | Image/Flagship / 形象旗舰品 | 建立品牌上限、技术能力、稀缺性或身份定位，不以销量最大为目标。 |
| PR10 | Anchor/Reference / 锚定品 | 提供价格/价值参照，帮助用户解释目标 Offer 的相对价值。 |
| PR11 | Decoy/Comparison / 对比诱饵品 | 改变选择集结构以帮助用户权衡；必须做真实实验，不能假定一定有效。 |
| PR12 | Qualification/Screening / 筛选品 | 通过资格、价格、使用行为或小额支付过滤低意向/不匹配用户。 |
| PR13 | Identity/Data Entry / 用户识别品 | 合法合规地把匿名需求变成可识别账户、偏好或第一方数据关系。 |

## C. 核心变现与购物篮角色 PR14-PR21

| ID | 角色 | 核心任务 |
|---|---|---|
| PR14 | Core Offer / 核心商品 | 解决主要 Job-to-be-Done，是商业系统价值主张主体。 |
| PR15 | Profit Product / 利润品 | 贡献主要绝对毛利/贡献利润。 |
| PR16 | Margin Booster / Add-on / 毛利增强附加品 | 在主交易上增加高增量毛利。 |
| PR17 | Upsell / 升级品 | 从当前版本升级到更高价值/价格层。 |
| PR18 | Cross-sell / 交叉销售品 | 利用已建立的需求、信任与渠道卖相邻产品。 |
| PR19 | Bundle Driver / 套餐核心品 | 作为套餐吸引力或价值中心，带动其他组件共同成交。 |
| PR20 | Premium/Status / 高端溢价品 | 服务高支付意愿、身份、稀缺、服务或性能需求。 |
| PR21 | Enterprise/Gift / 企业礼赠品 | 把个人消费商品转成组织采购、礼赠、员工福利或客户关系预算。 |

## D. 留存、复购与生命周期角色 PR22-PR28

| ID | 角色 | 核心任务 |
|---|---|---|
| PR22 | Replenishment/Consumable / 补充耗材品 | 由消耗、补货或维护周期驱动复购。 |
| PR23 | Subscription / 订阅品 | 把持续价值转成周期性付费。 |
| PR24 | Membership / 会员品 | 用身份、权益、价格与服务组合提高频次和留存。 |
| PR25 | Habit/Frequency / 高频习惯品 | 用高频使用占据心智与关系入口。 |
| PR26 | Lifecycle Extension / 生命周期延伸品 | 在用户下一阶段继续承接需求，延长 LTV。 |
| PR27 | Reactivation / 唤醒品 | 面向沉默/流失用户恢复交易，而非继续购买新客流量。 |
| PR28 | Loyalty/Redemption / 忠诚兑换品 | 承接积分、权益、里程或会员福利，影响留存与 breakage。 |

## E. 增长、伙伴、容量、库存与现金流角色 PR29-PR40

| ID | 角色 | 核心任务 |
|---|---|---|
| PR29 | Referral Reward / 推荐奖励品 | 激励现有用户带来新用户，并核算双边奖励成本与新客质量。 |
| PR30 | Viral/Shareable / 裂变传播品 | 商品/体验本身具有展示、分享或社交传播性。 |
| PR31 | Channel Exchange / 渠道交换品 | 作为异业、渠道或生态伙伴交换流量/权益的商业货币。 |
| PR32 | Supplier-funded Strategic SKU / 供应商战略品 | 供应商返点、MDF、free goods 等改变其真实单位经济性。 |
| PR33 | Data/Identity Product / 数据入口品 | 产品使用合法产生可复用数据、画像或后续服务输入。 |
| PR34 | Capacity Filler / 闲置容量填充品 | 在低峰时段提升房间、座位、算力、工时等利用率。 |
| PR35 | Inventory Liquidator / 库存消化品 | 用折价/组合/清仓降低过期、季末与持有成本。 |
| PR36 | Cashflow/Prepaid Product / 现金流品 | 通过预付、套餐、年付或承诺改善现金流与需求可预测性。 |
| PR37 | Gift Card/Credit / 储值权益品 | 把现金提前转换为未来消费权；需区分储值监管与 usage credits。 |
| PR38 | Backend Service / 后端服务品 | 在商品成交后用配送、安装、维护、咨询、代运营等获得后端收入。 |
| PR39 | Warranty/Risk Product / 风险保障品 | 把延保、保险、保证或风险承担变成独立价值与利润池。 |
| PR40 | Exit/Resale/Trade-in / 退出回收品 | 用回购、换新、二手、维修、再售承接生命周期末端并创造残值。 |

### 角色去重规则

- Traffic Product ≠ Loss Leader：前者定义目标，后者定义前端经济性可以为负。
- Hook ≠ Sample：Hook 关注获取行动/关系，Sample 是证明价值的一种包装。
- Hero SKU ≠ Profit Product：爆品可以低毛利，利润品也可以低流量。
- Anchor ≠ Decoy：Anchor 提供参照；Decoy 改变选择集结构。
- Subscription ≠ Membership：订阅主要是持续访问/交付与周期收费；会员强调身份与权益集合。
- Referral Reward ≠ Viral Product：前者有显式激励，后者可以靠产品天然传播。
- Gift Card ≠ Billing Credits：两者在法律、会计、可兑换范围与结算逻辑上可能不同，不应只因都叫“额度”而合并。

---

# 三、完整价格架构：价格不是一个数字

价格至少同时承担八个任务：

> **定位 + 降低进入门槛 + 筛选 + 分层 + 转化 + 提升购物篮 + 锁定/承诺 + 捕获真实净利润**

统一拆成六层：

## P0 Reference Layer / 参照层

`List Price → Reference/Anchor → Competitor Reference → Premium Ceiling`

解决“用户拿什么比较”。

## P1 Entry Layer / 进入层

`Free → Sample → Symbolic Price → Trial Price → First-order/New-customer Price → Intro Price → Standard Price`

核心不是越低越好，而是降低**目标客群**的第一步摩擦。

## P2 Segmentation/Fence Layer / 分层与价格围栏

按：

- 资格/用户分群；
- 新老客户；
- 数量/用量；
- 时间/季节；
- 地域；
- 渠道；
- 会员等级；
- 承诺期；
- 支付方式；
- 场景/事件；

给出不同交易条件。任何差异化定价都要做消费者保护、竞争、歧视与渠道合同审查。

## P3 Choice Architecture / 选择架构层

`Good-Better-Best → Anchor → Decoy/Comparison → Bundle/Unbundle → Add-on → Upsell → Cross-sell`

选择架构只是假设生成器，尤其 Decoy/Anchoring 不应被写成确定因果，必须通过受控实验验证。

## P4 Meter & Commitment / 计量与承诺层

`One-off → Subscription → Seat → Usage → Task → Outcome → Fixed+Usage → Included Usage+Overage → Credits → Minimum Commitment → Reserved Capacity`

适用于 SaaS、AI、API、云、服务与工业合同。

## P5 Net Effective Economics / 真实净价层

继续调用 v3/U19 的价格瀑布：

> `List → Invoice Discount → Off-invoice → Rebate → MDF/Co-op → Credits/Free Goods → Freight/Service → Payment Terms → Clawback → Net Effective Price/Revenue`

不得另造一套与 U19 冲突的“返点体系”。

---

# 四、Offer Architecture：从线性漏斗升级为条件图

默认不是所有项目都走同一条：

```text
Free Hook → Entry → Core → Profit → Upsell → Cross-sell → Subscription → Membership → Premium → Referral → Reactivation
```

应表示为图：

```text
Offer Node
  ├─ role_ids[]
  ├─ price_mechanisms[]
  ├─ eligible_segment
  ├─ trigger_context
  ├─ economics
  └─ capacity/inventory constraints
        ↓ conditional edge
Next Offer Node
```

每条边至少记录：

- `trigger_event`：购买、使用、达到额度、沉默、节日、天气等；
- `eligibility`：谁可以进入；
- `conversion_rate`；
- `attach_rate`；
- `time_lag`；
- `incremental_revenue`；
- `incremental_contribution`；
- `evidence/confidence`。

关键原则：

> **不能因为两件商品经常一起买，就自动把相关性当成可增量的 Cross-sell 因果。**

需要 control/holdout 测量增量。

---

# 五、低价/免费入口的成立条件

不能使用“便宜 → 流量”作为规则。更完整的机制是：

```text
Qualified Acquisition Potential
≈ Perceived Value
× Need Intensity
× Context Fit
× Target-segment Overlap
× Discoverability/Shareability
× Conversion Compatibility
× Operational Availability
÷ Entry Friction
```

然后必须通过经济门：

```text
Front-end Contribution
= Front-end Revenue
- COGS
- Fulfillment
- Delivery
- Spoilage/Loss
- Direct Promotion Cost

True Cohort Contribution
= Front-end Contribution
+ Attach Product Contribution
+ Backend Contribution
+ Membership/Subscription Contribution
+ Repeat Contribution
+ Cross-sell Contribution
+ Supplier/Channel/Conditional Economics
- CAC
- Incremental Service Cost
- Refunds
- Fraud/Abuse
```

成立条件至少包含：

1. 引流品客群与后端利润品客群高度重合；
2. 有可观测的下一步动作，而非只统计领取量；
3. 前端补贴/亏损有预算上限；
4. 购物篮、Attach Rate、后端转化或复购中至少有一项可承担回收；
5. 回收期可接受；
6. 不明显侵蚀原价购买、渠道价格、品牌定位；
7. 履约、配送、库存和损耗不会因流量增长反向吞噬利润；
8. 有防薅羊毛、重复账户、套利与转售规则；
9. 若供应商出资、返点或免费商品承担补贴，必须进入 Net Effective Economics；
10. 最终用 cohort/holdout 增量结果决定，而不是用“活动很热闹”决定。

---

# 六、场景 × 时间 × 商品：Context Router

入口商品不是固定 SKU，而应是一个“下一最佳 Offer”选择问题：

```text
Customer State
× Lifecycle
× Time of Day
× Week/Month
× Season
× Holiday/Event
× Location
× Weather
× Inventory
× Capacity
× Channel
× Current Intent
→ Candidate Entry Offers
→ Economics + Risk Filter
→ Best Offer
```

### 必须区分两类触发

**需求触发**：天气热、节日、开学、搬家、续约、项目上线等使需求本身提高。

**运营触发**：库存临期、低峰容量、返点门槛、供应商 MDF、物流空载等改变企业的边际经济性。

两者可以叠加，但不能混为一谈。

---

# 七、跨行业迁移示例

| 行业 | 入口/角色示例 | 后端候选 | 关键门 |
|---|---|---|---|
| 精品水果/零售 | 时令高感知低价 SKU、试吃、礼盒体验 | 精品果篮、会员、配送、企业礼赠、复购 | 篮子贡献、损耗、配送、客群重合、品牌稀释 |
| SaaS | 免费工具/试用/Starter | Team/Pro、席位扩展、实施、API | 激活、PQL、付费转化、服务成本 |
| AI/API | 免费 credits/credit pack | usage、overage、commit、enterprise | 推理成本、credits burn、毛利与限额 |
| 餐饮 | 低价招牌/限定时段品 | 正餐、饮品、套餐、会员 | 到店增量、桌台容量、Attach Rate |
| 酒店/航空 | 低峰入口/会员价 | 房型升级、行李、餐饮、延住、会员 | 易腐容量、取消/no-show、品牌/渠道冲突 |
| 游戏/内容 | 免费内容/体验 | 订阅、虚拟品、DLC、赞助/广告 | 留存、付费率、鲸鱼依赖、平台抽成 |
| B2B | 诊断/付费 Pilot | Core contract、land-and-expand、managed service | 线索质量、销售周期、交付容量 |
| 制造 | 样机/Starter Kit | 耗材、维护、备件、软件、服务合同 | Installed base、服务成本、采购返点 |

---

# 八、商品角色的四条治理规则

1. **角色不是永久属性**：夏季西瓜可以是 PR07+PR01，冬季可能只是普通 SKU。
2. **允许多角色但要有主角色**：否则 KPI 冲突无法判断。
3. **角色必须绑定经济责任**：Traffic Product 不能只看流量；要看 Qualified CAC 与 cohort contribution。
4. **角色必须有退出条件**：活动不增量、回收期过长、品牌/渠道/履约风险超阈值时自动停用。

---

# 九、v4 新增关系类型

知识图谱增加：

```text
Offer --has_role--> ProductRole
Offer --anchors--> Offer
Offer --decoys_for--> Offer
Offer --bundles_with--> Offer
Offer --cross_sells--> Offer
Offer --upsells_to--> Offer
Offer --replenishes--> Offer
Offer --reactivates--> CustomerState
Offer --triggered_by--> Context
Offer --funded_by--> ConditionalEconomics
Offer --converts_to--> Offer
ConversionEdge --measured_by--> KPI
Experiment --tests--> ConversionEdge/PriceMechanism
Risk --invalidates--> OfferArchitecture
```

这使 Skill 可以从“模式名召回”升级到“条件图组合”。
