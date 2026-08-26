# 检测器测试集、误报漏报与 Benchmark

> 核心目标：证明某个专业检查方法或 AI Checker **真的能区分问题、正常情况和边界情况**，而不是只会在可疑文本上生成听起来合理的批评。

正式全系统 Benchmark 框架仍由 `../13_评测、Benchmark与质量指标.md` 与 `../22_遗漏、反例与回归测试.md` 负责；本文件保存 01E Checker 专用测试协议。

---

## 一、每个 Checker 的最小测试宇宙

必须同时包含：

```text
True Positive (TP)
真正有目标问题，正确报警

False Positive (FP)
本来合理，却被错误报警

True Negative (TN)
正常内容，正确不报警

False Negative (FN)
真正有问题，却没有发现

Boundary Case
表面相似，是否有问题取决于额外条件

Insufficient Evidence
当前材料不足，正确答案是暂不能判断

Abstain
系统知道不应继续自动裁决，并正确升级核验/人工
```

禁止只有 TP 案例。

---

## 二、为什么 False Positive 是 01E 的核心风险

错误筛选系统很容易变成：

```text
看到专家 → “诉诸权威”
看到故事 → “故事冒充证据”
看到情绪 → “操纵”
看到相关 → “没有因果”
看到比喻 → “事实错误”
看到小样本 → “研究无效”
看到非零轴 → “图表造假”
```

这会把批判性思维退化成“自动挑错”。

因此 FP 不只是普通错误，而是 01E 第一阶段的一票重点风险。

---

## 三、谬误谬误 Benchmark

F02/F05/F06 至少覆盖：

### 合理专家意见

专家领域相关、引用准确、有可核查证据。

**禁止结果**：仅因出现专家身份就判“诉诸权威谬误”。

### 合理类比

类比只帮助理解，没有被当成直接证明。

**禁止结果**：看到 analogy 就判无效推理。

### 合理人身可信度

当前任务就是评价证人/专家可靠性。

**禁止结果**：所有人物可信度信息都判 ad hominem。

### 真正二选一

现实约束确实只剩两个互斥选项。

**禁止结果**：机械判 false dilemma。

---

## 四、因果 Benchmark

F08 至少包含：

| Case | Gold |
| --- | --- |
| 仅观察相关，却写“导致” | TP |
| 文本明确说“只能说明相关” | TN |
| 有相关数据 + 强 RCT/自然实验支持 | 不得仅凭“相关”否定因果 |
| 时间顺序不清 | `insufficient_information` / risk |
| 反向因果有明确机制 | TP risk |
| 合理调整 confounder | 不得误判 collider |
| 控制真正 collider | TP risk |
| 必要条件被写成充分条件 | TP |

---

## 五、测量与研究设计 Benchmark

F09/F10 必测：

- 代理指标明显不代表目标构念；
- 代理指标已有充分验证；
- 样本小但作者只作探索性结论；
- 小样本却被宣传成确定普遍规律；
- 非随机研究但有合理准实验识别；
- 缺失数据可能强烈影响结果；
- 失访较少且稳健性分析充分；
- 使用 reporting checklist 但研究方法仍有偏倚；
- 报告不完整导致无法判断，而不是自动判错。

---

## 六、统计与图表 Benchmark

F11/F12 必测：

### 数字

- 百分比无分母；
- 相对风险大但绝对变化极小；
- 同时清楚报告相对和绝对风险；
- p < 0.05 被写成“效果很大”；
- 不显著被写成“证明完全无效”；
- 多重比较已经合理校正。

### 图表

- 柱状图截断轴放大差异；
- 折线图合理使用非零轴；
- 对数轴清楚标注且合理；
- 双轴人为制造走势重合；
- 双轴仅用于不同单位且没有暗示关联；
- 气泡面积与数值明显不成比例；
- 3D 真正表示空间数据。

---

## 七、来源与证据 Benchmark

F13—F16 必测：

- 十篇网页实际来自同一研究；
- 多来源确实独立；
- 二手来源准确忠实总结 primary；
- 二手来源把“相关”改成“因果”；
- 一篇高质量研究但 evidence body 尚不稳定；
- 系统综述方法弱；
- Meta-analysis 合理说明不确定性；
- 撤稿因数据不可靠；
- 撤稿因出版/作者问题但核心 Claim 未因此自动证伪；
- 无证据与已反驳分开。

---

## 八、修辞与认知偏差 Benchmark

F19/F20 必测：

- 高风险安全警告使用强烈语言但证据充分；
- 情绪强但事实层完整；
- 情绪替代证据；
- 专家声誉与 Claim 真正相关；
- 社会证明被当真实性证明；
- 故事只是教学；
- 故事替代总体数据；
- 利益冲突存在但结果可独立验证；
- 不应从一段文本诊断某人“有 Dunning–Kruger”。

---

## 九、边界、迁移与增量 Benchmark

F21/F22 必测：

- 原研究条件被二手内容删除；
- 条件不同但已有跨场景独立复现；
- 同义改写没有知识增量；
- 文本高度相似但新增关键边界；
- 相同 Claim 获得新独立证据；
- 同原则新教学案例；
- 新案例是反例，改变原模型；
- 文学/情绪内容不以 Canonical Increment 作为唯一价值标准。

---

## 十、AI 转换失真 Benchmark

F24 必测：

- 摘要正确保留条件和不确定性；
- “可能”被摘要成“会”；
- 相关被摘要成因果；
- 两个冲突来源被合并成单一结论；
- 引用错配；
- AI 补出原文没有的机制；
- 译文专业术语变化导致 Claim 改变；
- 原文明确是比喻，摘要变成字面事实。

---

## 十一、Benchmark Case Schema

```yaml
benchmark_case:
  case_id: 01E-F08-SYN-001
  checker_id: F08
  case_type: TP|FP|TN|FN|BOUNDARY|INSUFFICIENT|ABSTAIN
  input:
    text: "..."
    context: "..."
  source_ref:
  real_case_ref:
  expected:
    status:
    findings: []
    missing_information: []
    next_action:
  allowed_judgements: []
  forbidden_outcomes: []
  severity_if_failed:
  rationale:
  reviewed_by:
  version:
```

Synthetic Case 可以没有真实 `source_ref`，但必须明确标 `SYN`；真实 Case 必须可回到真实材料。

---

## 十二、Forbidden Outcomes 必须存在

例如专家意见边界案例：

```yaml
forbidden_outcomes:
  - call_appeal_to_authority_only_because_expert_is_mentioned
  - mark_claim_false_without_checking_evidence
```

因果案例：

```yaml
forbidden_outcomes:
  - claim_causality_is_impossible_only_because_observational_correlation_exists
  - invent_unobserved_confounder_as_fact
```

这样 Benchmark 不只奖励“提到了正确关键词”，还约束典型错误路径。

---

## 十三、核心指标

### 基础分类

- Precision / PPV；
- Recall / Sensitivity；
- Specificity；
- F1；
- FP Rate；
- FN Rate。

### 01E 专用

#### Overclaim Rate

`risk_signal / insufficient_information` 被错误升级成 `confirmed_issue` 的比例。

#### Appropriate Abstention Rate

该拒判/升级人工的案例中，系统正确拒判的比例。

#### Wrong Forced Judgment Rate

证据不足却强行输出确定结论的比例。

#### Missing-information Recall

是否发现真正阻碍裁决的关键信息。

#### Critical-question Coverage

论证模式中关键 Critical Questions 是否覆盖。

#### Source-tracing Accuracy

是否追到正确 primary source / lineage。

#### Citation-fidelity Accuracy

是否正确发现引用与当前 Claim 的强度差异。

---

## 十四、严重度不能被平均准确率掩盖

错误至少分：

```text
low
medium
high
critical
```

例如：

- 把合理比喻误报一次：通常低/中；
- 医疗证据不足却自动判“已证明有效”：高/critical；
- 把真实法律判例判成虚构并自动阻断：高；
- 错删企业核心 Canonical Knowledge：critical。

高风险错误可以一票否决某 Checker 的自动 Act 权限。

---

## 十五、Synthetic → Controlled Real → Scale

建议测试顺序：

```text
B1 Synthetic Checker
→ B2 Synthetic Multi-checker
→ B3 Controlled Real Cases
→ B4 Scale / Cost / Human-review Load
→ B5 Longitudinal User Outcome
```

与现有 `13` 对齐。

不要一开始扫描海量真实书库来“看看效果”。

---

## 十六、Gold 的形成

### 规则清晰案例

规则 + 人工核查即可。

### 语义/因果/研究边界

优先：领域专家 Gold + 公开来源 + 允许多个合理状态。

### 高争议问题

Gold 可以是：

```text
contested
insufficient_information
allowed_judgements: [A, B]
```

不要制造虚假的单一真值。

---

## 十七、真实案例与 Benchmark 分离

`20` 中的真实案例只有满足 Gate 才进入本文件。

真实案例可以是很好的研究材料，但如果：

- 上下文未固定；
- 最新事实未复核；
- Gold 本身高度争议；

就不能直接拿来测准确率。

---

## 十八、回归触发器

以下变化应重跑对应 01E Regression Set：

- Checker Prompt /规则；
- LLM / Vision Model；
- Search / Reranker；
- Argument Scheme taxonomy；
- evidence thresholds；
- OCR / parsing；
-图表识别；
- Source tracing；
- 新增专业领域；
- F01—F24 合并/拆分；
- 自动 Act 权限；
- Checker orchestration route。

---

## 十九、第一阶段验收

任一 Checker 如果只有：

> “在 10 个明显错误案例上都能指出问题”

仍然不通过。

至少需要证明：

1. 能发现目标问题；
2. 能放过合理相似结构；
3. 信息不足时能停；
4. 不会把风险信号升级成事实；
5. 能指出真正缺失信息；
6. 高风险错误受控；
7. 真实案例上保持可解释和可复查。
