# 早期具体应用研究 · 延期与保留索引

性质：历史研究资产，不是当前任务。用户纠偏后，当前阶段只完善通用框架。下列早期研究文件并非无价值，但其实际应用、源码分析、浏览器实验和产品验证不适合作为当前阶段完成条件。

核查基线：b34bba95ee43b35a1d9cc986fbede91da6f3c826。原始应用研究提交 3148be698fe8f56e60e540619291125b5a66ba15、9e4edc370c272a9d89b3910093f337a75ef3aa72 的 Git 差异均位于 temp/ai-native-dev/，无该范围外文件修改。此索引不声称已核查其他项目仓库或其他对话的所有操作。

## 一、停用文件（保留原字节、历史路径、证据和状态）

| 专题 | 早期具体研究 | 文件数 |
|---|---|---:|
| R3-A | 阅读目录/滚动条等浏览器交互因素及受控机制实验 | 5 |
| R3-B | AI消息发送队列等具体需求、交付追溯与规则实验 | 5 |
| R3-G | 网页剪藏精确区域选择、源码跟进及浏览器反例实验 | 7 |

### R3-A

- [README.md](../results/R3-A/README.md)
- [browser_probe.py](../results/R3-A/browser_probe.py)
- [browser_results.json](../results/R3-A/browser_results.json)
- [evidence.md](../results/R3-A/evidence.md)
- [status.md](../results/R3-A/status.md)

### R3-B

- [README.md](../results/R3-B/README.md)
- [evidence.md](../results/R3-B/evidence.md)
- [status.md](../results/R3-B/status.md)
- [trace_probe.py](../results/R3-B/trace_probe.py)
- [trace_results.json](../results/R3-B/trace_results.json)

### R3-G

- [README.md](../results/R3-G/README.md)
- [evidence.md](../results/R3-G/evidence.md)
- [exact-source-followup.md](../results/R3-G/exact-source-followup.md)
- [exact_region_candidate_results.json](../results/R3-G/exact_region_candidate_results.json)
- [exact_region_probe.py](../results/R3-G/exact_region_probe.py)
- [exact_region_results.json](../results/R3-G/exact_region_results.json)
- [status.md](../results/R3-G/status.md)

共17个文件。原始状态文件 status.md 记录当时的应用研究缺口；它不是 FRAMEWORK-STATUS.md，也不是当前执行任务。当前研究默认不读取、不运行上述应用实验脚本，不恢复其待办，不把其结论当成通用框架已经验证的证据。

## 二、必须保留并继续使用的成果

- results/R3-A 至 R3-O 中的全部 FRAMEWORK.md 与 FRAMEWORK-STATUS.md（15份专题正文及15份状态）。
- R3-O 的总体导航、研究状态和来源追溯。
- 原始 reference/ 与 prompts/：按现行阶段规则读取其通用知识问题，旧应用执行要求延期。
- framework/README.md 与 RESEARCH-STAGES.md：当前研究导航与边界。
- launch/：已经纠正方向的现行启动文件。

A、B、G 的通用认识已经在相应 FRAMEWORK.md 中重新提炼。无需为了隔离应用研究而删除整个专题目录。

## 三、处置原则

不整体回滚，不删除原有研究成果，不继续旧业务待办。当前使用明确的文件级输入边界与停用索引实现逻辑隔离；没有移动历史文件，以保持引用、追溯及已有对话路径有效。需要物理归档或永久删除时，另行确认精确路径及受影响引用，先验证备份，再用独立的非强制提交完成。

未来仅当用户明确启动实际应用阶段时，才可按需恢复本索引中的相关历史成果，并重新确认版本、证据、适用范围及授权。不自动运行旧代码、部署或访问外部项目。

历史提交中曾新增的 C/D/E/F/H 普通 status.md 已在 c6dbd81b8531d9e20ad2aff66880c4ccdf9a3854 移除，当前对应 FRAMEWORK-STATUS.md 均存在。无需恢复这些临时状态文件。
