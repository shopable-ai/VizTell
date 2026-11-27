# AI-Native Framework Lab

本目录用于真实理解、实操和验收 Superpowers 与 BMAD。它是独立实验，不属于通用框架理论目录，也不属于生产项目。

## 固定版本

| 框架 | 版本 | 源码提交 |
|---|---|---|
| Superpowers | v7.0.2 | 22f0b463e7a5e579904dd6211a520321035526f7 |
| BMAD Method | v6.12.4 | bab9082c3e884e0d72c759bcd1a6d90bcc01be84 |

源码：[Superpowers v7.0.2](https://github.com/obra/superpowers/tree/v7.0.2) · [BMAD v6.12.4](https://github.com/bmad-code-org/BMAD-METHOD/tree/v6.12.4)

## 本轮状态

- 已完成：固定版本核对；关键 Skill、Workflow、Memlog 和 Codex 宿主说明的定向源码核查；统一案例与测试基线设计。
- 已写入：三份中文研究稿、共享模拟案例、测试骨架、证据目录和实验执行约定。
- 未完成：真实 Codex Skill 触发、框架安装/运行、TDD 红绿、Subagent 调度、Party Mode 模式验证、工作流中断恢复、真实浏览器验收。
- 阻塞：本轮 CodexPro 本地工作区桥接连接失败；本机文件桥接和桌面控制通道返回 429。详见 evidence/ENVIRONMENT-STATUS.md。
- 重要：当前没有 Superpowers 或 BMAD 真实生成的实验结果。研究稿是基于源码的解释，不得冒充框架生成物。

## 主要成果

1. [01_Superpowers理解与实操.md](01_Superpowers理解与实操.md)
2. [02_BMAD理解与实操.md](02_BMAD理解与实操.md)
3. [03_核心能力对比与复用结论.md](03_核心能力对比与复用结论.md)
4. [shared/CASE.md](shared/CASE.md)：两套框架共用的原始需求与验收契约。
5. [experiments/README.md](experiments/README.md)：运行、隔离与证据保存约定。
6. [evidence/ENVIRONMENT-STATUS.md](evidence/ENVIRONMENT-STATUS.md)：本轮真实连接检测。

## 隔离规则

- 不修改 OpenDesk Browser 生产代码。
- 不修改 Superpowers / BMAD 第三方源码，不升级固定版本。
- 不修改全局 Codex 配置，不为实验擅自开启 multi-agent。
- 不覆盖或迁移 projects/ai-native-dev 的既有研究。
- 两套框架使用 shared/CASE.md 的独立副本，彼此不共享工作区和生成物。
- 只有框架在真实宿主运行中生成的文件，才可以标记为 generated。
- 无真实子 Agent 时，标记 unavailable / not verified；不得用角色扮演或同一模型自评冒充独立 Agent。

## 继续执行顺序

1. 本地宿主恢复后，只读盘点 Codex 工作区、Skill 清单、Agent 工具和版本。
2. 复制 shared 案例到各自隔离工作区，运行并保存实现前测试基线。
3. 在 Superpowers 独立会话中验证 Brainstorming、设计批准、计划、TDD、Inline / Subagent、审核和恢复。
4. 在 BMAD 独立会话中验证 bmad-build、SPEC / Memlog、Oneshot / Dispatch、Party Mode 和恢复。
5. 使用相同测试基线做自动化和浏览器级验收。
6. 完成四个专业视角审核后，更新研究结论与评分。

当前状态是“源码机制已核查、真实实操未完成”，不是 R2 完成。
