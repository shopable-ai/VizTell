# 来源追溯及待核验历史线索

基线：VizTell main 3818e787402fa528ebc402488be677673c8c8e0b；A–H 纠偏提交 b1f629ccc529a4d5ad3021cbe38714fd6bbb989b。所有专题提示词仍按原文件作为线索，未覆盖。原始备份 reference/原始资料_完整备份.txt blob 55ad4c10edfcc2a426aba4810246740b8e58f7ab。
| 专题 | 完整提示词 blob |
|---|---|
| A | 03108b39677850f9d62f86f7c2aaafb89cdf6c7b |
| B | 714113b6fcd626beee0633779dba4661a342f602 |
| C | 91a892555dbdcc74ac2b93405654f54772d84c1b |
| D | f26bc8016687a5416bbcbab930ae1dc3d3ce4a8b |
| E | 611ef230c7b3eed2a06365b26cc703632359992a |
| F | 071318b724cb27dcf4ddef9003d9c8e9dfdfd243 |
| G | 574bb1cdbf4a4d2233820f7c7d10492693bd8c4f |
| H | 026846cc7603e684adb5fe96dcdde01a870b35e9 |
| I | 71f7399fed720fdc7fee4fea4b98a5ae01d50544 |
| J | fbe06d39c3fe4108e2a092206f626eb336488789 |
| K | bce6f5a5be6dea846ad0a44a9d26bacf5369d241 |
| L | 3cdf224bacb6d839982ffbce6f113c4fab376c5c |
| M | a63dcaa23cf11222e8cfeaabf44bf374f2f35ae1 |
| N | 6f715d6710e96e9aa4d60c47b8af36aeda640b49 |
| O | d4abd9d419fa826f3dfef5f3ce4ed1e45c1f834e |

## 外部来源及作用边界
- SWEBOK topics: https://www.computer.org/education/bodies-of-knowledge/software-engineering/topics — 专业知识域导航，不是AI方法完整性证明。
- NASA SEH 4.0: https://www.nasa.gov/reference/4-0-system-design-processes/ — 递归、迭代的设计关系。
- ISO/IEC/IEEE 42010 公开摘要: https://www.iso.org/standard/74393.html — 架构与描述的区分；未声称通读标准正文。
- IREB CPRE glossary: https://cpre.ireb.org/en/downloads-and-resources/glossary — 需求术语与分类。
- SFIA: https://sfia-online.org/en/about-sfia/how-sfia-works — 技能与责任等级的区分。
- 并发规则更新前曾只读查看 ai-native-project-os 的结构说明（02bce098b7a3fb5002400305ba8ba7e4b6f9b554）；未做业务或源码研究、未运行、未修改。当前框架以授权目录中的原始参考及通用理论为依据，按最新规则不继续访问该仓库。

## 尚未恢复
原始备份第88、783、1125行提及35模型族、14主领域；第463、503–504行提及九机制；第101、103行提及两份历史文件名称。本轮在授权目录未取得对应原始逐项定义，不能据名称或数量造出“恢复版”。原R2的16研究维度已按reference/02逐项映射；5/7/10环节按reference/09建立阅读对应。禁止越出授权目录找旧资料。

## F2/F3新增通用来源
- https://cpre.ireb.org/en/concept/requirements-elicitation — 需求来源、方法选择、冲突与确认。
- https://plato.stanford.edu/entries/abduction/ — 解释性推断与必然性区别；2025-06-18修订。
- https://www.nasa.gov/reference/6-8-decision-analysis/ — 分析强度及多属性、不确定性与利益相关者。
- https://www.w3.org/TR/prov-overview/ — 来源、派生及版本信息。以上为本轮公开HTML资料查阅，未宣称完整标准核验。


## F2/F3成熟方法补证
H第6节已记录15项逐项理论出处、直接/间接支持与访问限制；原FTA链接403、Scenario-Based RE链接418，保留边界。原reference/04、05、06、07、08、09、10、11、12的名录已逐项核对；不是恢复历史缺失35/14和九机制。SWEBOK官方topics曾通过搜索摘要核对18领域，本次直接打开返回403；新增二级知识入口是独立候选而非逐字复刻官方章节。

## R1及R1.1来源差量（当前）

起点main 0a099415f3f951e2110fa5958c0e870f12922cba；相对用户提供a1bcb624965ce436ed680d7ded207f0b617cb70a新增3次社会运行规则研究提交，未覆盖。核心正文commit b95512b5f7611e63cebce490c6d4117aa2c4a70e、2e29be672268ff0db6ec2db42ddb42975ed6e473；当前裁决见O §11。R1来源以各专题R1段落及O §10为历史记录。

| 来源 | 实际核查范围 | 支持内容及限制 |
|---|---|---|
| IEEE SWEBOK V4.0a https://ieeecs-media.computer.org/media/education/swebok/swebok-v4.pdf | 官方PDF目录印刷xx–xxiii，第16–18章 | 三大基础、人因、AI、度量、实验、数值误差等；非全书审查 |
| ACM/IEEE-CS/AAAI CS2023 https://csed.acm.org/wp-content/uploads/2025/11/CS2023-Report.htm 及 https://csed.acm.org/knowledge-areas/ | 公开报告目录及知识领域 | 计算与数学基础交叉索引；非全部知识或资格证明 |
| Sutcliffe等1998 Supporting Scenario-Based Requirements Engineering，DOI 10.1109/32.738340，https://research.cs.vt.edu/ns/cs5724papers/1.motivatingreuse.tpgap.sutcliffe.scenarios.pdf | 高校镜像PDF印刷1072–1074首页、方法段/图 | 场景路径、知识复用、异常与问题模式；非全文或穷尽证明 |
| Pearl 2010 https://pmc.ncbi.nlm.nih.gov/articles/PMC2836213/ | 公开HTML摘要、导论及方法导航 | 观察、干预、反事实与因果假设/识别；G二元模型为本轮反例 |
| Letier/van Lamsweerde 2002 https://research.dial.uclouvain.be/entities/publication/bce90b0f-32b2-4546-a319-469a22cad035 DOI 10.1109/ICSE.2002.1007958 | 作者机构摘要 | 目标可实现性、主体监测/控制；C形式定义和量词反例为本轮推导 |
| Lamport 1978 https://apice.unibo.it/bin/view/Publication/LamportAcmcomm21 DOI 10.1145/359545.359563 | 机构摘要 | 事件先后偏序，非统计因果/全序物理时间 |
| Benveniste等2018 https://doi.org/10.1561/1000000053 | 出版方摘要 | 契约设计与验证/抽象细化用途；D/E反例非全文定理复刻 |
| Alpern & Schneider 1985 DOI 10.1016/0020-0190(85)90056-0 | 公开摘要 | 安全/活性辨析入口；复杂公平/活性理论待独立复核 |

其余成熟方法沿用H §6及R1记录，未声称重读全部原论文/标准。A–O原提示词独立任务段、R2主要分册与原始备份关键区段用于恢复；重复附录按同源处理，原始1168行未逐字重读。新形式判据、选择规则、交叉关系与反方均为单模型综合及抽象推演，非软件实验或独立评审。
