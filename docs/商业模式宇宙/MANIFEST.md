# 商业模式宇宙：统一结构清单

> 当前版本：v4 合并视图。唯一入口：`README.md`。

## 00_导航与总览
- `00_当前有效版本与加载入口.md`
- `01_统一结构与迁移映射.md`
- `10_项目范围与边界.md`
- `11_知识层级与分类规范.md`
- `12_阅读与使用路径.md`
- `13_完整性与反方审计清单.md` — 同时包含仓库结构完整性与商业知识完整性审计
- `20_映射规则风险门与95分验收.md`

## 01_核心机制与组合模式
- `00_商业模式宇宙总览与核心结论.md` — 当前 v4 合并总览
- `01_L1-L2原子机制库.md`
- `02_L3经典与组合模式库.md`
- `03_v3新增组合模式P131-P170.md`
- `04_v4商品角色价格架构Offer转化与场景经济.md`
- `05_机会来源_差异捕获与商业模式变换算子.md` — 横向机会发现/结构变换镜头；不新增 U/Atom/Pattern ID
- `06_v4新增组合模式P171-P200.md` — v4 Pattern 人类阅读镜像；机器事实源仍为 08 中 JSONL
- `10_结构化知识地图/` — 原人工浏览主题地图全量保留

## 02_价值链与利润池
原价值链与利润池目录整体迁入。

## 03_生态与价值交换
原生态与价值交换目录整体迁入。

## 04_案例与行业地图
- `01_商业模式案例与证据/`
- `02_行业商业模式地图/`

## 05_失败模式与迁移
- `01_失败模式库/`
- `02_商业模式迁移路径/`

## 06_真实经济性_返点与治理
- `00_返点门槛后台利益与真实净经济性.md`
- `01_经济真相治理容量风险合同与劳动力层.md`
- `02_v4隐藏利润层单位经济KPI实验与风险.md`

## 07_元数据知识图谱与Skill
- `00_元数据知识图谱与Skill协议.md`
- `01_v3_Skill增量协议.md` — 已使用统一目录当前文件名
- `02_v4_Skill机器加载与Offer决策协议.md` — 当前 v4 Offer/价格/场景/Cohort 决策协议

## 08_机器数据与Schema
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
- `validation_v4.json` — 当前路径感知的结构与版本校验清单

## 09_专题商业模式
- `电子书商业模式.md`

## 90_研究来源与参考
- `00_传统参考知识/`
- `01_研究来源索引.md`
- `02_v3研究来源补充.md`
- `03_v4缺口审计与研究来源.md`
- `99_历史结构/README_v0.1.md`
- `99_历史结构/MANIFEST_v0.1.md`
- `99_历史结构/00_v2基线总览与核心结论.md`
- `99_历史结构/00A_原兼容加载入口_v4.md`

## 结构迁移后的同步纪律

目录发生移动、拆分、合并、重命名或并发新增时，必须同步核对：

1. `README.md`；
2. 本 `MANIFEST.md`；
3. `00_导航与总览/00_当前有效版本与加载入口.md`；
4. `00_导航与总览/11_知识层级与分类规范.md` 与 `12_阅读与使用路径.md`；
5. `07_元数据知识图谱与Skill/` 内跨文件引用；
6. `08_机器数据与Schema/validation_v4.json` 的 `load_rule` 与 `required_current_files`；
7. 人类阅读镜像与 JSONL/Registry/Schema 的主从关系；
8. 同一目录是否出现重复编号前缀导致导航歧义。
