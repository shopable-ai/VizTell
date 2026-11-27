# 02 · BMAD 理解与实操

> 状态：固定版本源码机制已定向核查；真实 Codex 实操未完成。本文是源码研究稿，不是实验完成报告。

## 1. 它解决什么问题

BMAD 不只是“几个 AI 专家角色”，而是把专业角色、工作流、项目配置、阶段产物和持久化记忆组织起来的方法。

它主要回答：

- 一个研发目标应该由什么专业视角处理。
- 如何从初始想法进入 PRD、SPEC、架构和实现。
- 不同阶段如何读取同一套项目约束和配置。
- 如何记录决定，避免换会话后重新猜测。
- 如何根据任务规模选择轻量或完整工作流。
- 如何审核实现并恢复未完成任务。

## 2. Agent、Skill、Workflow 的关系

### Agent：专业工作视角

固定版本的 BMM Agent roster 包括：

- Mary：Business Analyst。
- John：Product Manager。
- Sally：UX Designer。
- Winston：System Architect。
- Amelia：Senior Software Engineer。

定义位于 src/bmm-skills/agents/ 下的 SKILL.md 和 customize.toml。

Agent Skill 会要求模型解析角色配置、采用角色身份、加载持久化事实、显示菜单，并将明确请求路由到对应 Skill。

**Agent Skill 本身是一份角色行为定义，不自动意味着启动了独立 Agent 进程。** 同一会话里的模型可以只是切换了角色视角。

### Skill：能力入口

例如：

- bmad-prd：创建、更新或验证 PRD。
- bmad-spec：把想法、Brief、PRD 或混合材料收敛为 SPEC。
- bmad-architecture：技术架构设计。
- bmad-build：把实现意图转为可审核、可验证的代码变更。
- bmad-party-mode：组织多个角色参与讨论。

### Workflow：具体执行步骤

一个工作流 Skill 可能包含：

- SKILL.md：入口与调用规则。
- customize.toml：可配置路径、审核层和行为。
- workflow.md：总体执行流程。
- step-*.md：按需逐步加载的说明。
- scripts：配置解析、文件生成和记忆写入等程序工具。

关系可以理解为：

~~~text
用户提出目标
   ↓
宿主发现并调用 Skill
   ↓
必要时采用 Agent 专业视角
   ↓
Workflow 确定执行阶段
   ↓
步骤文件 + 项目配置 + 持久化记忆
   ↓
需求、代码、测试和审核产物
~~~

## 3. 从初始想法到 PRD 或 SPEC

BMAD v6.12.4 有两条不同路径。

### 路径 A：bmad-prd

源码：[bmad-prd/SKILL.md](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.4/src/bmm-skills/plan/bmad-prd/SKILL.md)

它负责较完整的产品需求发现：

1. 收集用户想法和已有材料。
2. 校准项目风险和工作规模。
3. 选择 Fast path 或 Coaching path。
4. 发现用户、业务、功能、非功能和领域约束。
5. 形成 PRD，技术细节和长篇论证可放 addendum.md。
6. 通过审核者检查需求质量。
7. 处理开放问题，完成 PRD。

PRD 重点回答产品为什么存在、为谁解决什么问题、需要提供哪些能力、怎样衡量成功。

### 路径 B：bmad-spec

源码：[bmad-spec/SKILL.md](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.4/src/bmm-skills/plan/bmad-spec/SKILL.md)

它是更轻量的意图收敛器。输入可以是想法、Brief、PRD、RFC、聊天记录或混合材料。

五字段核心：

1. Why：为什么需要。
2. Capabilities：需要具备什么能力。
3. Constraints：哪些约束会影响设计。
4. Non-goals：明确不做什么。
5. Success signal：什么结果可以证明目标实现。

SPEC.md 是下游工作流使用的机器契约；较长的术语、状态机、失败模式和设计材料可放 companion 文件。

## 4. Memlog 怎样保存决定

源码：[memlog.py](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.4/src/scripts/memlog.py)

Memlog 是追加式、按时间排序的工作记忆文件，通常名为 .memlog.md。它记录：

- 用户选择了什么方案以及原因。
- 已确认的约束和假设。
- 仍未解决的问题。
- 需求变化和重要事件。
- 当前工作的阶段性事实。

脚本提供 init、append 和 set 命令。其程序特性包括：

- 记录追加到文件末尾，不重排历史。
- 写入先到临时文件，flush、fsync 后原子替换。
- 不提供任意编辑或删除历史记录的命令。
- 写入后返回 JSON 回执。
- 恢复时由调用方重新读取日志。

### Memlog 与 SPEC.md 的关系

~~~text
用户输入与讨论
   ↓
每次确认的决定、约束、能力追加到 .memlog.md
   ↓
bmad-spec 读取日志及来源材料
   ↓
重新推导 SPEC.md 和 companion 文件
   ↓
下游工作流读取统一需求契约
~~~

SPEC.md 从 .memlog.md 推导，不应随意手工修改。更新需求时追加决策，再重新生成 SPEC。

PRD 工作流也使用 .memlog.md，但记录 PRD 讨论和决策；不要把 PRD 的记忆日志与 SPEC 的规范推导生命周期混为一谈。

## 5. bmad-build 如何选择 Oneshot / Dispatch

源码：

- [bmad-build Skill](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.4/src/bmm-skills/ship/bmad-build/SKILL.md)
- [Build Workflow](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.4/src/bmm-skills/ship/bmad-build/workflow.md)
- [Step 02 Plan](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.4/src/bmm-skills/ship/bmad-build/step-02-plan.md)

bmad-build 入口会先运行：

~~~bash
uv run --no-cache "<project-root>/_bmad/scripts/render_skill.py" --project-root "<project-root>" --skill "<skill-root>"
~~~

成功后读取命令输出的 workflow.md，按工作流继续。渲染器会把 Skill 的步骤文件、配置值和引用解析成不可变快照，并记录输入与输出哈希。

### Oneshot：小而明确

当调查后确认没有用户必须回答的需求缺口、没有不可逆操作、改动范围较小，选择 Oneshot。

它使用精简 SPEC，由当前代理实施，但仍需运行配置的审核层。Oneshot 不等于无审核或免测试。

### Dispatch：存在不确定性或规模较大

如果存在需求缺口、不可逆操作或较大实施范围，则生成完整 SPEC，解决开放问题并等待用户批准，再实施。

典型步骤：

1. 调查代码库和已有资料。
2. 形成包含 Code Map、Open Questions、Tasks & Acceptance 的 SPEC。
3. 用户回答开放问题并批准。
4. 默认派发无先前对话上下文的 Implementer Subagent。
5. 主代理检查 Diff 和验收条件。
6. 运行配置的审核层。
7. 修复、验证并记录变更。
8. 完成后提交并汇报。

没有 Subagent 工具时，工作流允许主代理直接实施；不能因此宣称完成了真实 Subagent 实验。

Oneshot 若发现新需求缺口、不可逆操作或规模增长，必须停止当前实现、更新 SPEC 并转为 Dispatch。

## 6. Party Mode 是角色模拟还是真实 Agent

源码：

- [Party Mode Skill](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.4/src/core-skills/bmad-party-mode/SKILL.md)
- [Subagent Mode](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.4/src/core-skills/bmad-party-mode/references/mode-subagent.md)
- [Auto Mode](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.4/src/core-skills/bmad-party-mode/references/mode-auto.md)

BMAD 明确区分：

| 模式 | 含义 | 独立 Agent |
|---|---|---|
| session | 一个模型在当前上下文扮演多个角色 | 否 |
| auto | 默认当前会话发言，必要时派发独立 Agent | 视轮次而定 |
| subagent | 每个角色由真实 Subagent 独立思考 | 是，前提是宿主支持 |
| agent-team | 持续存在、角色之间直接交流的团队 | 仅 Claude Code 支持 |

所以 Party Mode 不能一概说成多个真实专家 Agent。看到不同角色轮流发言，只能证明角色表达发生变化，不能证明独立进程或独立上下文。

如果宿主没有 Subagent 能力，BMAD 会退回 session 模式。

## 7. 中断后怎样恢复

BMAD 主要依赖三类事实：

- SPEC 状态：draft、ready-for-dev、in-progress、in-review、done；还可记录 route、baseline_commit、review_loop_iteration。
- Memlog：保留决策、约束和需求变化。
- 工作流产物：Code Map、Implementation Notes、Spec Change Log、Review Triage Log、测试结果。

重新调用工作流时，它先检查明确传入的文件、近期对话和活动 SPEC，再选择从规划、实施或审核步骤恢复。

恢复实验必须真正中断一次，再启动新会话读取这些文件。仅仅看到状态字段存在，不等于恢复能力已验证。

## 8. 程序保证与模型判断的边界

| 能力 | 性质 | 说明 |
|---|---|---|
| 安装 Skill 和共享配置 | 安装器 | 创建宿主 Skill 文件和项目配置 |
| 配置合并 | 脚本 | 合并基础、团队和用户配置 |
| Workflow 渲染 | 脚本 | 生成带配置和哈希的快照 |
| Memlog 追加 | 脚本 | 原子写入日志 |
| 需求是否充分 | 模型判断 | 仍需审核判断依据 |
| Oneshot / Dispatch 路由 | 模型判断 | 工作流规定标准，但不是独立规则引擎 |
| Agent 角色表达 | 模型指令 | 不自动产生独立进程 |
| Subagent 独立性 | 宿主运行时 | 必须看到真实 Agent 调用 |
| 代码正确性 | 测试、审核和运行结果 | SPEC 或自述不能保证 |

## 9. 本轮实验状态与证据位置

统一案例见 shared/CASE.md。计划位置：

- experiments/bmad/oneshot/：小任务路径。
- experiments/bmad/dispatch/：若受控实验触发 Dispatch，保留 SPEC、实施和审核过程。
- experiments/bmad/party-mode/：session 与真实 Subagent 对照。
- evidence/bmad/：渲染快照、Memlog、Agent 调度、恢复和测试记录。

当前没有实际安装或运行 BMAD，也没有真实生成 SPEC、Memlog、Workflow 快照或 Agent 回执。源码说明不能替代实验。

## 10. 关键源码

- [安装指南](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.4/docs/start/install-bmad.md)
- [Core Module](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.4/src/core-skills/module.yaml)
- [BMM Module 与 Agent roster](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.4/src/bmm-skills/module.yaml)
- [PM Agent](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.4/src/bmm-skills/agents/bmad-agent-pm/SKILL.md)
- [Architect Agent](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.4/src/bmm-skills/agents/bmad-agent-architect/SKILL.md)
- [PRD Skill](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.4/src/bmm-skills/plan/bmad-prd/SKILL.md)
- [SPEC Skill](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.4/src/bmm-skills/plan/bmad-spec/SKILL.md)
- [Build Skill](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.4/src/bmm-skills/ship/bmad-build/SKILL.md)
- [Workflow Renderer](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.4/src/scripts/render_skill.py)
- [Memlog](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.4/src/scripts/memlog.py)
