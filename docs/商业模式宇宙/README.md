# 商业模式宇宙

> **唯一总入口。** 原 `universe-business-model/` 与 `商业模式宇宙-带整合/` 已按功能层合并，不再并列维护两套“商业模式宇宙”。

## 当前有效版本：v4 本体 + runtime-v1 + 项目商业推理业务层

- L1：**U01-U27，共 27 个一级设计域**；v4 不新增 U28+。
- L2：**676 个原子机制** = v2 500 + v3 149 + v4 27。
- L3：**P001-P200，共 200 个组合模式**。
- 横向商品角色：**PR01-PR40，共 40 个**，不计入 L2 atom。
- U19 返点/条件性收益层及旧 ID 保持稳定；v3/v4 使用 additive registry / extension，不覆盖旧数据。
- runtime-v1 负责 Task Router、Retriever、最小充分上下文、Data/Evidence Gate、Trace、Benchmark、Ablation、Regression 与知识生命周期。
- **项目商业推理业务层**负责把真实项目、功能、灵感、经营问题、数据或商业现象转成商业决策和真实行动；它是人工默认入口，不新增 U/Atom/Pattern/PR ID。

---

## 一、人工默认入口：项目商业推理工作流

正式目录：

```text
10_任务工作流与运行时/项目商业推理工作流/
```

第一份文件：

```text
10_任务工作流与运行时/项目商业推理工作流/
00_总览_怎样使用项目商业推理工作流.md
```

人工业务总链：

> **项目是什么 → 现在到哪一步 → 当前真正要解决什么 → 最值得补什么信息 → 现在已经拥有什么 → 谁在用、谁付钱、为什么付钱 → 市场现在怎样 → 别人为什么成功、为什么失败 → 哪些商业机制值得借鉴 → 钱在哪里 → 上下游和相邻机会在哪里 → 3-5 套结构不同方案 → 商品与收费 → 经济性 → 竞争与风险 → 成立条件与 A-E 证据评级 → 排序 → 最小验证 → 真实交易 → P20 根据结果持续经营。**

### 业务目录

```text
项目商业推理工作流/
├─ 00_总览_怎样使用项目商业推理工作流.md
├─ 01_P01-P20项目商业推理总工作流.md
├─ 02_真实项目与现实输入入口.md
├─ 03_市场研究_成功失败与证据判断.md
├─ 04_利润池_上下游与相邻机会.md
├─ 05_候选商业方案_商品价格与经济性.md
├─ 06_竞争风险_证据评级与排序.md
├─ 07_最小验证_实际赚钱与持续经营.md
├─ 08_商业现象逆向拆解工作流.md
├─ 09_项目输入输出模板与快速清单.md
└─ 10_真实项目验证_T03_AI_PDF与T04_低价电子书现象_2026-08-25.md
```

P01-P20 是完整地图，不要求任何项目机械跑满。不同现实输入由 `02_真实项目与现实输入入口.md` 选择起点。

旧 `10/03`、`10/05`、`10/06` 路径保留为兼容跳转，避免历史 T01/T02、Runtime 或外部引用断链；不再独立维护第二份业务规则。

---

## 二、统一知识分析主链

> **参与方与需求 → 机会来源/差异/错配 → 价值主张 → 产品/权利包装 → 商品角色 → 获客与渠道 → 供给与交付 → 交易与信任 → 价格架构与 Offer Graph → 返点/条件性经济 → 所有权与治理 → 会计与经济真相 → Front-end/Basket/Cohort 贡献 → 容量/库存/风险/公共激励/财资/合同/劳动力 → 留存复购 → Context Router → 增长复制 → 壁垒与竞争反应 → KPI/增量实验 → 风险治理 → 迁移/退出**

这条知识主链服务 P10-P17 等业务阶段，但不替代人工工作流。

---

## 三、后台运行时主链

中文对应见 `10_任务工作流与运行时/02_端到端商业推理Workflow与知识生命周期.md`。

```text
任务接收
→ 任务路由
→ 项目商业画像
→ 数据/证据门
→ 信息缺口
→ 最小充分上下文
→ 按需外部研究
→ 机会扫描
→ Domain / Atom / Pattern Retrieval
→ 按需商品角色/价格/Offer
→ 价值链/利润池/生态
→ 条件性经济/会计真相
→ 候选生成
→ Unit / Basket / Cohort / Cashflow
→ 竞争/壁垒/风险/反方
→ 实验
→ 排序/淘汰/扩大
→ 商业决策输出
→ Trace
→ Benchmark / Error Classification
→ Knowledge Feedback / Lifecycle
```

后台系统用于支持、实现和质量保障，不是普通人处理真实项目时的第一阅读顺序。

---

## 四、统一目录

```text
docs/商业模式宇宙/
├── README.md
├── MANIFEST.md
├── 00_导航与总览/
├── 01_核心机制与组合模式/
├── 02_价值链与利润池/
├── 03_生态与价值交换/
├── 04_案例与行业地图/
├── 05_失败模式与迁移/
├── 06_真实经济性_返点与治理/
├── 07_元数据知识图谱与Skill/
├── 08_机器数据与Schema/
├── 09_专题商业模式/
├── 10_任务工作流与运行时/
├── 11_Benchmark与回归/
└── 90_研究来源与参考/
```

| 目录 | 唯一职责 |
|---|---|
| `00_导航与总览` | 当前版本、加载入口、边界、分类规范、使用路径、结构完整性、风险门与验收 |
| `01_核心机制与组合模式` | U01-U27、atoms、patterns、Product Roles、价格/Offer、机会来源与变换算子、知识地图 |
| `02_价值链与利润池` | 价值链位置、利润池、成本池、控制点、价值迁移 |
| `03_生态与价值交换` | 多方价值网络、资源交换、合作、激励与治理 |
| `04_案例与行业地图` | 案例证据、实例映射、行业情境化 |
| `05_失败模式与迁移` | 失败机制、反方诊断、阶段迁移与模式演化 |
| `06_真实经济性_返点与治理` | U19、U20-U27、隐藏利润、Cohort Economics、KPI/实验与风险 |
| `07_元数据知识图谱与Skill` | 统一对象模型、知识图谱关系、v2/v3/v4 Skill 协议 |
| `08_机器数据与Schema` | JSONL、Registry、Product Roles、Schema、Validation 与 runtime-v1 机器协议 |
| `09_专题商业模式` | 电子书等具体项目/主题深度商业模型 |
| `10_任务工作流与运行时` | **业务子目录是人工默认入口；同层 00/01/02 是后台运行时与演进协议；04 是历史真实运行记录；旧 03/05/06 为兼容入口** |
| `11_Benchmark与回归` | Rubric、错误分类、Ablation、Regression、T01/T02 与确定性 Harness |
| `90_研究来源与参考` | 研究来源、传统框架、缺口审计、历史结构快照 |

---

## 五、01_核心机制与组合模式当前顺序

```text
00 总览
→ 01 L1-L2 原子
→ 02 L3 经典组合模式
→ 03 P131-P170
→ 04 v4 商品角色/价格/Offer
→ 05 P171-P200 人类阅读镜像
→ 06 机会来源、差异捕获与商业模式变换算子
→ 10 结构化知识地图
```

- `05_v4新增组合模式P171-P200.md` 是机器 P171-P200 JSONL 的人类阅读镜像；
- `06_机会来源_差异捕获与商业模式变换算子.md` 是横向机会发现与重构镜头，不是 U28，也不新增 atom/pattern ID。

---

## 六、推荐路径

- **真实商业项目**：`项目商业推理工作流/00 → 01 P01-P20 → 02 现实入口 → 按需 03-08 → 09 模板/状态 → P20`。
- **已有产品/功能商业化**：`02 已有项目/功能入口 → P06/P07/P11/P14/P15/P18 → 07 真实付费验证`。
- **已有真实经营数据**：直接 `P15 → P17 → P18 → P19/P20`，数据必须改变或验证排序。
- **看到别人赚钱现象**：`08 逆向拆解 → 假设/证据/反证 → P08-P17 → 判断可持续性 → 迁移后重新 P13-P19`。
- **成功/失败案例迁移**：先拆收入、成本、频率、供给、渠道、现金流、壁垒和成立条件，再判断哪些可迁移。
- **快速理解本体**：`README → 00/00_当前有效版本与加载入口 → 01/00 → 01/04 → 01/05 → 01/06 → 06真实经济性`。
- **发现商业机会**：P11/P12 按需调用 `01/06 → U01-U27 → Patterns → 02利润池 → 03生态 → 06真实经济性 → 05失败/迁移`，最后回 P13-P18 收敛。
- **后台运行时/质量保障**：`10/00 → 10/01 → 10/02 → 08机器协议 → 11 Benchmark/Regression`。
- **AI / Agent / Skill**：`00/00 → 07 → 08 → 10后台运行时 → 11`。
- **专题商业化**：先读 `09_专题商业模式/`，再回查通用本体；专题不能替代 P01-P20。

---

## 七、机器加载基线

### v4 本体

```text
atoms = 08_机器数据与Schema/atoms.jsonl
      + 08_机器数据与Schema/atoms_v3_registry.json
      + 08_机器数据与Schema/atoms_v4_registry.json

patterns = 08_机器数据与Schema/patterns.jsonl
         + 08_机器数据与Schema/patterns_v3_extension_P131-P170.jsonl
         + 08_机器数据与Schema/patterns_v4_extension_P171-P200.jsonl

product_roles = 08_机器数据与Schema/product_roles_v4.json
schema = 08_机器数据与Schema/business_model_signature_v4.schema.json
validation = 08_机器数据与Schema/validation_v4.json
rebate_schema = 08_机器数据与Schema/conditional_economics_rebate.schema.json
skill = 07_元数据知识图谱与Skill/02_v4_Skill机器加载与Offer决策协议.md
```

### runtime-v1

```text
task_router = 08_机器数据与Schema/task_router_v1.json
runtime_protocol = 08_机器数据与Schema/commercial_reasoning_runtime_v1.json
benchmark_manifest = 08_机器数据与Schema/benchmark_manifest_v1.json
benchmark_harness = ../../scripts/benchmark_business_model_universe.py
```

runtime-v1 只决定如何使用 v4 知识，不覆盖 v4 本体事实源。

---

## 八、当前真实测试与 Benchmark

### 后台 Benchmark

- `T01`：电子书/PDF 低门槛入口与后端商业化 Seed Case；
- `T02`：AI API usage/commit/overage/企业后端跨场景 Canary。

Harness 验证稳定 ID/数量、Router/Flags、Domain/Asset Recall、最小上下文、基础召回、Ablation；**Harness 分数不等于商业答案 A-E 质量**。

### 业务 Workflow 真实运行

- `T03`：已有 AI PDF 产品与上传/问答/总结/知识库功能；
- `T04`：闲鱼 0.01-3 元电子书反常低价现象。

运行记录：`10_任务工作流与运行时/项目商业推理工作流/10_真实项目验证_T03_AI_PDF与T04_低价电子书现象_2026-08-25.md`。

T03/T04 暴露并已修复：现实入口跳转、P01-P20 跳过规则、Fact/Inference/Assumption/Unknown、H1-H12 逆向拆解、候选去同质化、条件性收益分层、商业行动卡和 P20 状态继承。本轮未发现必须立即新增 U/Atom/Pattern/Schema 的问题。

---

## 九、冲突优先级

1. 本 `README.md` 与 `00_导航与总览/00_当前有效版本与加载入口.md`：版本、路径、加载事实；
2. `10_任务工作流与运行时/项目商业推理工作流/`：真实项目人工业务流程的唯一事实源；
3. `01_核心机制与组合模式/00_商业模式宇宙总览与核心结论.md`：人类可读 v4 本体总览；
4. v4 Registry / Schema / Validation / Skill / P171-P200：当前本体增量层；
5. runtime-v1 Router / Protocol / Benchmark：运行和评测，不得改写稳定本体；
6. v3 与 v2 基线；
7. `90_研究来源与参考/`：来源与历史快照，不作为当前加载入口。

---

## 十、结构迁移与维护纪律

已有统一目录重构的核心本体资产、稳定 U/Atom/Pattern/PR ID 不因本轮业务目录化而改变。本轮采取“新业务目录成为 canonical + 旧 03/05/06 保留兼容入口”的方式，避免外部与历史引用断裂，同时防止继续维护重复规则。

维护规则：

1. 不重排 U01-U27、既有原子 ID、P001-P200、PR01-PR40。
2. 禁止再次创建第二个“商业模式宇宙”顶级目录。
3. 横向问题优先复用 U01-U27，不为商品角色、场景、Offer、机会来源、任务类型机械新增一级域。
4. Product Role、Opportunity Source、Transformation Operator、Pricing Mechanism、Pattern、Instance、Task Family 分开建模。
5. 价格分析必须经过 U19 Net Effective Economics。
6. 低价/免费入口必须核算 Front-end、Basket、True Cohort Contribution 与 Qualified Promo CAC，并设置增量实验和 Kill Condition。
7. 新本体机器对象同步 Registry/Schema/Validation/Skill；新运行时对象同步 Router/Protocol/Benchmark。
8. 目录移动或 canonical 路径变化必须同步 README、MANIFEST、当前有效版本、阅读路径、Skill/Validation 中相关引用，并回读 `main`。
9. 影响商业模式宇宙的修改应运行 `scripts/benchmark_business_model_universe.py --strict`；结构通过不代表商业决策质量提升。
10. 真实项目输出不好时先按项目理解 → 商业问题 → 市场研究 → 成功失败机制 → 利润池 → 上下游 → 候选 → 经济性 → 排序 → 行动 → P20 状态继承排错；只有最后确认为 K1 才优先补本体。

完整性门见 `00_导航与总览/13_完整性与反方审计清单.md`，机器基线见 `08_机器数据与Schema/validation_v4.json`，运行评测见 `11_Benchmark与回归/`。