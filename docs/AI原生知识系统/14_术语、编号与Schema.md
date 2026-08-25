# 术语、编号与 Schema

> 本文件把框架从“人能读的文档”逐步升级为“机器可处理的统一协议”。当前先固定编号和字段族，不冻结所有枚举值。

## 一、编号规则

- `L1-xx`：一级空间；
- `L2-xx-yy`：二级维度；
- `L3-xx-yy-zz`：三级指标；
- `K-*`：标准知识节点；
- `S-*`：来源；
- `E-*`：证据；
- `R-*`：知识关系；
- `D-*`：需求实例；
- `C-*`：消费／调用实例；
- `V-*`：验证／评测实例。

## 二、知识节点最小字段族

```yaml
knowledge_id:
title:
content_type:
canonical_claim:
mechanism:
conditions:
scope:
examples:
counterexamples:
sources:
evidence:
relations:
quality:
subject_value:
learning_fit:
compound_leverage:
market_value:
time_state:
human_state:
ai_state:
risk_state:
version:
updated_at:
```

字段可为空；“不知道”应显式表示，不能由模型自动补成确定事实。

## 三、来源最小字段族

```yaml
source_id:
carrier_type:
title:
author_or_org:
source_level:
published_at:
version:
location:
upstream_source:
independence:
license:
credibility_state:
```

## 四、需求实例最小字段族

```yaml
demand_id:
goal:
time_horizon:
relevance:
scope:
consumer:
mastery_depth:
expected_output:
priority:
trigger:
```

## 五、关系枚举候选

`duplicate`、`paraphrase`、`contains`、`extends`、`supports`、`conflicts`、`counterexample`、`depends_on`、`prerequisite_of`、`complements`、`replaces`、`unrelated`。

关系必须尽量保留“为什么这样判”的证据和来源定位。

## 六、Schema 演进原则

1. 先用 Markdown 维护语义定义，再生成 JSON Schema／YAML Schema；
2. 不因某个模型输出方便就扭曲领域语义；
3. 新增字段前先判断是否能由现有维度组合表达；
4. 字段变更要考虑历史数据迁移和版本兼容；
5. 机器评分必须能回到可解释的 L2／L3 维度，不保留无法解释的单一总分。
