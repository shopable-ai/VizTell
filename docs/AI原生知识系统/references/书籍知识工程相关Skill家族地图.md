# 书籍知识工程相关 Skill 家族地图

> 类型：Reference / Taxonomy
>
> 目的：把网络上与“书籍 → 知识 → 学习 → AI 使用 → 行动”相关的能力拆成稳定家族，方便后续查找 Skill、产品、论文、方案与缺口。
>
> 注意：本文的 SF01–SF12 是**本项目自建分类**，用于分析与架构，不是行业官方标准。

---

## 1. 为什么需要 Skill 家族地图

“把一本书变成有用知识”实际上包含多个完全不同的问题。如果只搜索 `book summary` 或 `book skill`，容易把以下能力混在一起：

- 读懂；
- 压缩；
- 提取；
- 原子化；
- 连接；
- 记忆；
- 批判；
- 行动；
- AI 调用；
- 全库检索；
- 评测。

因此本地图的作用不是指定一种实现，而是先回答：

> **当前需求到底属于哪一种能力家族？**

---

## 2. 12 个 Skill 家族总表

| 编号 | 家族 | 普通语言解释 | 主要解决的问题 | 典型输出 |
| --- | --- | --- | --- | --- |
| SF01 | Book Reader | 帮我读懂这本书 | 书里讲了什么、在哪里、如何回源 | 章节解释、问答、引用 |
| SF02 | Long-text Summarizer | 把长内容压短 | 内容太长、没有时间完整阅读 | 摘要、TL;DR、章节压缩 |
| SF03 | Book Distiller | 只留下最值钱的知识 | 摘要仍然太多，不知道什么重要 | 核心论点、原则、重点 |
| SF04 | Book-to-Skill | 把书变成 AI 能长期调用的能力 | AI 每次重新读书成本高 | SKILL.md、章节索引、模式、规则 |
| SF05 | Atomic Notes | 把知识拆成可独立复用的单元 | 大段笔记以后无法重组和连接 | 原子笔记、永久笔记 |
| SF06 | Knowledge Graph | 把相关知识连接起来 | 知识孤岛、跨资料关系难发现 | 关系、链接、图谱 |
| SF07 | Library Agent | 让 AI 操作整个书库 / 阅读库 | 单文档问答无法处理长期海量资料 | 全库问答、整理、跨文档连接 |
| SF08 | AI Tutor | 像老师一样帮助理解 | 看了但没懂、缺少互动解释 | 教学解释、追问、学习路径 |
| SF09 | Active Recall | 检查是不是真的记得 | 熟悉感误认为掌握 | 卡片、测验、回忆练习 |
| SF10 | Critical Reader | 检查作者可能哪里不成立 | 只接受作者观点、缺少反例和边界 | 假设、盲点、反方、边界 |
| SF11 | Action Extractor | 把“知道”变成“怎么做” | 知识停留在认知层 | 行动清单、触发规则、计划 |
| SF12 | Evaluation Skill | 验证处理后是不是真的更好 | 生成很多资产却不知道有没有用 | baseline、测试集、质量指标 |

---

## 3. SF01 Book Reader：书籍阅读与来源问答

### 核心需求

> 我需要快速理解书里的某个内容，并且知道答案来自哪里。

### 典型输入

- PDF；
- EPUB；
- Markdown；
- 某章；
- 用户关于书的具体问题。

### 典型输出

- 章节结构；
- 局部解释；
- 书内问答；
- 原文位置；
- 引用。

### 代表机制

- document parsing；
- chunking；
- source-grounded QA；
- chapter routing；
- citation。

### 不解决

- 这条知识是否值得长期保存；
- 与其他书是否重复；
- 是否已经掌握；
- 是否应该变成行动。

---

## 4. SF02 Long-text Summarizer：长文本压缩

### 核心需求

> 内容太多，我需要先获得低成本概览。

### 典型输出

- TL;DR；
- 章节摘要；
- 分层摘要；
- Map-Reduce / hierarchical summary。

### 价值

适合作为低成本入口、筛选和阅读前预览。

### 风险

- 压缩损失条件和边界；
- 将作者修辞与事实混在一起；
- 摘要看似完整但无法支持迁移和执行。

---

## 5. SF03 Book Distiller：核心知识蒸馏

### 核心需求

> 我不是只想知道作者说了什么，而是想知道真正值得保留的是什么。

### 典型输出

- 核心论点；
- 少量高价值原则；
- 关键模型；
- 高杠杆观点；
- 可跳过内容。

### 代表机制

- value filtering；
- thesis extraction；
- principle extraction；
- prioritization。

### 与普通摘要的区别

```text
摘要：把全部内容变短
蒸馏：允许主动丢弃低价值内容，只保留高价值结构
```

---

## 6. SF04 Book-to-Skill：书籍到 Agent Skill

### 核心需求

> 让 AI 以后在真实任务中按需使用一本书的方法，而不是每次重新读整本书。

### 典型输出

```text
SKILL.md
references/
chapters/
patterns.md
glossary.md
cheatsheet.md
```

### 代表机制

- framework extraction；
- decision rules；
- anti-patterns；
- routing；
- progressive disclosure；
- on-demand references。

### 代表项目

- virgiliojr94/book-to-skill；
- Londeren/book-to-skill。

### 不解决

Book-to-Skill 是一种**能力化出口**，不是所有书籍默认目标。

一本故事型、低密度或高度重复书籍可能根本不值得转 Skill。

---

## 7. SF05 Atomic Notes：原子知识 / 永久笔记

### 核心需求

> 大段读书笔记未来难以重组，我需要一条一条可独立理解和连接的知识。

### 典型原则

- one idea per note；
- self-contained；
- own words；
- source link；
- meaningful connections。

### 代表体系

- Zettelkasten；
- Atomic Notes；
- Permanent Notes。

### 与本项目 Knowledge Atom 的区别

`Atomic Note` 主要是一种笔记 / 思考组织方式；

`Knowledge Atom` 是系统中的知识对象，还可能承担：

- 类型；
- 来源；
- 条件；
- 证据；
- 关系；
- 时间；
- Canonical Resolution。

二者可以映射，但不应直接等同。

---

## 8. SF06 Knowledge Graph：知识关系与图谱

### 核心需求

> 不同知识之间究竟有什么关系？

### 典型关系

- related_to；
- supports；
- contradicts；
- refines；
- example_of；
- depends_on；
- supersedes。

### 代表机制

- explicit links；
- knowledge graph；
- concept graph；
- semantic relation extraction。

### 风险

> 图谱边很多不等于知识质量高。

图谱必须建立在正确知识身份和关系裁决之上，否则会把噪声结构化。

---

## 9. SF07 Library Agent：全库 Agent

### 核心需求

> 当资料很多以后，我不想再逐个文件打开，我要直接和整个知识库交互。

### 典型能力

- library-wide search；
- cited QA；
- find similar；
- cross-document synthesis；
- tagging / organization；
- metadata actions；
- whole-library agent context。

### 代表方案

- Readwise Global Ghostreader；
- Recall whole-KB chat；
- 其他基于 MCP / RAG 的 personal knowledge agents。

### 关键边界

Library Agent 不应绕过：

- provenance；
- evidence；
- permission；
- version；
- knowledge identity；
- context budget。

---

## 10. SF08 AI Tutor：AI 导师

### 核心需求

> 我不只是要结果，我需要根据自己的理解状态逐步学会。

### 典型能力

- section-by-section teaching；
- explanation；
- Socratic questions；
- prerequisite repair；
- targeted follow-up；
- personalized study path。

### 代表方案

- RemNote Guided Learn；
- NotebookLM 的来源型学习辅助。

### 与摘要区别

AI Tutor 的目标是改变主体状态，而不是生成一份静态内容。

---

## 11. SF09 Active Recall：主动回忆与掌握验证

### 核心需求

> 我感觉自己懂了，但在没有原文时到底能不能提取和应用？

### 典型能力

- flashcards；
- free recall；
- quiz；
- spaced repetition；
- weak-topic detection；
- targeted follow-up。

### 对接本项目

可以支持 H1–H3 的部分验证，但：

> 选择题 / 卡片成绩不能直接证明 H4 执行、H5 适应、H6 迁移和 H7 教学 / 设计。

---

## 12. SF10 Critical Reader：批判性阅读

### 核心需求

> 作者说得很有道理，但这是真的吗、在什么情况下不成立？

### 典型输出

- hidden assumptions；
- missing evidence；
- alternative explanation；
- counterexample；
- edge case；
- strongest critic；
- outdated claim。

### 代表模式

- Blind Spot Finder；
- Debate Mode；
- claim / evidence audit。

### 关键纪律

外部反驳和作者原观点必须分开标记，不能把模型自己的批评伪装成书中内容。

---

## 13. SF11 Action Extractor：知识到行动

### 核心需求

> 读完以后到底应该改变什么行为？

### 典型输出

```text
触发场景
→ 判断条件
→ 应采取行为
→ 不应采取行为
→ 反馈信号
```

或：

```text
IF situation X
THEN behavior Y
```

### 风险

- 不是所有知识都适合行为化；
- 把观点改写成命令可能放大错误；
- 行为成败不能只由是否执行判断，还需检查环境和知识本身。

---

## 14. SF12 Evaluation Skill：知识 / Skill / 学习效果评测

### 核心需求

> 做了摘要、Skill、知识库、练习以后，到底有没有产生增益？

### 典型评测

- no-skill baseline；
- source-grounding accuracy；
- retrieval quality；
- transfer task；
- delayed retention；
- behavior outcome；
- token / latency / cost；
- regression test。

### 关键原则

```text
“生成成功” ≠ “知识正确”
“知识正确” ≠ “人已掌握”
“人已掌握” ≠ “能迁移”
“Skill 能加载” ≠ “AI 任务表现更好”
```

---

## 15. 12 个家族之间的关系

它们不是平级工具清单，更像不同阶段 / 消费方式：

```text
                    原始书籍
                       ↓
             SF01 Reader / SF02 Summary
                       ↓
                 SF03 Distiller
                       ↓
                SF05 Atomic Notes
                       ↓
                SF06 Knowledge Graph
                  ↙               ↘
       人类学习路线                 AI 使用路线
       SF08 Tutor                  SF04 Book-to-Skill
       SF09 Recall                 SF07 Library Agent
       SF10 Critical              Search / RAG / Agent
       SF11 Action                  ↘
                  ↘               ↙
                     SF12 Evaluation
```

这张图只是能力家族关系图，不等于正式运行顺序。

---

## 16. 从家族到本项目的能力缺口

12 个家族仍不能自动覆盖本项目完整需求。需要额外的上层知识工程能力：

- Source Provenance；
- Claim / Knowledge ID；
- Canonical Knowledge；
- Same / Support / Conflict / Refine / Boundary 等关系裁决；
- Knowledge Delta；
- evidence independence；
- time / version；
- subject value；
- Human / AI / Tool consumption routing；
- lifecycle governance。

因此更合理的目标不是打造一个越来越大的 Book Skill，而是：

> **用书籍知识工程工作流编排多个 Skill 家族与底层知识能力。**

---

## 17. 使用方式

以后遇到新的网络 Skill、产品或论文时，不要立即新增一个一级体系。

先问：

1. 它主要解决 SF01–SF12 中哪个问题？
2. 是否只是旧能力的新实现？
3. 它新增了什么此前没有的能力？
4. 新能力属于知识工程、学习、AI 消费还是评测？
5. 是否需要扩展 taxonomy，还是只增加一个代表方案？

相关研究证据见：

`../research-notes/2026-08-26_书籍知识工程外部Skill与产品生态研究.md`
