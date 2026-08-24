# 商业模式宇宙：统一结构清单

> 当前版本：**v4 本体 + runtime-v1 横向运行时 + 项目商业推理业务层**。唯一入口：`README.md`。

## 00_导航与总览
- `00_当前有效版本与加载入口.md`
- `01_统一结构与迁移映射.md`
- `10_项目范围与边界.md`
- `11_知识层级与分类规范.md`
- `12_阅读与使用路径.md`
- `13_完整性与反方审计清单.md`
- `20_映射规则风险门与95分验收.md`

## 01_核心机制与组合模式
- `00_商业模式宇宙总览与核心结论.md`
- `01_L1-L2原子机制库.md`
- `02_L3经典与组合模式库.md`
- `03_v3新增组合模式P131-P170.md`
- `04_v4商品角色价格架构Offer转化与场景经济.md`
- `05_v4新增组合模式P171-P200.md` — v4 Pattern 人类阅读镜像；机器事实源仍为 08 中 JSONL
- `06_机会来源_差异捕获与商业模式变换算子.md` — 横向机会发现/差异捕获/结构变换镜头；不新增 U/Atom/Pattern ID
- `10_结构化知识地图/`

## 02_价值链与利润池
原价值链与利润池目录整体迁入。当前审计确认总览/部分子文件仍偏纲要级，后续由真实项目暴露的 K1/W1 信号驱动深化。

## 03_生态与价值交换
原生态与价值交换目录整体迁入。当前审计确认主要仍是框架/问题集，后续重点补多方激励、补贴稳定性、绕平台和案例校准。

## 04_案例与行业地图
- `01_商业模式案例与证据/`
- `02_行业商业模式地图/`

案例用于现实证据和机制校准，不作为项目商业推理的唯一入口。

## 05_失败模式与迁移
- `01_失败模式库/`
- `02_商业模式迁移路径/`

## 06_真实经济性_返点与治理
- `00_返点门槛后台利益与真实净经济性.md`
- `01_经济真相治理容量风险合同与劳动力层.md`
- `02_v4隐藏利润层单位经济KPI实验与风险.md`

## 07_元数据知识图谱与Skill
- `00_元数据知识图谱与Skill协议.md`
- `01_v3_Skill增量协议.md`
- `02_v4_Skill机器加载与Offer决策协议.md`

## 08_机器数据与Schema

### v2/v3/v4 本体与协议
- `atoms.jsonl`
- `atoms_v3_registry.json`
- `atoms_v4_registry.json`
- `patterns.jsonl`
- `patterns_v3_extension_P131-P170.jsonl`
- `patterns_v4_extension_P171-P200.jsonl`
- `product_roles_v4.json`
- `business_model_signature.schema.json`
- `business_model_signature_v3.schema.json`
- `business_model_signature_v4.schema.json`
- `conditional_economics_rebate.schema.json`
- `validation.json`
- `validation_v3.json`
- `validation_v4.json`

### runtime-v1 横向机器资产
- `task_router_v1.json` — 8 个核心任务族 + 跨切 flags + `retrieval_concepts` + 最小上下文装配规则
- `commercial_reasoning_runtime_v1.json` — 端到端状态机、Data/Evidence Gate、Trace、错误分类与生命周期
- `benchmark_manifest_v1.json` — A-E、Rubric、惩罚项、T01/T02、Semantic Retrieval Anchors、Ablation、Regression

> runtime-v1 不新增或重排 U/Atom/Pattern/PR ID；它只描述怎样加载、使用、测试 v4。

## 09_专题商业模式
- `电子书商业模式.md`

专题提供某一项目/行业的深度背景，但不能替代 P01-P20 通用业务主干。

## 10_任务工作流与运行时

### 人类业务层（真实项目默认入口）
- `03_项目优先商业推理执行协议.md` — **P01-P20 项目商业推理主干**；按普通商业问题组织，回答“项目是什么、钱在哪里、先做什么、怎样验证和持续经营”
- `05_真实商业项目与商业现象解析.md` — 处理已有项目、已有功能、灵感、经营问题、真实数据，以及别人赚钱现象/成功失败案例/模式迁移等现实入口；包含商业模式逆向拆解与盈利假设树
- `06_从商业判断到实际赚钱.md` — 把候选排序转成可卖 Offer、真实交易、经营指标、继续/修改/停止条件与扩大路径
- `04_T01电子书与T02_AI_API真实项目运行记录_2026-08-24.md` — 首轮真实项目决策运行记录；属于案例证据，不是工作流本体

### 后台运行与质量保障层
- `00_下一阶段演进与成熟度地图.md`
- `01_任务路由_检索_上下文与数据门.md`
- `02_端到端商业推理Workflow与知识生命周期.md`

> 默认人工阅读顺序是 `03 → 05 → 按需调用知识 → 06 → P20`。`00/01/02` 只在需要后台实现、检索、上下文或质量保障时进入。

## 11_Benchmark与回归
- `00_Benchmark评测体系_A-E_消融_回归.md`
- `01_T01电子书与T02_AI_API跨场景Canary.md`
- `02_首轮运行时实测_问题修正与验收.md` — 记录首轮 R1/C1 暴露、两次 Retriever 修正及最终验收
- `runtime_harness_latest.json` — GitHub Actions 自动写回的最新确定性运行报告；属于可再生测试证据，不是本体事实源

> Benchmark 是后台质量保障，不是普通用户处理项目时的第一阅读入口。新增 Case 应由真实项目暴露的覆盖缺口驱动，而不是为了增加数量。

## 仓库级测试入口
- `scripts/benchmark_business_model_universe.py` — v4 preservation + runtime routing/context + V0 retrieval semantic-anchor harness；其分数不等于 A-E 商业答案质量分数。
- `.github/workflows/business-model-universe.yml` — `main` 相关修改的回归入口；带并发串行保护，自动写回最新报告。

## 90_研究来源与参考
- `00_传统参考知识/`
- `01_研究来源索引.md`
- `02_v3研究来源补充.md`
- `03_v4缺口审计与研究来源.md`
- `99_历史结构/` — 历史入口、结构快照和并发重构版本说明，不作为当前事实源

## 结构迁移与运行时同步纪律

目录发生移动、拆分、合并、重命名、并发新增或运行时协议改变时，必须同步核对：

1. `README.md`；
2. 本 `MANIFEST.md`；
3. `00_导航与总览/00_当前有效版本与加载入口.md`；
4. `00_导航与总览/11_知识层级与分类规范.md` 与 `12_阅读与使用路径.md`；
5. `07_元数据知识图谱与Skill/` 内跨文件引用；
6. `08_机器数据与Schema/validation_v4.json` 的 `load_rule` 与 `required_current_files`；
7. `08_机器数据与Schema/task_router_v1.json`、`commercial_reasoning_runtime_v1.json`、`benchmark_manifest_v1.json` 的相互引用；
8. 人类阅读镜像与 JSONL/Registry/Schema 的主从关系；
9. 当前树是否残留迁移过程中的重复副本或多个稳定入口；
10. `scripts/benchmark_business_model_universe.py --strict` 是否仍通过；
11. `runtime_harness_latest.json` 的 `tested_commit`、Semantic Anchor Recall 和 `regression.pass` 是否与当前运行一致；
12. Benchmark 失败应先按 K1/R1/W1/C1/E1/F1/S1/T1/O1/B1 定位根因，不得默认通过增加 Atom 修复；
13. **真实项目的人类默认入口必须保持 P01-P20 业务主干；不得因为后台工程扩展而把 Router/Schema/Benchmark 重新放到用户入口之前。**
