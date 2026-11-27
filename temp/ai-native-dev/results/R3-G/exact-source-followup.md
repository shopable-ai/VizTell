# R3-G 补证：精确源码与动态操作资格

2026-11-27 同一会话增量。在此前的机制实验之后，进一步验证真实源代码，避免把简化算法证据误当正式模块。

## 来源和复现
- OpenDesk Browser 只读，commit 2d98a00128cf77a7587f62729aee8d5a61a07c5a。
- 固定源码：https://github.com/shopable-ai/opendesk-browser/blob/2d98a00128cf77a7587f62729aee8d5a61a07c5a/projects/web-markdown-clipper/trusted/region-picker.js
- GitHub fetch_file 提供完整 blob，复制至隔离容器后通过 Git blob SHA-1 校验：45f09fae8c948bfd748b66c01d3066282e550b1c，10615 bytes。不是改写的候选算法。
- Chromium 144.0.7559.96 + Python Playwright。隔离 about:blank 页面，导入准确模块字节，模拟提取回调只返回节点ID和测试文本。没有生产站点、真实用户数据、安装或实际 Markdown 持久化。初次 fake HTTPS origin 导航被容器策略阻断，改为 about:blank + set_content，不请求外部站点。
- 把固定版本源码保存为 region-picker.js（不在本研究仓库复制整个外部项目），运行：
  `python exact_region_probe.py /path/to/region-picker.js`
  `python exact_region_probe.py /path/to/region-picker.js --candidate`
  候选只在进程内替换一个检查点；原始文件和外部仓库均不写入。输出 JSON 已归档。脚本包含原始失败的断言，成功退出表示按预设复现，并非原始11项全部通过。

## 实验
判据：指定选区ID或禁止提取、结束后清理浮层；Ctrl必须返回append=true。两项反例先确认新计算候选为空，再以可信鼠标事件进行提交。每次重建页面和单次选区会话。
| 条件 | 原模块 | 研究候选 |
|---|---|---|
| tiny, pointer-events:auto | tiny | tiny |
| tiny, pointer-events:none | parent | parent |
| 恢复 auto | tiny | tiny |
| pre 内 token | code（原子设计） | code |
| Ctrl追加 | tiny+append=true | 同 |
| password input | 未提取，取消 | 同 |
| hash 地址变化 | 未提取，取消 | 同 |
| ArrowUp 主动扩大 | parent | parent |
| ArrowUp/Down + Enter | tiny | tiny |
| hover 后同一元素 aria-hidden=true | 仍提取 tiny，不符合新资格 | 取消，未提取 |
| hover 后父级 contenteditable=true | 仍提取 tiny，不符合新资格 | 取消，未提取 |

原模块符合预设行为9/11，另外2项反例准确复现；研究候选11/11符合。本轮未运行完整扩展测试，不应外推为实际剪藏产品质量通过；也不是独立随机A/B或证明所有问题被修复。

## 根因和候选
源码 regionCandidates 在候选计算时检查 BLOCKED；update 遇到同一 target 且缓存节点 isConnected 时复用；commit 只在 target 变化或节点断开时更新，并未重新确认该选区仍符合当下资格。aria-hidden 或祖先 contenteditable 可变化但节点保持连接、鼠标目标不变。此处依据代码阅读及受控反例，确认了该构造条件下的资格失效机制；不能断言是用户原始小区域问题的唯一根因。

研究候选：提交前重新计算 regionCandidates(lastTarget||target,doc,win)，若选中的 node 不在新候选中则明确取消而不悄悄选择其它区域。保留主动扩父选择只在其仍符合资格时。此候选只验证局部机制，性能开销（祖先/查询）、动态DOM大页面、遮挡、快捷键修饰、网站兼容、错误本地化、真正的Markdown转换和安装运行仍需独立评估。候选英文错误信息只是实验标记，不可直接发布。

## 可复用的研究增量
1. 反事实/可控实验区别真实命中变化与候选优先级；边界审查又发现对象连通性与操作资格的差异。
2. 提出跨项目不变量（候选）：对动态对象执行最终操作前，使用当下环境重新验证必要的资格/权限/身份条件；若失效，不沿用历史缓存或扩大操作范围。权限、队列和会话等场景须单独实证；不可机械引入全量重复查询。
3. 方法比较仍是单模型同任务推演，没有独立对照，不能以本例22次运行证明AI推理普适增益。真实新价值是两个精确源码反例和一个已验证的局部修正候选。原项目未修改。
