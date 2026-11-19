# D23 营销技术、AI 与自动化知识地图

> Domain ID：D23
> Domain Type：TECHNOLOGY_ENABLER
> Primary Owner：营销数据与系统能力、营销自动化、AI 辅助和工具集成的业务需求与验收。
> 状态：DRAFT｜首版 L2-L3 地图；技术选型、权限和数据治理 SOP 尚未完成。
> Registry：见 [24 域专业领域权威登记表](01_24域专业领域权威登记表.md)。

## 一、领域任务与边界

D23 负责营销技术能力和系统实现需求，回答：

- 营销需要哪些数据、工具和技术能力？
- CRM、CDP、CMS、MAP、AdTech 和分析系统如何协作？
- 如何建立数据事件、身份、权限和自动化工作流？
- AI、Agent 和生成式内容如何安全、可测量地应用？
- 如何评估工具、供应商、许可、成本和迁移风险？

### 与相邻领域的边界

- D23 负责营销技术、数据系统、AI 和自动化能力；
- D21 负责指标、测量、归因、实验和分析逻辑；
- D19 负责 CRM 生命周期策略；
- D24 负责组织治理、权限、预算和风险控制；
- AI 原生知识系统拥有通用 Knowledge Object、Source、Evidence、Relation 和 Agent 路由定义；
- 技术工程团队负责底层基础设施、安全和软件实现。

## 二、L2-L3 专业知识地图

### MKT-D23-M01 MarTech 能力地图与架构

- MKT-D23-T001 MarTech、AdTech、RevTech 和 Data Stack 的边界。
- MKT-D23-T002 CRM、CDP、CMS、MAP、DAM 和分析系统。
- MKT-D23-T003 营销能力、业务对象和系统职责。
- MKT-D23-T004 系统集成、API、事件和数据流。
- MKT-D23-T005 Vendor、Build/Buy/Integrate 决策。
- MKT-D23-T006 技术栈依赖、锁定和迁移风险。

### MKT-D23-M02 客户数据与身份管理

- MKT-D23-T007 Customer、Account、Contact、Event 和 Consent 对象。
- MKT-D23-T008 Identity Resolution 和身份合并。
- MKT-D23-T009 First-party Data、Preference 和 Consent。
- MKT-D23-T010 数据质量、Schema、事件字典和血缘。
- MKT-D23-T011 数据共享、访问、保留和删除。
- MKT-D23-T012 数据驻留、跨境和供应商风险。

### MKT-D23-M03 CRM、CDP 与营销自动化

- MKT-D23-T013 CRM 账户、联系人、线索和机会数据。
- MKT-D23-T014 CDP 事件、用户画像和受众激活。
- MKT-D23-T015 MAP、Campaign、Segment 和 Trigger。
- MKT-D23-T016 生命周期自动化、频控和抑制规则。
- MKT-D23-T017 事件触发、Webhook 和系统编排。
- MKT-D23-T018 自动化流程的幂等、重试、错误和审计。

### MKT-D23-M04 分析、实验与营销数据系统

- MKT-D23-T019 Web/Product Analytics 和事件采集。
- MKT-D23-T020 Data Warehouse、BI 和语义层。
- MKT-D23-T021 Experiment Platform、Feature Flag 和分流。
- MKT-D23-T022 MMM、归因和数据输出接口。
- MKT-D23-T023 数据权限、隐私和分析环境。
- MKT-D23-T024 数据质量监控和可观测性。

### MKT-D23-M05 AI、Agent 与生成式营销

- MKT-D23-T025 AI 辅助研究、内容、创意和数据分析。
- MKT-D23-T026 AI Agent 的任务规划、工具调用和状态管理。
- MKT-D23-T027 RAG、知识检索和企业营销知识。
- MKT-D23-T028 个性化、推荐和预测能力。
- MKT-D23-T029 AI 生成内容的事实、版权和人工审核。
- MKT-D23-T030 AI Agent 的权限、成本、审计和停止条件。
- MKT-D23-T031 合成数据、AI 访谈和模型输出的披露。

### MKT-D23-M06 工作流自动化与系统集成

- MKT-D23-T032 事件驱动工作流和任务编排。
- MKT-D23-T033 CRM、邮件、广告、客服和数据仓库集成。
- MKT-D23-T034 审批、人工接管和外部副作用控制。
- MKT-D23-T035 失败处理、重试、回滚和告警。
- MKT-D23-T036 自动化工作流的测试和验收。

### MKT-D23-M07 技术供应商与工具治理

- MKT-D23-T037 软件能力、适用场景和采购要求。
- MKT-D23-T038 Open Source、Open Core、Fair-code 和 Source-available。
- MKT-D23-T039 许可证、第三方依赖和商业使用边界。
- MKT-D23-T040 SaaS 成本、托管成本和总拥有成本。
- MKT-D23-T041 供应商安全、数据处理和退出机制。
- MKT-D23-T042 工具弃用、迁移和业务连续性。

## 三、工具采用与集成决策

每个技术方案必须说明：

- 业务问题和预期结果；
- 使用角色和核心业务对象；
- 数据输入、输出和权限；
- 与现有系统的集成方式；
- 许可证、隐私、安全和供应商风险；
- 运行成本、维护和迁移成本；
- 人工审批和错误恢复；
- 试点范围、验收指标和退出条件。

## 四、标准交付物

- MarTech Capability Map；
- System Architecture / Data Flow；
- CRM/CDP Requirements；
- Automation Workflow Specification；
- AI Use Case and Risk Register；
- Vendor Evaluation Matrix；
- Integration Test Plan；
- Migration / Exit Plan。

## 五、质量门槛与常见反例

- 先定义业务问题，再选工具；
- 工具功能不等于业务价值；
- CRM/CDP 不自动形成可信客户视图；
- AI 生成内容不自动真实或合规；
- 自动化外部副作用必须授权和可审计；
- 数据使用遵守目的限制、最小化和保留规则；
- 开源与源码可见必须区分许可证；
- 关键系统有回滚、退出和业务连续性方案。

## 六、核心参考来源

- Agent Skills Open Standard：https://agentskills.io/
- PostHog：https://github.com/PostHog/posthog
- Mautic：https://github.com/mautic/mautic
- Google Meridian：https://developers.google.com/meridian/docs/basics/meridian-introduction
- AI 原生知识系统拥有通用知识对象和 AI 路由标准；D23 负责营销场景中的技术需求和验收。

## 七、当前成熟度

- L2-L3 地图：首版完成。
- MarTech 架构、自动化和 AI 治理 SOP：尚未完成。
- 真实工具选型和集成验证：尚未完成。
- 状态：DRAFT，不得标记 ACTIVE。
