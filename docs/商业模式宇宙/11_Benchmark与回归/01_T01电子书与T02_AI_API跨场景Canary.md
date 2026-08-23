# Benchmark T01 / T02：电子书 Seed Case 与 AI API 跨场景 Canary

> 目的：第一阶段不追求很多题，而是先用**两个结构明显不同**的任务验证运行时是否真的跨场景。
>
> T01 使用仓库已有专题知识；T02 不依赖电子书专题，验证系统不会变成“电子书商业模式专用工作流”。

---

# T01：电子书低门槛入口与后端商业化

## 1. 原始输入

> **基于这本电子书/PDF，研究适合的电商销售与后端商业模式。**

## 2. 正确背景

本题不是：

> “列出电子书行业所有商业模式。”

核心背景更接近：

> **在电商平台销售单本电子书/数字知识产品，把单本书作为一个低门槛、高意图识别入口，并继续发现与该用户领域、目标和任务相关的其他知识、商品、软件、AI、服务和企业价值。**

`09_专题商业模式/电子书商业模式.md` 已经明确覆盖：

- 单本/合集/专题；
- 会员；
- 官方渠道/分销；
- 知识加工；
- 知识补全；
- AI 阅读；
- AI 知识库；
- 知识库实施/咨询；
- 相关软件/硬件/服务；
- Affiliate；
- 企业后端；
- 作者/出版社；
- 数据/趋势。

因此 T01 首先测试的是：

> **Workflow 能不能把已有专题知识、通用宇宙和真实经济层正确组合起来。**

如果遗漏了仓库已经存在的“知识库/咨询/企业后端”，优先判 R1/W1，而不是立即新增知识。

---

# 3. T01 路由预期

```yaml
primary_family: design_new_business_model
flags:
  - knowledge_product
```

如果用户进一步明确：

> “0.01-3 元低价单本引流”

再增加：

```yaml
flags:
  - low_price_entry
```

不能因为专题里包含低价入口，就把任何“电子书研究”都强制假设为亏损引流。

---

# 4. T01 必需知识上下文

最低应覆盖：

- `09_专题商业模式/电子书商业模式.md`
- `01/06_机会来源_差异捕获与商业模式变换算子.md`
- `01/04_v4商品角色价格架构Offer转化与场景经济.md`
- `07/02_v4_Skill机器加载与Offer决策协议.md`
- `02/00_价值链与利润池总览.md`
- `06/02_v4隐藏利润层单位经济KPI实验与风险.md`
- `05/01/00_失败模式总览.md`

以及相关 Atom/Pattern。

---

# 5. T01 能力检查

一个强结果至少应主动发现以下结构，而不是照抄固定列表：

```text
电子书单本
→ Traffic / Hook / Qualification / Identity
→ 用户所在领域
→ 用户目标/任务
→ 同类书/合集/专题
→ 知识加工
→ 软件/AI/工具
→ 实物商品/相关服务
→ Affiliate / 分销
→ 会员/订阅
→ AI知识库
→ 知识库实施/咨询
→ 专业服务
→ 企业后端
```

这不是要求所有项目都同时做完这些，而是检查**Opportunity Recall**。

随后必须：

1. 生成 3-7 个结构差异明显的候选；
2. 判断哪些角色适合做入口、核心、利润、后端；
3. 排除只靠低价但没有回收路径的方案；
4. 建立经济模型；
5. 给关键实验和 Kill Condition。

---

# 6. T01 三层经济模型

## Front-end Contribution

至少需要：

```text
电子书实际成交收入
- 内容/版权增量成本
- 平台费率
- 支付
- 售后/退款
- 直接促销成本
= Front-end Contribution
```

数字产品边际交付成本可能低，但：

> 平台费用、退款、版权、内容制作、客服、获客并不等于 0。

## Basket Contribution

如果同单/同会话有：

- 合集；
- 加购；
- 软件；
- 会员；
- 工具；

才进入 Basket。

## True Cohort Contribution

加入：

- 后续书籍；
- 会员；
- AI；
- 知识库；
- 咨询；
- 企业线索；
- Affiliate；

再减：

- CAC；
- 退款；
- 客服；
- 促销滥用；
- 运营；
- 可能的渠道/合规成本。

---

# 7. T01 真实数据门

至少需要询问/标记：

```text
成交价
版权/内容成本
平台费率
退款率
履约与售后成本
CAC
加购率
后端转化率
复购率
会员转化
咨询/企业线索转化
渠道返佣/返点条件
真实Cohort
```

没有这些数据时，允许做三场景模型；不允许直接输出一个精确 LTV。

---

# 8. T01 核心实验

### Experiment A：入口资格

比较：

- 普通低价；
- 有资格围栏/行为门槛的低价；
- 高价值样品/试看；
- 非价格入口。

看：

- Qualified CAC；
- 后端转化；
- 退款/滥用；
- 90/180 天 Cohort。

### Experiment B：后端路径

不同 cohort 分流：

```text
学习型 → 书单/知识库/AI导师
工具型 → 软件/工具/Affiliate
专业型 → 咨询/实施
企业型 → 企业知识库/培训/实施
```

比较下一 Offer 的真实增量贡献。

### Kill Condition 示例

- 90/180 天 True Cohort Contribution 持续小于 0；
- 低价用户与后端目标用户重合度太低；
- 退款/作弊吞噬贡献；
- 后端转化只能靠不合规渠道或不可持续平台规则；
- 促销主要蚕食原本会全价购买的人。

---

# 9. T01 A-E 应观察什么

## A 可能检验

普通模型能想到多少基础直接销售/会员/课程/咨询？

## B

电子书专题是否显著提高机会召回？

## C

通用宇宙是否增加：

- Product Role；
- 价值链；
- 条件经济；
- 竞争/风险；
- 迁移；

而不仅是多几个赚钱点？

## D

Workflow 是否减少：

- 重复建议；
- 无经济模型；
- 无数据门；
- 无实验；
- 无 Kill Condition？

## E

真实项目数据是否改变最终排序？

这是最重要的：

> 如果 E 组只是把 D 写得更长，却没有因为真实数据淘汰/重排方案，说明 Data Gate 没真正工作。

---

# T02：AI API Usage / Commit / Overage 与企业后端

## 10. 原始输入

> **我们提供按调用计费的 AI API，推理成本随用量变化。怎样设计免费额度、commit、overage、渠道和企业后端，避免增长越快亏得越多？**

---

# 11. 为什么 T02 与 T01 结构不同

T01 的核心是：

> 低门槛知识商品 → 高意图用户 → 多后端利润池。

T02 的核心是：

> **变量推理成本 + 用量分布 + Free/Included Usage + Commit/Overage + 企业合同 + 渠道 + 成本风险。**

它能够测试：

- 系统是否真正使用 U10/U12/U13/U14/U18/U19/U21/U26；
- 是否错误地把 AI API 当近零边际成本 SaaS；
- 是否能处理高用量用户负毛利；
- 是否能从消费型入口迁移到企业合同结构。

---

# 12. T02 路由预期

```yaml
primary_family: pricing_offer_portfolio
flags:
  - ai_native
  - enterprise
  - low_price_entry
```

---

# 13. T02 必需能力

至少比较：

- Pure usage-based；
- Free credits + Paid Usage；
- Included Usage + Overage；
- Monthly Minimum / Commit；
- Reserved Capacity；
- Tiered Usage；
- Enterprise Contract；
- Channel/Reseller；
- 混合模型。

必须问：

> 哪个结构把推理成本风险留给谁？

---

# 14. T02 关键经济模型

```text
Revenue per customer
- Model inference COGS
- Other compute/storage/network
- Payment/channel share
- Support
- Fraud/abuse
- Credits/free usage
= Contribution
```

再看：

- Commit Coverage；
- Overage Margin；
- Gross Margin by Usage Decile；
- Heavy-user negative margin；
- Enterprise discount；
- Support burden；
- Working capital；
- Capacity peak。

如果不同模型成本差异很大，还要：

> 按模型/路由拆分，而不是用一个平均“AI 成本”。

---

# 15. T02 真实数据门

至少：

```text
模型真实输入/输出成本
平均与P90/P99 token
每请求成本
缓存命中率
模型路由分布
免费额度使用分布
Free→Paid 转化
Paid 用量分布
渠道分成
退款/坏账
支持成本
企业折扣
账期
最低承诺
峰值容量成本
```

---

# 16. T02 核心失败模式

- Free credits 被脚本/批量账户滥用；
- 高用量用户贡献为负；
- Commit 太低，无法覆盖固定/容量成本；
- Overage 价格低于边际成本 + 风险缓冲；
- 企业折扣 + 渠道分成叠加后 Pocket Price 崩溃；
- 模型供应商涨价或优惠 credits 到期；
- 上下文/输出长度变化导致成本失真；
- 大客户支持成本被忽略；
- 账期使“利润正但现金流危险”。

---

# 17. T02 Kill Condition 示例

- 某用量分位客户连续多个周期贡献为负且无法通过限额/分层修复；
- Free→Paid 的增量贡献无法覆盖 Free COGS；
- 企业净有效价格低于风险调整后的边际成本；
- 供应商 credits/返点消失后模型立刻转负；
- 峰值容量成本使规模扩张越大损失越大。

---

# 十八、T01/T02 不是完整 Benchmark Universe

当前只把它们作为：

> Seed + Cross-domain Canary

后续按覆盖缺口逐步增加：

- 普通电商 SKU；
- 酒店/容量经济；
- Marketplace；
- 企业采购/返点；
- 知识库实施；
- 线下服务；
- 内容创作者。

增加新 Case 的触发器应是：

> **现有 Case 无法覆盖某种关键经济结构或 Workflow 分支。**

而不是为了把 Benchmark 数量做大。
