# R3-A 证据、差量与验证记录
## 输入和来源
研究输入提交 602a2f397cab8fdc4b08b758c9fb17212a82e7a3；完整 prompts/R3-A_因素宇宙.md blob 03108b39677850f9d62f86f7c2aaafb89cdf6c7b，含 R2 02；README、runbook、主控、地图、批次01均读完。结果目录基线不存在（API 404）。遵守隔离，不读取 VizTell 其他目录。
外部来源（检索核实，未将其当本框架有效性证明）：
- SEI Quality Attribute Workshop collection：https://www.sei.cmu.edu/library/quality-attribute-workshop-collection/ ：业务驱动、场景、环境与响应。适用架构质量场景；小修复不需要组织完整 workshop。
- NIST SP 800-142：https://csrc.nist.gov/pubs/sp/800/142/final ：多参数交互测试与覆盖取舍。非充分性证明。
- W3C CSS Overflow 3：https://www.w3.org/TR/css-overflow-3/Overview.html ：classic/overlay scrollbar 尺寸、位置是 UA 决定；不得推定固定宽度适用所有环境。
- W3C Pointer Events：https://www.w3.org/TR/pointerevents/ ：pointer capture 的重定向机制；自定义控件规则不等于 OS 原生滚动条。
固定 OpenDesk 源码 2d98a00128cf77a7587f62729aee8d5a61a07c5a：
- https://github.com/shopable-ai/opendesk-browser/blob/2d98a00128cf77a7587f62729aee8d5a61a07c5a/projects/reading-toc/trusted/view.js#L9-L49 ：28px/10% 边缘保护，host pointer-events:none，panel/toggle auto，skin none；折叠 hover 会扩大可交互宽度。
- 同文件 L101-L110 foldPoint；L391-L395 grab setPointerCapture，不能直接推断它抢原生滚动条。
- https://github.com/shopable-ai/opendesk-browser/blob/2d98a00128cf77a7587f62729aee8d5a61a07c5a/projects/reading-toc/trusted/placement.js#L17-L59 ：visual viewport 与约束计算。
- https://github.com/shopable-ai/opendesk-browser/blob/2d98a00128cf77a7587f62729aee8d5a61a07c5a/projects/reading-toc/tests/scrollbar-clearance.test.mjs#L13-L52 ：五种宽度、左右、classic/visual viewport 的几何断言，非原生拖动。未运行该项目测试。
## 受控 Chromium 机制实验（实际执行）
运行容器 Chromium 144.0.7559.96，Python Playwright，800×600；headless。非完整扩展、非原生 OS 滚动条、非真实用户故障复现。人为定义网页模拟 track/thumb（24px 或32px），button 38×46、top140、z-index100。thumb top80 height180。pointerdown 捕获，pointermove 更新 window.scrollTo。唯一操纵因素是 track 宽及 button 右距/是否接收事件。每次先归零 scroll，起点 x=800-width+2,y=155，鼠标拖到 y=290，8步。事前判据：trusted pointerdown target=knob 且 scrollY>0。执行命令 python browser_probe.py（归档完整原始实验脚本见本目录；G 使用同一脚本后半段的独立页面）。观测：
| 宽度 | 模式 | x | trusted target | scrollY | 判据 |
|---:|---|---:|---|---:|---|
|24|重叠|778|toc|0|不满足|
|24|28px预留|778|knob|700|满足|
|24|pointer-events:none|778|knob|700|满足|
|32|重叠|770|toc|0|不满足|
|32|28px预留|770|toc|0|不满足|
|32|pointer-events:none|770|knob|700|满足|
六组与实验前 assert 一致（验证机制而非六组产品 PASS）。不能把32px假设当真实站点宽度或把禁用交互当最终修复。
## 对照/反例
直接方案覆盖普通拖动、位置；因素方案增加三类可测差异：命中目标（不再只看视觉）、宽度与状态的交互、目录自身仍可操作。已有源码证明重复添加28px无价值，实验实证两个宽度下规则的不同效果。没有独立 baseline 生成，不能声称发现率提高百分比；成本未计量。潜在误报：浏览器原生滚动区域不受 DOM hit test 同样控制；有必要用真实 OS / 网站验证。最重要的未知是用户故障发生瞬间的实际滚动容器和 pointer event 路径。
