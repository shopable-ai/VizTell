# 商业模式宇宙 v3：Skill 增量协议

> 在 v2 `03_商业模式宇宙_元数据知识图谱与Skill协议.md` 基础上增加经济真相、治理、容量、风险、公共激励、财资、合同和劳动力分析。

## 一、必须新增的输入/输出对象

```yaml
ownership_governance:
  asset_owner:
  ip_owner:
  data_owner:
  customer_relationship_owner:
  voting_control:
  residual_claimant:

accounting_truth:
  gmv:
  gross_billings:
  principal_or_agent:
  recognized_revenue:
  net_revenue:
  gross_profit:
  contribution_margin:
  cash_collected:
  free_cash_flow:

capacity_economics:
  physical_capacity:
  sold_capacity:
  used_capacity:
  utilization:
  breakage:
  cancellation:
  no_show:
  overbooking:
  spoilage:

risk_transfer:
  risk_owner:
  premium:
  deductible:
  guarantees:
  reserves:
  reinsurance_or_hedges:

public_economics:
  grants:
  subsidies:
  tax_credits:
  government_procurement:
  policy_expiry_risk:

treasury:
  float:
  interest:
  fx_spread:
  settlement_delay:
  working_capital:
  financing_structure:

contract_economics:
  minimum_commitment:
  take_or_pay:
  auto_renew:
  early_termination:
  exclusivity:
  mfn:
  options:
  buyback:
  audit_right:
  sla_credits:

labor_economics:
  labor_model:
  fixed_vs_variable:
  compensation:
  commission:
  revenue_share:
  quality_incentives:
  classification_risk:

market_design:
competitive_response:
metrics:
experiments:
```

## 二、新增 Skills

- `principal-agent-classifier`：识别交易控制权，防止把 GMV/Gross 错当净收入。
- `economic-truth-waterfall`：GMV → Billings → Revenue → Net Revenue → Gross Profit → Contribution Margin → Cash → FCF。
- `capacity-economics-analyzer`：分析利用率、Breakage、No-show、Overbooking、Spoilage。
- `risk-transfer-designer`：识别风险拥有者、保证、保险、再保险、准备金和对冲。
- `public-incentive-extractor`：提取补助、税收抵免、政府采购、担保和政策期限。
- `treasury-economics-analyzer`：分析 Float、利息、FX、结算周期、营运资金和融资结构。
- `contract-economics-extractor`：抽取最低承诺、Take-or-pay、续约、退出、MFN、排他、期权、回购和 SLA。
- `labor-model-analyzer`：分析员工、外包、Gig、加盟、佣金、分成与质量激励。
- `competitive-response-simulator`：模拟竞争者、渠道、供应商和用户对新模式的反应。

## 三、推荐候选模式的强制输出

```text
谁拥有？
谁控制？
谁承担风险？
谁获得剩余利润？
GMV/收入/净收入/贡献利润各是多少？
容量利用率发生变化时模型是否反转？
是否依赖政府、税收或补贴？
Float/FX/账期是否贡献或吞噬利润？
合同最低承诺、退出、回购和 SLA 的最坏情形是什么？
谁真正完成工作，劳动成本是否可规模化？
竞争对手复制后还剩什么优势？
用什么 KPI 和实验验证？
```
