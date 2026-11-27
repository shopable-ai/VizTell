# R3-G 证据与实验
输入 602a2f397cab8fdc4b08b758c9fb17212a82e7a3；完整 prompts/R3-G_推理模式宇宙.md blob 574bb1cdbf4a4d2233820f7c7d10492693bd8c4f（R2 07，13项及早期12项），公共入口、runbook、主控、执行地图、第一批完整阅读。结果目录基线不存在。
- Stanford Encyclopedia of Philosophy, Abduction：https://plato.stanford.edu/archives/spr2022/entries/abduction/ ；演绎、归纳、溯因及非必然推断。分类来源支持逻辑区别，不证明AI自动推理正确。
- Google SRE Effective Troubleshooting：https://sre.google/sre-book/effective-troubleshooting/ ；观察、理解系统、假设、控制试验及反证。实际机制比单纯形式推理重要。
- MDN pointer-events：https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/pointer-events ；none不成为普通事件目标，后代可能另有行为。
- MDN elementFromPoint：https://developer.mozilla.org/en-US/docs/Web/API/Document/elementFromPoint ；坐标命中忽略pointer-events:none，跨文档有边界。
- NIST SP800-142：https://csrc.nist.gov/pubs/sp/800/142/final ；组合覆盖，不保证高阶交互完整。
固定真实源码 2d98a00128cf77a7587f62729aee8d5a61a07c5a：
https://github.com/shopable-ai/opendesk-browser/blob/2d98a00128cf77a7587f62729aee8d5a61a07c5a/projects/web-markdown-clipper/trusted/region-picker.js#L22-L56 ：祖先遍历、pre原子、正尺寸、内容与可见性、敏感输入阻断、第一候选；L127-L153 基于 event.target 更新/确认；L155-L189 键盘和状态事件。https://github.com/shopable-ai/opendesk-browser/blob/2d98a00128cf77a7587f62729aee8d5a61a07c5a/projects/web-markdown-clipper/tests/region-picker.test.mjs#L5-L66 ：模拟DOM；L170-L201 tiny/modifier、stale parent及主动扩父。未运行该项目测试，不把源码定义当PASS。
## 实际 Chromium 受控试验（非已安装扩展）
容器 Chromium 144.0.7559.96 headless；Playwright真实浏览器输入 API 产生 trusted pointerdown。构建可见 article#parent 和 span#tiny；最小祖先遍历依源码机制（非完整 regionCandidates，未复制安全过滤/路由）。相同坐标 (71,58)、文本、布局、角色及候选算法；仅修改 span pointer-events。每次记录 elementFromPoint、实际事件target、候选序列。事前预测 auto命中tiny，none命中parent，恢复auto再命中tiny。
| 条件 | elementFromPoint | event.target | candidates | trusted |
|---|---|---|---|---|
|auto|tiny|tiny|tiny,parent|true|
|none|parent|parent|parent|true|
|恢复auto|tiny|tiny|tiny,parent|true|
三个断言均成立。实际验证的是浏览器命中与祖先选择机制，不是生产故障或完整剪藏功能。完整同次执行的原始脚本和日志位于 ../R3-A/browser_probe.py 和 ../R3-A/browser_results.json（同一进程先A后G，两个独立页面；不代表独立Agent）。G不重复存储原始脚本。
## 反例和成本
H1在构造页面可证，真实站点待核；H2 pre或安全过滤可能是正确行为，不能强行最小；H3路由竞态需真实动态测试；H4候选提交需要交互路径记录。直接阈值改动被源码否决但不是所有直接方法都会犯错。组合有效性需要独立、固定预算实验，目前没有模型调用成本/误报率。只使用同模型推理和实际浏览器工具；无独立专家。
