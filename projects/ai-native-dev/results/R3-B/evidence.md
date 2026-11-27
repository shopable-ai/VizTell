# R3-B 证据与验证
研究输入 602a2f397cab8fdc4b08b758c9fb17212a82e7a3，完整 prompts/R3-B_链路宇宙.md blob 714113b6fcd626beee0633779dba4661a342f602（含R2 03、04、05）。README/runbook/00/地图/01完整读取；results基线不存在。
- NASA SWE-047 双向追溯：https://swehb.nasa.gov/spaces/SWEHBVB/pages/32604501/SWE-047%2B-%2BTraceability%2BData ；用于需求遗漏、无需求来源的实现、变更影响。不是小项目强制全流程。
- Google SRE Troubleshooting：https://sre.google/sre-book/effective-troubleshooting/ ；观察与系统理解形成假设，受控改变或观察检验；避免相关性当因果。局部修复可短路径。
- 真实历史验收：https://github.com/shopable-ai/opendesk-browser/blob/2d98a00128cf77a7587f62729aee8d5a61a07c5a/projects/ai-send-queue/ACCEPTANCE-CTRL-ENTER.zh-CN.md ，L3-13状态层级；L19-24历史缺陷修复；L30-45历史测试与失败；L51-62行为和mock限制；L64-86候选身份和安装缺口；L92-105历史评分及发布阻断。本轮未重新运行历史命令，未验证本地忽略日志。
- 当前源码测试定义：https://github.com/shopable-ai/opendesk-browser/blob/2d98a00128cf77a7587f62729aee8d5a61a07c5a/projects/ai-send-queue/tests/shortcut-integration.test.mjs#L148-L211 ，包括unknown后的禁止重放、编辑接管与原生尝试守卫；定义不是执行结果。
## 实际运行的验收链路变异实验
运行 Python trace_probe.py；固定预先定义必要门：源码、构建、包、全测通过、无发布阻断、安装/执行候选身份匹配、四组原生行为证据匹配。四组行为=trusted_shortcut/fifo_no_replay/draft_ime/route_owner。历史案例基于报告事实：已实现/构建/候选通过，246/247、未安装和运行r16、release blocked。r16/hash-A等仅合成标识，并非实际SHA。基线仅检查三个里程碑，不代表真实OpenDesk流程（真实报告本就明确blocked）。
| 输入 | 预期能发布 | 简单状态基线 | 新门 |
|---|---|---|---|
|历史报告|否|是|否|
|假设完整|是|是|是|
|安装旧候选|否|是|否|
|执行旧回执|否|是|否|
|全测失败|否|是|否|
|发布阻断未解除|否|是|否|
|缺原生IME|否|是|否|
|FIFO证据属于旧版|否|是|否|
实际8/8与预定义断言相同。七个拒绝含一个真实报告的状态映射、六个人工单缺口变异；不能将此称为独立验证、真实产品全测、统计性改进或通过发布。规则的全测要求适用于这个项目当前阻断场景；其他项目若有合法例外应有明确授权和风险记录，不照搬成通用绝对条件。原始运行脚本和记录见同目录。
## 反方自审
- 过度追溯会拖慢小修：裁剪到目标/行为/实际修改/证据。
- 身份匹配是必要非充分：真实行为测试可能遗漏、环境不对、回执可能伪造；需要可信运行来源。
- 低风险变更可沿用不受影响的证据，但不能沿用受影响行为的历史运行结论。
- 本轮对照基线故意简化，真正严谨对照应随机分配相同输入给独立Agent，以盲评判断遗漏、错误和工时。