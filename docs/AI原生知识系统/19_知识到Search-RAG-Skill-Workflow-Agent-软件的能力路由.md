# 知识到 Search / RAG / Skill / Workflow / Agent / 软件的能力路由

> 本文件是 Problem Space 与 Solution Space 之间的桥梁。

它回答：

> 已经知道“这项知识/能力应该交给谁消费”之后，**最小充分的实现载体是什么？**

核心原则：

> **优先选择足以解决问题的最低复杂度能力层，不因 AI 原生而默认 Agent，更不因知识重要而默认软件化。**

---

## 1. 先区分三个层次

### 1.1 Knowledge

回答：

- 知道什么；
- 为什么；
- 什么条件成立；
- 有什么证据与边界。

### 1.2 Capability

回答：

- 能完成什么稳定任务；
- 输入输出是什么；
- 需要哪些判断、状态和动作。

### 1.3 Implementation

回答：

- 用 Search、RAG、Skill、Tool、Workflow、Agent、Automation、Software 还是现成服务承载。

禁止：

> 把知识条目直接命名为 Skill；
> 把多步文字说明直接叫 Agent；
> 把一个 Agent 包上 UI 就自动称为成熟 Software。

---

## 2. 路由前必须观察的变量

至少判断：

- 查询是否可预测；
- 是否以“找到原文”为主；
- 是否需要语义召回；
- 是否需要生成式综合；
- 是否需要显式知识关系；
- 方法是否稳定；
- 输入输出是否稳定；
- 是否需要调用外部工具；
- 是否多步骤；
- 步骤顺序是否稳定；
- 是否存在动态分支；
- 是否需要观察环境；
- 是否有长期状态；
- 是否会产生外部副作用；
- 是否高频；
- 是否多用户；
- 是否需要固定 UI；
- 是否有强业务闭环；
- 是否需要审计、权限、SLA；
- 失败是否可检测、可恢复；
- 生命周期变化速度。

---

## 3. Full-text Search

### 最适合

- 精确关键词；
- 专有名词；
- 错误码；
- 代码/字段；
- 日期/版本号；
- 文档定位；
- 结构化过滤。

### 不负责

- 语义归一；
- 生成答案；
- 判断真伪；
- 自动完成任务。

> 即使未来有强 RAG，全文检索仍然是基础能力，不应被向量检索替代。

---

## 4. Semantic Search

### 最适合

- 用户表达与文档措辞不同；
- 同义改写；
- 跨语言或跨表述召回；
- 去重候选召回；
- 概念相关资料探索。

### 边界

相似度高不代表：

- 命题等价；
- 来源独立；
- 知识正确；
- 可以自动合并。

---

## 5. Hybrid Search

当同时存在：

- 精确术语；
- 语义表达；
- 结构字段；
- 时间/权限/来源过滤；

Hybrid Search 通常比“只做向量搜索”更合理。

它可以作为通用检索层的默认候选，但是否采用仍取决于规模、成本和真实 Benchmark。

---

## 6. Wiki

### 最适合

- 人浏览稳定知识结构；
- 概念导航；
- 主题地图；
- Canonical Knowledge 的人工可读入口；
- 版本、来源、边界与关系展示。

### 不应承担

- 全部自动检索；
- 动态任务执行；
- 把每个原始文档都人工整理成页面。

Wiki 是 **Human Browse Surface**，不是知识系统的全部存储模型。

---

## 7. RAG

### 最适合

- 任务发生时动态获取相关知识；
- 当前不值得人类长期记忆的信息；
- 需要来源引用的问答和综合；
- 长尾、低频但可检索知识；
- 高频变化、需要最新上下文的知识。

### RAG 不解决

- 真伪；
- 来源独立性；
- Canonical Knowledge 身份；
- 人是否值得学习；
- Skill 是否正确；
- 知识是否过期；
- 外部动作权限。

RAG 是**上下文获取与组合机制**，不是知识治理的替代品。

---

## 8. Knowledge Graph

### 最适合

- 显式关系非常重要；
- 需要依赖、因果、上下位、来源、版本、支持/冲突查询；
- 需要跨对象多跳分析；
- 关系本身具有业务价值。

### 不应默认使用

如果主要需求只是全文搜索与问答，不必为了“知识图谱”这个名词先构建复杂图数据库。

当前体系优先保证：

> Canonical ID + typed Relation Assertion

底层是否使用图数据库可以后置。

---

## 9. Skill

Skill 是：

> **稳定、可重复调用、输入输出边界相对清晰的方法、判断规则或微能力。**

适合：

- 需求归一化；
- 固定检查；
- 稳定分类；
- 方法执行；
- 结构提取；
- 可重复决策规则。

Skill 一般不应承担：

- 长期复杂状态；
- 大量开放环境探索；
- 持续自主调度；
- 多阶段项目生命周期。

### Skill 候选必要条件

- 任务反复出现；
- 方法相对稳定；
- 输入/输出可描述；
- 成功/失败可验证；
- 边界和异常可枚举到一定程度。

---

## 10. Tool

Tool 是：

> **对外部系统、数据或确定性计算能力的可调用接口。**

例如：

- 搜索 API；
- 数据库查询；
- 解析器；
- 计算器；
- Git；
- 文件转换；
- OCR；
- 业务系统 API。

知识告诉 AI “怎样判断”，Tool 让系统“真的能做某个操作”。

Tool 与 Skill 可以组合，但不是同义词。

---

## 11. Workflow

Workflow 是：

> **多步骤、顺序/依赖/关口相对稳定的任务图。**

适合：

- 导入 → 清洗 → 提取 → 去重 → 复核 → 发布；
- 固定审批；
- 定期报告；
- 训练/评测流水线；
- 发布前检查。

核心能力：

- step；
- dependency；
- state；
- retry；
- checkpoint；
- human gate；
- error handling。

如果流程可以预先定义为稳定 DAG/状态机，优先 Workflow，而不是 Agent。

---

## 12. Agent

Agent 更适合：

- 必须持续观察环境；
- 下一步不能完全预先枚举；
- 需要根据结果动态规划；
- 存在多分支和不确定路径；
- 需要跨工具推进；
- 有任务状态和恢复需求。

Agent 不是：

> “调用 LLM 的 Workflow”。

### Agent 候选门槛

至少有一项稳定 Workflow 难以经济覆盖的动态性：

- 动态信息搜索；
- 开放问题研究；
- 环境反馈驱动的下一步决策；
- 不确定工具选择；
- 长任务中的重规划。

### Agent 仍必须有外部约束

- budget；
- permission；
- tool allowlist；
- state checkpoint；
- stop condition；
- human gate；
- validation；
- rollback/recovery。

---

## 13. Automation

Automation 强调：

> **事件或时间触发后，系统可靠地重复执行已定义能力。**

它可以承载：

- Workflow；
- Tool；
- 部分 Agent；

但“自动运行”并不自动意味着“Agent”。

适合：

- 定时同步；
- 变更监测；
- 周期报告；
- 到期重验证；
- 触发式知识刷新。

---

## 14. Software / Product

Software 值得建立的信号：

- 高频重复；
- 多用户；
- 固定交互界面价值高；
- 需要长期持久状态；
- 权限/审计复杂；
- 需要 SLA；
- 需要大量集成；
- 需要规模化稳定交付；
- 形成业务闭环；
- 手工/Prompt/Agent 拼装维护成本已明显过高。

软件化不是“最高级路线”，而是满足稳定产品需求后的工程选择。

---

## 15. Existing Tool Integration

当市场已有成熟工具时，必须先问：

- 功能是否已经覆盖；
- 可靠性是否更高；
- 总拥有成本是否更低；
- 数据能否导出；
- 权限/隐私是否可接受；
- 能否接入当前 Canonical Knowledge / Workflow；
- 是否有供应商锁定风险。

如果答案良好：

> 集成 > 重造。

---

## 16. External Service

适合：

- 低频；
- 极高专业门槛；
- 法律/审计/专业责任需要外部主体承担；
- 内部学习与自建成本远高于采购；
- 无长期核心竞争价值。

例如某些法律、医疗、专业检测或审计任务。

外部服务结果仍需保留 provenance、范围和责任边界。

---

## 17. Monitor / Deferred / Ignore

### Monitor

当前不执行，但变化值得监测。

### Deferred

当前无足够价值，保留触发条件。

### Ignore

在当前可预见目标下低价值、低风险、低增量。

Ignore 不是永久删除原始资料；是否删除取决于存储和治理策略。

---

## 18. 关键路由矩阵

| 条件 | 优先候选 |
|---|---|
| 精确定位原文 | Full-text Search |
| 语义表达差异大 | Semantic Search |
| 精确词 + 语义 + 过滤 | Hybrid Search |
| 人需要浏览稳定结构 | Wiki |
| 任务时动态取知识并生成 | RAG |
| 显式关系/多跳分析很重要 | Knowledge Graph |
| 稳定可重复的方法/判断 | Skill |
| 调外部系统/确定性操作 | Tool |
| 多步骤稳定流程 | Workflow |
| 动态环境 + 分支 + 重规划 | Agent |
| 定时/事件重复执行 | Automation |
| 高频 + 状态 + UI + 多用户 + 规模 | Software |
| 市面成熟能力已存在 | Existing Tool Integration |
| 低频高专业门槛 | External Service |
| 当前不做但需要观察 | Monitor |

---

## 19. 能力升级阶梯

默认按以下顺序问：

```text
人是否只需要 Reference？
→ Search 能否解决？
→ Hybrid/RAG 是否足够？
→ 是否只是一个稳定 Skill？
→ 是否需要 Tool？
→ 稳定 Workflow 是否足够？
→ 是否真的需要 Agent 的动态性？
→ 是否值得 Automation？
→ 是否已有成熟工具可集成？
→ 高频规模化是否已经证明 Software 的必要性？
```

这不是严格单向技术层级，而是防止过度工程化的检查顺序。

---

## 20. 同一个需求可能需要组合，不是只能选一个

示例：知识研究助手可能需要：

```text
Hybrid Search
+ Canonical Knowledge Store
+ RAG
+ Evidence Verification Skill
+ Research Workflow
+ 少量 Agentic Search
+ Human Gate
```

但组合前必须说明：

> 每一层分别解决什么问题；如果删除这一层，会失去什么能力。

---

## 21. 09、11、19 三个文件的职责边界

### `09_人与AI分工、替代与能力化.md`

Problem Space：

> 谁应掌握/承担？人、AI、工具、外部服务的可替代性如何？

### `11_知识基础设施与技术方案.md`

Solution Space：

> 整体知识基础设施有哪些技术层？

### 本文件 `19`

Bridge：

> 针对一个已归一化需求/知识/能力，如何在上述实现载体中选择最小充分方案？

三者不得再次合并成一个“AI 能力”概念。

---

## 22. Routing Decision 最小结构

```yaml
implementation_routing:
  route_id: IR-...
  requirement_id: D-...
  knowledge_ids: []
  capability: "cross-source increment detection"

  task_characteristics:
    query_predictability: low
    recurrence: high
    statefulness: medium
    environment_observation: true
    branching: medium
    side_effects: low
    verification: possible

  candidates:
    - type: workflow
      fit: high
      rationale: "主流程稳定"
    - type: agent
      fit: medium
      rationale: "仅开放研究子步骤需要动态探索"

  selected:
    primary: workflow
    adjuncts:
      - hybrid_search
      - skill
      - agent_substep

  rejected:
    - type: software
      reason: "尚未验证多用户与稳定产品需求"

  review_trigger:
    - "usage_frequency_increases"
    - "workflow_branch_explosion"
```

必须记录 rejected alternatives，避免以后只看到结论看不到为什么没有采用更复杂方案。

---

## 23. 能力路由验收

任取一个需求，系统应能回答：

1. 它主要需要知识、检索、判断还是外部动作？
2. Search 能不能解决？为什么？
3. RAG 是否必要？
4. 是否已经稳定到可以做 Skill？
5. 是否需要 Tool？
6. Workflow 能否覆盖大部分路径？
7. 哪一部分动态性才真正需要 Agent？
8. 为什么要或不要 Automation？
9. 是否已有成熟工具可集成？
10. 为什么现在值得或不值得 Software 化？
11. 每个实现层失败时由谁验收、恢复和承担责任？

如果答案只是“建议使用 Agent + RAG + Knowledge Graph”，而没有问题—能力映射，本路由视为失败。