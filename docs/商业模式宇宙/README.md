# 商业模式宇宙

> **唯一总入口。** 原 `universe-business-model/` 与 `商业模式宇宙-带整合/` 已按功能层重新合并，不再并列维护两套“商业模式宇宙”。

## 当前有效版本：v4 合并视图

- L1：**U01-U27，共 27 个一级设计域**；v4 不新增 U28+。
- L2：**676 个原子机制** = v2 500 + v3 149 + v4 27。
- L3：**P001-P200，共 200 个组合模式**。
- 横向商品角色：**PR01-PR40，共 40 个**，不计入 L2 atom。
- U19 返点/条件性收益层及旧 ID 保持稳定；v3/v4 使用 additive registry / extension，不覆盖旧数据。

统一分析主链：

> **参与方与需求 → 机会来源/差异/错配 → 价值主张 → 产品/权利包装 → 商品角色 → 获客与渠道 → 供给与交付 → 交易与信任 → 价格架构与 Offer Graph → 返点/条件性经济 → 所有权与治理 → 会计与经济真相 → Front-end/Basket/Cohort 贡献 → 容量/库存/风险/公共激励/财资/合同/劳动力 → 留存复购 → Context Router → 增长复制 → 壁垒与竞争反应 → KPI/增量实验 → 风险治理 → 迁移/退出**

## 统一目录

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
└── 90_研究来源与参考/
```

## 各层职责

| 目录 | 唯一职责 |
|---|---|
| `00_导航与总览` | 当前版本、加载入口、边界、分类规范、使用路径、结构完整性、风险门与验收 |
| `01_核心机制与组合模式` | 当前总览、U01-U27、L2 atoms、L3 patterns、v4 商品角色/价格/Offer、P171-P200 人类阅读镜像、机会来源与变换算子、主题知识地图 |
| `02_价值链与利润池` | 价值链位置、利润池、成本池、控制点、价值迁移 |
| `03_生态与价值交换` | 多方价值网络、资源交换、合作、激励与治理 |
| `04_案例与行业地图` | 案例证据、实例映射、行业情境化 |
| `05_失败模式与迁移` | 失败机制、反方诊断、阶段迁移与模式演化 |
| `06_真实经济性_返点与治理` | U19、U20-U27、隐藏利润、Cohort Economics、KPI/实验与风险 |
| `07_元数据知识图谱与Skill` | 统一对象模型、知识图谱关系、v2/v3/v4 Skill 协议 |
| `08_机器数据与Schema` | JSONL、Registry、Product Roles、Schema、Validation 的唯一机器目录 |
| `09_专题商业模式` | 电子书等具体项目/主题完整商业模型 |
| `90_研究来源与参考` | 研究来源、传统框架、缺口审计、历史结构快照 |

## 01_核心机制与组合模式的当前顺序

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

其中：

- `05_v4新增组合模式P171-P200.md` 是机器 P171-P200 JSONL 的人类阅读镜像；
- `06_机会来源_差异捕获与商业模式变换算子.md` 是横向机会发现与重构镜头，不是 U28，也不新增 atom/pattern ID。

## 推荐路径

- **快速理解**：`README → 00/00_当前有效版本与加载入口 → 01/00 总览 → 01/04 商品角色/价格/Offer → 01/05 P171-P200 → 01/06 机会来源/变换算子 → 06 真实经济性`
- **发现商业机会**：`01/06 机会来源/差异/错配 → 变换算子 → 01/01 U01-U27 原子 → 01/02/03/05 Pattern → 02 利润池 → 03 生态 → 06 真实经济性 → 05 失败/迁移`
- **设计真实项目**：`01 核心机制/商品角色/Offer → 02 价值链 → 03 生态 → 06 真实经济性 → 05 失败/迁移 → 04 案例/行业`
- **AI / Agent / Skill**：`00/00_当前有效版本与加载入口 → 07_元数据知识图谱与Skill → 08_机器数据与Schema`
- **专题商业化**：先读 `09_专题商业模式/`，再回查 `01/02/03/06`；专题不能反向替代通用宇宙。

## 机器加载基线

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

## 冲突优先级

1. 本 `README.md` 与 `00_导航与总览/00_当前有效版本与加载入口.md`：版本、路径、加载事实。
2. `01_核心机制与组合模式/00_商业模式宇宙总览与核心结论.md`：当前人类可读 v4 总览。
3. v4 Registry / Schema / Validation / Skill / P171-P200：当前增量层。
4. v3 Registry / Schema / Skill / P131-P170：U20-U27 与 v3 增量。
5. v2 JSONL 与 L1-L3 基线正文：稳定旧 ID 基线。
6. `90_研究来源与参考/`：来源、传统兼容与历史快照，不作为当前加载入口。

## 结构迁移完整性结论

统一目录重构已按重构前提交 `357da7578308acff03ef9cda1f7f745102db53a8` 与重构提交 `d29da8b9bf918e9c5877f0982120f0ae9094b0fb` 对账。核心旧子树与 v4 关键机器/正文资产保持原 tree/blob SHA，**当前审计未发现实质内容资产丢失**。

重构后发现并已修复：

- v3 Skill 的旧平铺文件名引用；
- v4 Skill 的旧编号式引用与机器加载路径；
- `validation_v4.json` 的旧平铺必需文件名；
- P171-P200 缺少与 P131-P170 对称的人类阅读索引；
- 仓库根 README 缺少商业模式宇宙入口；
- 并发重构产生的机会来源/Pattern 编号冲突。当前固定为 **05=P171-P200、06=机会来源/变换算子**。

完整性门见 `00_导航与总览/13_完整性与反方审计清单.md`，机器基线见 `08_机器数据与Schema/validation_v4.json`。

## 不丢失与维护规则

1. 不重排 U01-U27、既有原子 ID、P001-P200、PR01-PR40。
2. 禁止再次创建第二个“商业模式宇宙”顶级目录。
3. 横向问题优先复用现有 U01-U27，不为商品角色、场景、Offer、机会来源机械新增一级域。
4. Product Role、Opportunity Source、Transformation Operator、Pricing Mechanism、Pattern、Instance 必须分开建模。
5. 价格分析必须经过 U19 Net Effective Economics。
6. 低价/免费入口必须核算 Front-end、Basket、True Cohort Contribution 与 Qualified Promo CAC，并设置增量实验及 kill condition。
7. 新机器对象同时更新 Registry/Schema/Validation/Skill。
8. 每次目录移动后同步更新 README、MANIFEST、知识层级、阅读路径、Skill、Validation，并回读 GitHub `main` 验证。
