# R1-B.2 工程模型实际使用对照：AI Send Queue Ctrl+Enter

> 2026-11-26｜真实历史源码回顾性同作者对照，不是独立盲测或当前产品验收。未运行产品或测试、未修改业务。

## 1. 固定输入与评价标准

任务：在既有 ChatGPT 消息队列中实现/核对 Ctrl+Enter 等价于皇冠入队，保留正常 Enter / Shift+Enter 与草稿安全；决定复用什么、修改什么、验证什么。源于 H0 README 3、7、55行，不把历史修复描述当新需求。理由：局部、真实需求/修复前源码/测试可读，并有后续修复佐证。在本专题01–06、README、90中未发现 Ctrl+Enter/发送队列/ai-send-queue 完整演示（关键词检查，非全库语义证明）。

- VizTell 输入 `5f93116c283a777000835cb36b6e53bacb09a172`；AI-Project-OS `1a1867640b7ee538bac21cd1a16d50f6a7e19c0f`。OpenDesk 读取时 main `a79c2c8879607f924683be71d32468030c225537`。
- 比较只用修复前 H0 `3c0f53686b047eb94af6c83f38709ff0b17380ff`。后续历史修复 H1 `d2465192d8efa89d38d47cd1d2a4762f14ae9c38` 作事后佐证；当前 main 的 main.js 已明显演进，不当作 H0/H1。
- A/B 共同允许资料：H0 README、main.js、engine.js、site.js、view.js、main-recovery.test.mjs；共同方法：现有 OS 总览、需求工作流、能力/功能/Spec 指南、需求卡、Spec 与证据规则。B 额外使用本轮任务选择表和五个问题。没有独立环境、模型指纹、预算/耗时/token 计量；仅作者分别组织输出，不能称独立执行。
- 下表在写出 A/B 结果前确定，依据 H0 原始需求及事实。作者此前读过历史验收报告，存在后见偏差；并未实际隔离 H1 答案，不能称真正预注册盲测。C4/C5 为依据目标与代码推导的候选安全行为，不冒充已批准需求。

| 编号 | 评价判据（明确覆盖/未覆盖/未知） | H0 根据 |
| --- | --- | --- |
| C1 | 确认已有快捷键及皇冠共享能力，避免新队列 | README 3、7；main 35–60、122–145；view 159 |
| C2 | 保持 Enter、Shift+Enter、IME、修饰键、其他编辑器、重复按键原行为 | README 7；main 130–158；旧测试 |
| C3 | 区分可信键盘和合成事件，定位可信来源门缺失 | README 7；main 130–144 |
| C4 | 未确认发送时残留文本不能当新草稿；两入口均不得再次清空/入队 | README 3、55；main 35–60、141–157；engine 32–46、152–169 |
| C5 | 确认后即使 busy 也允许新草稿（含有意同文）；不靠文本去重或 busy 一刀切 | README 3；engine 103–112、243–254 |
| C6 | 保留草稿预检、清空确认、恢复、路由与现有模块责任 | main 35–60；site 159–174；engine 32–46 |
| C7 | 针对 C2–C6 提出正反回归；区分测试定义、实际运行和原生观察 | README 85；旧测试 |
| C8 | 只提出必要差量；历史记录不证明当前版本/真实 Chrome | README 85；共同 OS 证据规则 |

## 2. A：常规存量研发 + 既有 AI-Project-OS

- 需求和场景：当前受支持的原生输入框可信 Ctrl+Enter 捕获后只走皇冠入队，即使队列空且原生 Send 可用；普通 Enter 保留受限回退，Shift/Alt/Meta、IME、编辑器替换、其他输入与重复事件保持原规则。已有 main 128–158、view 159，无需新队列/按钮。
- 状态及存量：main 130 的监听缺 isTrusted；main 35–60 与 engine 32–46 的预检不阻止 inFlight；普通 Enter 的门 154–156 被 Ctrl 分支与皇冠绕过。engine 152–169 会把待发文本准备到原生编辑器，若同路由、队列未满且残留文本可读，可能再次清空/入队。preparing、await-native-ready、await-confirm、unknown、await-stop 均需保护双入口。confirmFlight 清除 inFlight 并保留 answerGate，确认后允许新草稿（含同文），现有发送门控制 FIFO 和回复结束。
- 候选修改：共享 enqueue 在清空前检查未结束 flight；键盘入口检查可信来源。保留原预检、路由、附件/IME、清空读回与恢复；复用 site、engine、view，不改 schema、派发器、侧栏，不新增队列。普通 Enter 既有额外门保持。
- 验收：复用首次入队、原生 Enter、IME、修饰键、重复按键、恢复测试；补 isTrusted=false（不消费/不清空/不入队）、两入口五种 flight（草稿/队列不变）、确认后 busy 时同文新草稿、迟到确认/FIFO 不重发。区分 Node 替身、真实键盘/原生历史观察与安装版本；不报当前通过。

## 3. B：相同方法 + 工程模型选择框架

任务类型为存量功能修改/缺陷核对；每行回答一个决定，不建立独立模型文件。

| 决定 | 所需知识与权威来源 | 输出 |
| --- | --- | --- |
| 是否需要新能力 | 目标/需求、能力/功能：README 3、7；main 128–145、view 159 | 复用共享 enqueue；不新增队列、按钮或派发能力 |
| 哪些触发合法 | 场景/交互/规则：README 7；main 130–158；旧测试 146–206 | 只当前编辑器的可信 Ctrl+Enter；保持其他修饰键、IME、repeat、原生 Enter；缺 isTrusted，补 listener 门 |
| 当前文本属于谁、何时不可动 | 状态/规则/数据：main 35–60、141–157；engine 32–46、103–112、152–169、243–254；site 159–174 | 未确认 flight 残留可能是待发正文，五阶段双入口拒绝清空/入队；确认后 answerGate busy 仍接收新草稿，允许有意同文，不用文本/busy 去重 |
| 改谁，哪些不动 | 架构/实现：view 159 → main.enqueue → engine.checkEnqueue / site.clearForQueue → engine.enqueue / poll | 共享 action 在清空之前 guard；可信事件在 listener；复用 site 读回/恢复与 engine FIFO/确认，不改 schema、派发、侧栏 |
| 如何验证 | 需求/行为、测试：旧 main-recovery 146–206、220–231 | 复用旧测试；补不可信、五阶段双入口、确认后 busy 同文、迟到确认及 FIFO；保持原生 Enter、IME/节点替换、预检和恢复 |
| 可以声称什么 | 证据：README 85、OS Run/Evidence | H0 静态分析；Node 替身也不证明真实 Chrome、IME、安装或当前版本通过 |

不展开全项目目标树、用户旅程、完整数据/架构图、部署拓扑、独立任务 DAG、关系注册或新状态对象：没有对应决定。数据知识指草稿与队列项的归属、生命周期，而非新建数据表。结果复用现有需求卡/候选 Spec/验收项，未批准新对象。

## 4. 对照结果

| 判据 | A | B | 可观察结果 |
| --- | --- | --- | --- |
| C1 复用 | 覆盖 | 覆盖 | 都选择共享动作 |
| C2 交互 | 覆盖 | 覆盖 | 都保持原有边界 |
| C3 可信来源 | 覆盖 | 覆盖 | 都定位真实代码缺失 |
| C4 状态 | 覆盖 | 覆盖 | 都找到五阶段双入口问题 |
| C5 确认后入队 | 覆盖 | 覆盖 | 都避免文本/busy 粗暴拦截 |
| C6 职责和保护 | 覆盖 | 覆盖 | 同一共享入口并复用模块 |
| C7 验证 | 覆盖 | 覆盖 | 都提出必要回归和原生边界 |
| C8 差量和证据 | 覆盖 | 覆盖 | 都不新增队列或冒称通过 |

A 8/8、B 8/8 是作者依据上表对自身输出的描述性核对，不是独立命中率。两份均提出同样两个修复点，无不必要新增开发任务。A 四段叙述，B 六行明确决定与来源。两组业务输入均为六文件，B 额外阅读选择表；正式新增模型文件均为0。没有测量阅读耗时、token、认知成本、长期维护成本。

### 历史修复佐证（非本轮测试）

- H0 [共享动作][h0-main]、[键盘入口][h0-key] 缺共享 flight guard 和 isTrusted 检查；[engine 32–46][h0-engine] 仅检查文本、容量和路由。旧[测试 220–231][h0-oldtest] 针对普通 Enter 且固定预检拒绝，不能证明 Ctrl 与皇冠在允许预检下也能阻止。
- H1 [main 35–59][h1-main] 共享动作清空前加入 inFlight 检查，[键盘入口][h1-key] 加 isTrusted；[单元回归][h1-test] 验证两种 Enter 非可信、五阶段双入口保留；[组合回归][h1-int] 使用真实 main/Site/Engine 与 Node 替身覆盖迟到确认、FIFO、确认后 busy 同文。与 A、B 候选一致，不是 B 独有发现。
- [历史验收报告][h1-report] 记载入口26/26、组合9/9、全测246/247，唯一全测失败为侧栏正式包字节不一致；原始日志存本地忽略目录，未取到或复跑。r16 未完成真实 Chrome 快捷键和安装验收。只能引用历史文档记载，不继承通过等级，也不评价当前 main 的运行。

**结论：** OS 现有工作流已要求状态、异常、规则、已有资产、验收及风险裁剪。严谨基线可找到同样缺陷。新增选择法暂时仅展示显式决定—知识—来源—停止理由的组织价值，未证明减少遗漏、重复或成本。无依据新增正式协议、Skill、模型文件或运行机制。

## 5. 剩余验证

唯一缺口：新执行上下文、另一个固定真实历史小任务、相同输入与预算，A 只给原 OS、B 增加 README 选择法；协调者先冻结基于项目事实的判据，执行者分别保存首次输出、实际读取和耗时/token，第三方盲评，允许平局或 B 更差。若只有表达改善，保留可选指南；仅有可复核的决策收益且成本合理时研究最小接入。不将单例外推。

[h0-main]: https://github.com/shopable-ai/opendesk-browser/blob/3c0f53686b047eb94af6c83f38709ff0b17380ff/projects/ai-send-queue/src/page/main.js#L35-L60
[h0-key]: https://github.com/shopable-ai/opendesk-browser/blob/3c0f53686b047eb94af6c83f38709ff0b17380ff/projects/ai-send-queue/src/page/main.js#L130-L158
[h0-engine]: https://github.com/shopable-ai/opendesk-browser/blob/3c0f53686b047eb94af6c83f38709ff0b17380ff/projects/ai-send-queue/src/page/engine.js#L32-L46
[h0-oldtest]: https://github.com/shopable-ai/opendesk-browser/blob/3c0f53686b047eb94af6c83f38709ff0b17380ff/projects/ai-send-queue/tests/main-recovery.test.mjs#L220-L231
[h1-main]: https://github.com/shopable-ai/opendesk-browser/blob/d2465192d8efa89d38d47cd1d2a4762f14ae9c38/projects/ai-send-queue/src/page/main.js#L35-L59
[h1-key]: https://github.com/shopable-ai/opendesk-browser/blob/d2465192d8efa89d38d47cd1d2a4762f14ae9c38/projects/ai-send-queue/src/page/main.js#L135-L149
[h1-test]: https://github.com/shopable-ai/opendesk-browser/blob/d2465192d8efa89d38d47cd1d2a4762f14ae9c38/projects/ai-send-queue/tests/main-recovery.test.mjs#L210-L230
[h1-int]: https://github.com/shopable-ai/opendesk-browser/blob/d2465192d8efa89d38d47cd1d2a4762f14ae9c38/projects/ai-send-queue/tests/shortcut-integration.test.mjs#L99-L166
[h1-report]: https://github.com/shopable-ai/opendesk-browser/blob/d2465192d8efa89d38d47cd1d2a4762f14ae9c38/projects/ai-send-queue/ACCEPTANCE-CTRL-ENTER.zh-CN.md

H0 共同资料：[需求](https://github.com/shopable-ai/opendesk-browser/blob/3c0f53686b047eb94af6c83f38709ff0b17380ff/projects/ai-send-queue/README.zh-CN.md)、[main](https://github.com/shopable-ai/opendesk-browser/blob/3c0f53686b047eb94af6c83f38709ff0b17380ff/projects/ai-send-queue/src/page/main.js)、[engine](https://github.com/shopable-ai/opendesk-browser/blob/3c0f53686b047eb94af6c83f38709ff0b17380ff/projects/ai-send-queue/src/page/engine.js)、[site](https://github.com/shopable-ai/opendesk-browser/blob/3c0f53686b047eb94af6c83f38709ff0b17380ff/projects/ai-send-queue/src/page/site.js)、[view](https://github.com/shopable-ai/opendesk-browser/blob/3c0f53686b047eb94af6c83f38709ff0b17380ff/projects/ai-send-queue/src/page/view.js)、[测试](https://github.com/shopable-ai/opendesk-browser/blob/3c0f53686b047eb94af6c83f38709ff0b17380ff/projects/ai-send-queue/tests/main-recovery.test.mjs)。OS [需求工作流](https://github.com/shopable-ai/ai-native-project-os/blob/1a1867640b7ee538bac21cd1a16d50f6a7e19c0f/docs/workflows/REQUIREMENT_DESIGN_WORKFLOW.md)、[映射指南](https://github.com/shopable-ai/ai-native-project-os/blob/1a1867640b7ee538bac21cd1a16d50f6a7e19c0f/docs/governance/CAPABILITY_FUNCTION_SPEC_MAPPING.md)；其他共同 OS 入口见 README。
