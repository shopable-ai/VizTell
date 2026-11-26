# R1-B.3｜Cookie Editor 同站子路径变化：独立增量价值实验登记

> 状态：**REGISTERED / BLOCKED_INDEPENDENT_EXECUTION**。登记日期 2026-11-26。仅供协调者与审阅者；执行者只收第2节共同输入和各自方法资料，不得读取本文件全文。当前没有 A/B 输出、盲评、运行测试、实际成本或增量收益结果。
>
> 任务 ID：AI-NATIVE-ENGINEERING-MODEL-UNIVERSE-R1-B.3。目标不是修 Cookie Editor，而是检验 R1-B.2 选择法是否能使 AI 在同一存量局部任务中作出更好的研发决定。

## 1. 真实任务与固定基线

历史用户反馈（2026-11-12 10:30:53 UTC，历史对话检索返回的原话片段）：“网址没变，但是sidepanel里面的内容会变化……在域名没有变化时，他里面的数值几乎不会变。现在似乎子路径变化，都会导致触发更新，页面中有2秒钟的空白间隙一样。” 该日后续目标另含复制/导出；本实验仅取上述导航问题，不把后续修复、其他需求或协调者推断写成用户原话。未获得完整原始会话导出，约2秒为用户观察而非本轮测量。

固定源码为 OpenDesk [cfc6e232](https://github.com/shopable-ai/opendesk-browser/tree/cfc6e232ac074be656a5af8bacacc30e6f351fd3)，提交时间 2026-11-12 12:34:11 UTC，树 d422b142723f5d8cdd0806a1cf5baa3e392deedc；为历史 R2 相关修复前的父版本。源码/测试从此树读取，不读取后续修复 diff、commit message 或验收。主线读取时 afca127bb406c94119ffd6c093071a5df25b4a06，不作实验输入。既有 AI-Project-OS 共同基线 [1a186764](https://github.com/shopable-ai/ai-native-project-os/tree/1a1867640b7ee538bac21cd1a16d50f6a7e19c0f)。R1-B.2 方法基线 VizTell [f7b8860](https://github.com/shopable-ai/VizTell/tree/f7b886000131bf6a86cddba252bd1e95f2732fae)，树 19067a8550951f11dd4b2ae01b95538f159ffab1。其相对用户指定 da98e64b 的差量仅 README、90。

选择原因：用户观察明确，真实存量、跨 UI 与异步数据责任、存在旧测试和安全边界，区别于快捷键及媒体规则案例。在本专题 00–08、README、90 固定文本中按 Cookie Editor、cookie-editor、同站空白等关键词检索未发现该案例；这不是全库语义证明。协调者已知历史修复提交标题，仅用于选定前版本，未读取修复 diff。协调者不能担任两组执行者或独立盲评者。

## 2. 两组共同输入（只摘录本节和各自方法，不传其他节）

**同一请求：** 上述用户报告的同域名/子路径变化导致 Cookie Editor 列表触发更新并约两秒空白。请基于修复前现有代码，确定怎样让同站导航时列表表现稳定、仍能正确更新，不引入新功能或破坏既有行为。只做可实施的分析与最小修改/验证建议，不改代码，不处理复制导出、账号切换或整个框架重构。无法证明的事实标 Unknown；不得把用户观察或测试定义当运行结果。

**共同业务资料**（只允许 cfc6e232... 的以下入口及其明确相关的直接/间接依赖、相应旧测试；禁止 Git 历史、其他版本、网页搜索、实验协调文档、后续验收、其他聊天/记忆。协调者可预制只含允许文件的独立资料包；发现必要依赖时对两组同时开放同一固定版本并记录，不给内容提示）：

| 固定入口 | Git blob SHA |
| --- | --- |
| projects/cookie-editor/app/CookieEditorApp.jsx | 79ab2e2a28d0c4aa8fb0e5b0da65950c8255c30d |
| projects/cookie-editor/app/controller/cookie-controller.js | 75eaf90fa3d700b804ff3bfaca79794bc078da4c |
| projects/cookie-editor/app/controller/cookie-observation.js | e6bd52c18a82a4514718dfe03235d5eeecdb22d4 |
| projects/cookie-editor/app/adapters/browser-sdk.js | 691b319c3cd57f692c908ead421edc1f092594c2 |
| projects/cookie-editor/app/domain/cookie-model.js | d37d29c1879bdbcf0d4284146f6f0049e9 |
| src/ui/sidebar-tools.js | 68cb02cf0380cb4f31d0d4933991ccf3c4023521 |
| src/sidebar-tools/bridge.js | 8c3e80a72e0bcbdbe651ef13027ba42df234e435 |
| src/ui/current-page-target.js | f51f4b8193d69419a1068159e2a8116ae21bf9e1 |
| tests/environment/cookie-editor-react-controller.test.mjs | f553315c953c1c8c813ae2ad5ae049a9df8d5929 |
| tests/environment/sidebar-tools-host.test.mjs | 9bcf1216de49572afb997a778fb70d5d3f96af5d |
| tests/environment/current-page-target.test.mjs | a1a45cbab10a60b57baea1f3c58b345d34ca8b1a |
| projects/cookie-editor/tests/cookie-changes.test.mjs | 337bea72efeea8c2603a756ef49410b699904c41 |

以上路径及 SHA 均由固定树或文件读取返回；current-page-target 源码与测试只核对树条目，尚未逐行审读。未执行任何测试。无需提供包含无关个人账号/历史运行记录的整个产品 README；不得访问真实 Cookie、账号、浏览器会话或凭据。用合成测试数据。

**共同方法资料**（OS 固定 SHA）：README.md、project-os.yaml、templates/brownfield-project/README.md、docs/workflows/L2_PROGRESSION.md、docs/workflows/REQUIREMENT_DESIGN_WORKFLOW.md、docs/governance/CAPABILITY_FUNCTION_SPEC_MAPPING.md、templates/standard-project/requirements/functions/FUNC-001_功能需求卡.md、templates/spec-package/README.md、docs/governance/RUN_EVIDENCE_ACCEPTANCE.md。均为既有方法；不得用弱化版 A。两组均交付：有来源的目标和现状判断、建议改动与不变范围、风险和验收、未知项、读取路径及实际用量。输出结构一致；不要求 A 使用工程模型名称或额外表格。

## 3. 隔离、方法差量与计量（协调者）

A 只收到第2节共同输入及 OS 资料。B 得到完全相同内容，额外提供 VizTell 固定 f7b8860 README 的 L13–63（六类任务、五问、停止规则及决策关系）和 L81–94（真实资料恢复、冲突、停止）。不要发送 README 整篇、08、09、90 或案例结论。摘录保持原文与行号，B 的额外阅读计入总成本；不将审阅判据变成提示线索。

执行前检查：相同模型及推理配置、相同系统指令、独立空白上下文（禁用历史/共享记忆/项目自动加载；不能强制隔离则停止）、相同工具和只读文件包。不得由协调者补答案。默认每组最多20分钟、25次文件读取、同一输出上限2500中文字符（引用路径和原始指标不计）；两组同一限制。如环境无法测时/计数，事前统一调整并留下差异，不能事后改。记录模型、执行身份、实际首答原文和 SHA、读取路径/字节或 token、开始/结束时间、工具调用次数、截断/失败、额外方法读取成本；不能取 token 则明确未观测，不估算替代。固定原始首次输出后方可继续。

第三位未参与方案分析的审阅者只收到第2节共同事实、下节冻结标准和去掉组名/方法标签的两份原文（随机 X/Y），不提供真实分组或历史修复。保留原有实质内容与引用，不以润色抹去差异；若审阅者可识别分组，记录盲法破坏。先锁定逐项理由和评分，再揭盲；任何后续历史修复只作佐证，不是唯一正确答案。协调者不替代评审。

## 4. 审阅判据（仅审阅者；分析者不得读）

以下是协调者基于修复前事实冻结的判据，不是新批准的产品需求或指定唯一实现。证据均可在共同资料内查证；仍需由独立审阅者校对。

| ID | 评价问题（0 / 0.5 / 1） | 修复前依据 |
| --- | --- | --- |
| C1 目标 | 明确无意义空白/闪烁是用户问题，但稳定不等于禁止真实数据变化；不扩展账号/导出 | 原始用户描述；cookie-model.js L6–14 |
| C2 事件与根因 | 是否找到真实 Host→Bridge→App→Controller 触发链并指出哪里产生清空/加载；不把约2秒当已证实的唯一计时根因 | sidebar-tools.js L5804–5825；bridge.js L536–538；CookieEditorApp.jsx L156–188；cookie-controller.js L54–65、79–121 |
| C3 范围正确性（关键） | 区分标题/Query/Hash、Path、Document/Tab、Origin、授权与 Store/Partition；Path 可影响真实 Cookie 匹配，同域名不等于安全同范围，未知范围不得盲目复用 | cookie-model.js L6–14、16–47；browser-sdk.js L48–82；Host pageKey |
| C4 资产复用 | 是否发现现有被动元数据同步/失效/读回与已有防覆盖测试；能否说明复用边界，避免另建全站缓存、第二控制器等无依据机制 | controller L528–567；App L191–228；react-controller.test L65–106 |
| C5 并发与安全（关键） | 快速 A→B→A、旧请求迟到/错误、权限撤销、敏感 DOM、编辑草稿/确认与已派发副作用未知，不把旧数据变成可操作真相、不自动重放 | controller L49–78、528–567；App L121–175；测试 L75–95、252–278、314–325 |
| C6 修改范围 | 给出有源码依据的最小责任边界；共享宿主事件可能有其他消费者，不能为了 Cookie 切掉其他工具必要通知或弱化全局安全门；说明未知 | Host L5804–5825；sidebar-tools-host.test L3446–3457、3459起 |
| C7 验收 | 事前正反例：同站纯元数据变化/子路径稳定且正确，范围改变时旧数据清除/禁用，快速导航/撤权/草稿/未知操作回归；优先复用旧测试，真实 Chrome 与 Node 区分 | react-controller.test L65–106、252–278、314–325；Host tests |
| C8 证据及成本 | 每项关键事实可追溯；注明静态分析/未知；无虚假已修复/已运行；实际用量及不必新建模型的成本有记录 | OS 证据规则；本登记共同输入 |

每项明确且正确覆盖1，部分正确0.5，遗漏或关键错误0；另登记事实错误/误报、重复开发项、实际修改范围和安全缺陷。仅输出更长或模型名称更多不加分。C3/C5 为关键安全正确性；其余项同权用于描述，不能用总分抵消严重错误。独立评审允许不同合理方案。

决策规则（协调者预设，非统计显著性）：若 B 没有可复核的新实质正确决定，保留可选指引；仅改善表达，不增机制。若 B 有至少一项有来源的实质遗漏修正、错误避免、资产复用或删减不必要开发，且无新严重错误/关键项退化，才考虑接入已有 R0/需求卡/Spec 的最小阅读位置。默认成本容忍线为实际可比较总时长和读入 token/字节各不增加超过20%；超出时不能自动升格，除非审阅者明确说明收益为何足以抵偿成本。若测量缺失则不判成本合理；若成本明显大于收益则停止相应做法。单个历史任务最多支持局部候选接入，不能证明通用效果或修改正式契约。成本维护项独立记录需新增的正式文档/字段/重复权威数量和预计维护责任；估计不能冒称长期观测。

## 5. 实际执行回执

| 步骤 | 结果 |
| --- | --- |
| 指定 baseline、main 差量、仅主分支 | 已核验，VizTell 当时仅 main |
| 新真实案例、修复前源/测试路径、共同输入、B 增量与事前审阅标准 | 已登记；尚未生成独立沙箱资料包 |
| CodexPro server_config | UNAVAILABLE：McpServerError: Connection failed |
| OpenDesk Desktop Mac96 browser status | UNAVAILABLE：MCP SSE probe returned 429 from openai.org |
| 可直接启动隔离模型/审阅的当前工具 | 未发现；handoff 仅写计划、不执行 |
| A 首次输出 / B 首次输出 | NOT_RUN / NOT_RUN |
| 独立盲评 / 成本测量 / 产品测试 | NOT_RUN / NOT_MEASURED / NOT_RUN |
| 实质增量收益、长期维护成本 | UNKNOWN |
| 当前采用决策 | 暂不正式接入；保留可选阅读指引，理论研究冻结 |

本登记是协调者真实读取与事前设计，不是独立实验，也不是 A/B 模拟或历史修复验证。唯一剩余动作是用已登记输入完成独立 A/B 和盲评；无需重复理论或另开任务。只修改 VizTell 研究文档，不修改正式 OS、OpenDesk 业务或发布。
