# 01 · Superpowers 理解与实操

> 状态：固定版本源码机制已定向核查；真实 Codex 实操未完成。本文是源码研究稿，不是实验完成报告。

## 1. 它解决什么问题

Superpowers 主要解决“AI 编码代理怎样按可靠的软件工程纪律工作”，而不是替用户完整承担产品经理、业务分析师或系统架构师职责。

它把研发方法拆成可被宿主发现和加载的 Skills，覆盖需求澄清、设计、实施计划、TDD、调试、代码审核、任务恢复和交付验证。

## 2. 安装后为什么能影响 AI

v7.0.2 的 Codex 插件清单位于 [plugin.json](https://github.com/obra/superpowers/blob/v7.0.2/.codex-plugin/plugin.json)，其中声明插件版本和 Skills 目录。

关键入口是 [using-superpowers/SKILL.md](https://github.com/obra/superpowers/blob/v7.0.2/skills/using-superpowers/SKILL.md)。它要求代理在开始对话或行动前检查并调用适用 Skill；Brainstorming 则要求在创造性工作和功能开发前先理解需求。

影响链路是：

1. 宿主安装插件并注册 Skill 目录。
2. 宿主发现 Skill 的名称和描述。
3. 自然语言任务与 Skill 描述匹配时，宿主/模型选择加载对应 Skill。
4. Skill 正文进入代理上下文，指导后续行为。
5. 代理遵循规则并调用可用工具。

**这不是模型权重重新训练，也不是确定性策略引擎。** Skill 的规则大多是模型指令；只有辅助脚本、文件操作、测试命令和宿主能力本身能提供可独立核验的程序行为。

Codex 插件清单中的 hooks 当前为空（hooks: {}）。仓库另有 SessionStart Hook 文件，不能因此推断 Codex 一定会执行该 Hook。自然语言是否触发 Skill，必须在真实 Codex 会话中看工具调用和加载记录。

## 3. 从原始需求到研发交付

### 3.1 Brainstorming：理解真正需求

源码：[brainstorming/SKILL.md](https://github.com/obra/superpowers/blob/v7.0.2/skills/brainstorming/SKILL.md)

它要求先查看用户已提供的资料和现有项目，避免重复询问。对非简单需求，流程是：

1. 理解用户想解决什么、为什么。
2. 提出真实可行的实现路径，说明取舍并给出建议。
3. 编写设计文档。
4. 等用户批准设计文档。
5. 批准后才进入 Writing Plans。

设计默认保存到 docs/superpowers/specs/YYYY-MM-DD-主题-design.md。

**设计批准门槛是 Skill 对模型的明确要求，不是程序级文件写入锁。** 必须实验观察模型是否真的在批准前停止写产品代码、脚手架和依赖。

### 3.2 Writing Plans：将设计转成任务

源码：[writing-plans/SKILL.md](https://github.com/obra/superpowers/blob/v7.0.2/skills/writing-plans/SKILL.md)

默认输出 docs/superpowers/plans/YYYY-MM-DD-功能名.md。

计划需要具体到：

- 创建/修改/测试的准确文件路径。
- 任务依赖、接口、输入输出和全局约束。
- 每一步执行的测试命令。
- 预期的失败或成功结果。
- 每个任务可独立检查的完成条件。

它不是泛泛的“实现按钮”，而是让没有参加需求讨论的工程师也能按步骤执行。

### 3.3 TDD：先证明测试能失败

源码：[test-driven-development/SKILL.md](https://github.com/obra/superpowers/blob/v7.0.2/skills/test-driven-development/SKILL.md)

RED → GREEN → REFACTOR：

1. 写一个描述正确行为的测试。
2. 运行测试，确认它因目标功能缺失而失败。
3. 写最小实现。
4. 再运行测试，确认通过。
5. 在测试保持通过的前提下重构。

关键不是“最后有测试”，而是保存测试先失败、后通过的真实输出。语法错误、依赖缺失或测试配置错误不算有效 RED。

### 3.4 审核和完成前验证

源码：

- [verification-before-completion](https://github.com/obra/superpowers/blob/v7.0.2/skills/verification-before-completion/SKILL.md)
- [subagent-driven-development](https://github.com/obra/superpowers/blob/v7.0.2/skills/subagent-driven-development/SKILL.md)

完成前必须运行新鲜验证命令、读取输出、核对退出码和失败数量。不能用“代码已修改”“Agent 说完成”或旧测试结果代替。

## 4. Inline 与 Subagent-driven Development

### Inline / Executing Plans

源码：[executing-plans/SKILL.md](https://github.com/obra/superpowers/blob/v7.0.2/skills/executing-plans/SKILL.md)

同一个主代理按计划逐项实施。每项任务都执行 TDD，记录进度，最后做一次整分支审核。

优点：上下文切换少、成本较低。缺点：每个任务缺少独立实施者和任务级新鲜审核视角。

### Subagent-driven Development

源码：[subagent-driven-development/SKILL.md](https://github.com/obra/superpowers/blob/v7.0.2/skills/subagent-driven-development/SKILL.md)

每个任务通常经历：

1. 主代理创建任务 Brief。
2. 派发新鲜上下文的 Implementer Subagent。
3. Implementer 实施、测试、提交并自检。
4. 主代理准备该任务的 Diff。
5. 派发 Task Reviewer，分别检查规格符合度和代码质量。
6. 有问题则进入修复循环。
7. 通过后写任务账本，再处理下一个任务。
8. 全部任务完成后进行整分支审核。

关键不是“多开几个聊天窗口”，而是任务上下文隔离、明确输入输出、独立审核和可恢复记录。

### Codex 宿主依赖

源码：[Codex tools reference](https://github.com/obra/superpowers/blob/v7.0.2/skills/using-superpowers/references/codex-tools.md)

Subagent 调度依赖 Codex 宿主的 multi-agent 能力。参考文档说明了 spawn_agent、followup_task、wait_agent 等机制，也提到可在 ~/.codex/config.toml 开启 multi_agent。

本轮禁止擅自修改全局配置，因此先只读检查当前工具列表：

- 如果已有真实 Agent 工具，才执行 Subagent 实验。
- 如果没有，标记 unavailable，走 Inline。
- 不得让主代理轮流扮演 Implementer 和 Reviewer，再声称是独立 Agent。

## 5. 进度账本与中断恢复

Subagent-driven Development 和 Executing Plans 共用任务工作区和账本。典型位置为：

~~~text
<repo>/.superpowers/sdd/<plan-basename>/
  progress.md
  task briefs / review packages
~~~

恢复原则：

- 读取当前计划和对应 progress.md。
- 以账本中标记完成的任务为准，不依赖模型回忆。
- 用 Git 提交记录核对代码状态。
- 从第一个未完成任务继续。
- 账本计划身份不匹配时，不能把其他计划的记录当作当前进度。

task-start、task-done 等脚本会参与任务 Brief、验证执行和账本更新。其实际行为仍须由本地运行和文件证据确认。

## 6. 哪些由程序保证，哪些依赖模型遵循

| 能力 | 性质 | 验证方式 |
|---|---|---|
| 插件清单声明 Skill 目录 | 宿主注册机制 | Codex Skill 清单 |
| Skill 描述和触发规则 | 模型/宿主行为 | 真实调用记录 |
| 设计批准门槛 | 模型指令 | 批准前后文件写入顺序 |
| TDD RED → GREEN | 模型规则 + 测试程序 | 同一测试的失败/通过输出 |
| task-start / task-done | 辅助脚本 | 脚本输出和账本 |
| Subagent 独立性 | 宿主运行时 | Agent ID、独立上下文、回执 |
| 完成前验证 | 模型规则 + 命令输出 | 新鲜命令、退出码、完整输出 |

## 7. 本轮实验状态与证据位置

统一案例见 shared/CASE.md。计划中的实验位置：

- experiments/superpowers/inline/：Inline 独立工作副本。
- experiments/superpowers/subagent/：真实 Subagent 工作副本，仅宿主支持时执行。
- evidence/superpowers/：触发、设计门槛、TDD、审核、恢复和浏览器验收记录。

当前尚无真实 Codex Skill 调用、设计文档、计划、实现提交、Agent 回执或测试输出。不得将本章源码分析视为实操完成。

## 8. 关键源码

- [插件清单](https://github.com/obra/superpowers/blob/v7.0.2/.codex-plugin/plugin.json)
- [入口 Skill](https://github.com/obra/superpowers/blob/v7.0.2/skills/using-superpowers/SKILL.md)
- [Brainstorming](https://github.com/obra/superpowers/blob/v7.0.2/skills/brainstorming/SKILL.md)
- [Writing Plans](https://github.com/obra/superpowers/blob/v7.0.2/skills/writing-plans/SKILL.md)
- [TDD](https://github.com/obra/superpowers/blob/v7.0.2/skills/test-driven-development/SKILL.md)
- [Inline Execution](https://github.com/obra/superpowers/blob/v7.0.2/skills/executing-plans/SKILL.md)
- [Subagent-driven Development](https://github.com/obra/superpowers/blob/v7.0.2/skills/subagent-driven-development/SKILL.md)
- [Codex 专用说明](https://github.com/obra/superpowers/blob/v7.0.2/skills/using-superpowers/references/codex-tools.md)
- [完成前验证](https://github.com/obra/superpowers/blob/v7.0.2/skills/verification-before-completion/SKILL.md)
