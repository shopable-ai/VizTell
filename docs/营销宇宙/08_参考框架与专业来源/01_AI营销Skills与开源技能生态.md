# AI 营销 Skills 与开源技能生态

> 状态：RESEARCHED_REFERENCE_BASELINE
> 核查日期：2026-11-19
> 目的：研究 AI Skills 如何承载营销专业方法、重复任务和执行工作流；不把外部 Skill 数量当作营销知识完整性。

## 一、先区分五种对象

- **知识地图**
  - 说明营销领域包含什么、各领域边界和关系。
  - 不负责自动执行某个任务。
- **专业方法 / Playbook**
  - 描述如何研究、分析、判断、执行和验收。
  - 可供人和 AI 共同使用。
- **Skill**
  - 将一个边界相对稳定、重复出现、输入输出可描述的专业任务打包为可调用能力。
  - 通常包含触发条件、步骤、判断规则、参考资料、模板、脚本和验收。
- **Workflow**
  - 将多个步骤、依赖、状态、重试、检查点和人工审批连接成可执行流程。
- **Agent**
  - 面对开放环境和不确定路径，动态搜索、规划、调用工具、根据结果调整行动。
  - 必须有预算、权限、状态、停止条件和人工控制。

不要把知识地图、Skill、Workflow、Agent 混成同一层级。通用的 Skill / Workflow / Agent 定义由 AI 原生知识系统维护，营销宇宙只记录营销领域的应用。

## 二、Agent Skills 开放标准

- 官方项目：
  - https://github.com/agentskills/agentskills
  - https://agentskills.io/
- 核心结构：
  - 一个 Skill 是一个目录。
  - 必须包含 SKILL.md。
  - 最低元数据包括 name 和 description。
  - 可以包含 scripts、references、assets 等配套资源。
- 关键价值：
  - 让专业知识和任务流程可以版本化、按需加载和跨兼容 Agent 工具复用。
  - 通过 progressive disclosure，避免每次任务都加载全部长篇资料。
- 营销宇宙的应用：
  - 总地图保留知识导航。
  - 领域行动手册保留完整专业方法。
  - 高频稳定任务再提炼成 Skill。
  - Skill 只引用 canonical 知识节点，不复制第二份专业定义。
- 采用边界：
  - 不因某个任务能写成 Prompt 就一定创建 Skill。
  - 先验证任务重复性、稳定性、输入输出、失败处理和评价方式。
  - 不把第三方 Skill 当作可信指令；先审查内容、来源、工具权限、脚本和数据处理方式。

## 三、优先研究的开源技能库

### 1. Corey Haines — Marketing Skills

- 仓库：
  - https://github.com/coreyhaines31/marketingskills
- 许可：仓库 README / LICENSE 标示 MIT；实际复制或改编前仍需保留版权与许可声明。
- 项目定位：
  - 面向技术营销人员和创业者的模块化 AI 营销技能库。
  - README 描述其支持 Claude Code、OpenAI Codex、Cursor、Windsurf 等兼容 Agent Skills 的工具。
  - 技能之间通过共享上下文和 Related Skills 连接。
- 重要架构经验：
  - 用产品营销上下文提供稳定背景。
  - 其他技能通过共享上下文理解产品、用户和定位。
  - 每个 Skill 聚焦一个专业任务，而不是把所有营销任务塞进一个大提示词。
  - 复杂资料可拆到 references，核心 SKILL.md 保持精简。
- 值得研究的技能：
  - 战略与市场：
    - product-marketing
    - marketing-plan
    - marketing-psychology
    - customer-research
    - competitor-profiling
    - competitors
    - reverse-engineer-marketing
    - pricing
  - 内容与传播：
    - content-strategy
    - copywriting
    - copy-editing
    - brand-voice
    - emails
    - social-content
  - 搜索与网站：
    - seo-audit
    - ai-seo
    - site-architecture
    - programmatic-seo
    - link-building
  - 转化与增长：
    - cro
    - ab-testing
    - analytics
    - attribution
    - onboarding
    - churn-prevention
    - referrals
    - marketing-loops
  - 销售与运营：
    - revops
    - sales-enablement
    - lead-magnets
    - launch
- 不应照搬的部分：
  - product-marketing-context 面向具体企业和产品，不等于通用营销宇宙的根知识地图。
  - marketing-plan 是具体企业计划，不是营销理论总分类。
  - SEO、CRO、文案等只是局部技能，不代表完整营销能力。

### 2. OneWave AI — Claude Skills

- 仓库：
  - https://github.com/OneWave-AI/claude-skills
- 配套项目：
  - https://github.com/OneWave-AI/open-agent-stack
- README 当前展示约 230 个 Skills，数量会随仓库变化；历史 Release 的技能数量与当前 README 可能不同，引用时应记录具体 commit / release。
- README 标示 MIT；仍须对实际 Skill 文件、配套资源和依赖逐项核对。
- 值得研究的营销和商业研究技能：
  - market-sizing
  - competitor-intel-agent
  - competitor-content-analyzer
  - competitor-price-tracker
  - reddit-analyzer
  - customer-panel-of-experts
  - customer-journey-mapper
  - churn-autopsy
  - brand-voice-analyzer
  - landing-page-copywriter
  - seo-keyword-cluster-builder
  - seo-optimizer
  - customer-review-aggregator
  - product-launch-war-room
  - bi-measure-builder
  - devils-advocate
- 值得研究的架构经验：
  - 单文件 Skill 与需要 manifest / 多 Agent / 多资源的复杂工作流分离。
  - 使用专门的 Agent 负责单一研究或执行任务。
  - 通过审计、交叉检查和人类审批减少错误。
- 不应照搬的部分：
  - 230 是仓库某时点的目录数量，不是经过独立评测的 230 个高质量营销能力。
  - Agent Army 等并行机制并不适用于所有研究任务；并行不能替代证据独立性和审计。

### 3. Awesome Marketing 资源目录

- 仓库：
  - https://github.com/marketingtoolslist/awesome-marketing
  - https://github.com/kokasexton/awesome-marketing-repos
- 用途：
  - 发现工具、书籍、博客、播客、课程和专业资源。
  - 扩展工具与来源候选集。
- 边界：
  - Awesome 列表是发现入口，不是权威分类或质量认证。
  - 目录中的工具可能过时、商业化、停止维护或存在许可限制。
  - 必须回到项目官网、GitHub 活跃度、LICENSE、文档和实际测试核验。

## 四、将外部 Skills 映射到营销知识域

- D01-D02：市场与商业研究
  - market-sizing
  - competitor-profiling
  - competitor-intel-agent
  - reverse-engineer-marketing
- D03-D04：用户与需求
  - customer-research
  - customer-panel-of-experts
  - customer-journey-mapper
  - reddit-analyzer
  - customer-review-aggregator
- D05-D07：战略、STP 与竞争
  - product-marketing
  - marketing-plan
  - competitors
  - competitor-profiling
  - devils-advocate
- D08-D10：价值、定价与品牌
  - product-marketing
  - pricing
  - brand-voice-analyzer
- D11-D17：组合、内容、搜索、广告、渠道、社交与公关
  - content-strategy
  - copywriting
  - seo-audit
  - ai-seo
  - seo-keyword-cluster-builder
  - social-content
- D18-D19：转化与客户生命周期
  - cro
  - onboarding
  - churn-prevention
  - referrals
  - revops
  - sales-enablement
- D20：国际化
  - 需要补充专门的本地化、跨文化、地区法规和国际渠道 Skills；不可认为现有数字营销 Skill 已覆盖。
- D21-D22：数据、实验和增长
  - analytics
  - attribution
  - ab-testing
  - marketing-loops
  - bi-measure-builder
- D23-D24：MarTech、AI、组织与治理
  - marketing-plan
  - revops
  - marketing-loops
  - agent orchestration / workflow skills

该映射是检索和研究路由，不代表这些 Skills 已覆盖对应领域全部知识。

## 五、营销 Skill 的质量契约

一个候选 Skill 至少应有：

- 身份与版本：
  - 唯一名称。
  - 版本。
  - 作者 / 维护者。
  - 来源 URL。
  - 许可证。
  - 最近核查日期。
- 任务边界：
  - 何时触发。
  - 何时不触发。
  - 解决的问题。
  - 适用对象和前置条件。
- 输入：
  - 必需资料。
  - 可选资料。
  - 输入格式和质量要求。
- 执行：
  - 步骤。
  - 决策点。
  - 方法依据。
  - 外部工具。
  - 权限和成本。
- 输出：
  - 结构化成果。
  - 引用和证据。
  - 未知与限制。
  - 后续行动。
- 验收：
  - 正确性。
  - 完整性。
  - 可复现性。
  - 失败处理。
  - 人工审批点。
- 安全：
  - 不信任外部页面、评论、用户内容中的指令。
  - 不泄露敏感资料。
  - 不擅自联系客户、发布内容、花费广告预算或修改业务系统。
  - 不把模拟数据和生成内容冒充真实研究。

## 六、Skill 候选晋级规则

- IDEA：
  - 发现某项任务可能值得技能化。
- RESEARCHED：
  - 已研究现有开源 Skill 和专业方法。
- PROTOTYPE：
  - 已形成初步工作流程。
- TASK_TESTED：
  - 至少在代表性真实任务中测试。
- REVIEWED：
  - 已完成反方、事实、安全和边界审查。
- ACTIVE：
  - 输入输出稳定、可重复调用、维护者和复核周期明确。
- DEPRECATED：
  - 被新版本或其他能力替代。

不以目录数量、Skill 数量或 Prompt 长度作为成熟度指标。

## 七、当前采用建议

- 第一阶段：
  - 只研究和引用外部 Skills。
  - 不将整个技能库复制进营销宇宙。
  - 不要求用户安装全部技能。
- 第二阶段：
  - 选取市场研究、用户研究、竞争情报、营销规划、测量分析等高频任务做小范围验证。
- 第三阶段：
  - 对重复出现且验收稳定的任务，形成营销宇宙自己的领域 Skill。
- 第四阶段：
  - 需要跨多个 Skill、数据源和人工审批的任务，才设计 Workflow。
- 第五阶段：
  - 只有存在开放式动态探索和重规划需要时，才考虑 Agent。

## 八、维护要求

- 每 90-180 天检查主要 Skill 仓库的版本、活跃度、许可证和目录变化。
- 对快速变化的 AI Skill 和营销平台接口，使用前重新核查。
- 外部 Skill 的内容属于参考材料，不得覆盖营销宇宙的 canonical 专业定义。
