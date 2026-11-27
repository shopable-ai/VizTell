# 实验输出保存约定

本目录当前只有运行约定，不包含人工伪造的框架执行结果。

## 目录约定

~~~text
experiments/
  superpowers/
    inline/workspace/
    inline/generated/
    subagent/workspace/
    subagent/generated/
  bmad/
    oneshot/workspace/
    oneshot/generated/
    dispatch/workspace/
    dispatch/generated/
    party-mode/generated/
~~~

## 每次实验必须保存

- 开始前工作区状态和基线提交。
- 框架版本与宿主 Skill 清单。
- 自然语言输入原文和 Skill 调用顺序。
- 设计文档、SPEC、Plan 等框架真实生成文件。
- 用户批准前后的行为记录。
- 测试命令、原始输出和退出码。
- Agent 调度调用、Agent ID、任务输入、结果和恢复记录。
- 代码 Diff、审核报告和修复过程。
- 浏览器级真实操作证据。

## 禁止替代

- 不手工写一份看似框架生成的 SPEC 或 Plan。
- 不把同一模型切换角色后的回答称为独立 Agent 结果。
- 不用源码中写着“必须执行”证明宿主真的执行。
- 不用测试文件存在代替测试实际运行。
- 不用测试通过代替浏览器真实新标签页验收。
- 不在没有恢复操作时宣称中断恢复已验证。

## 路由实验说明

共享案例是一个小型、低风险、单目标需求。按 BMAD bmad-build 的源码规则，预计选择 Oneshot；实际选择必须以真实运行生成的 SPEC frontmatter route 和执行步骤为证据。

如需验证 Dispatch，可另做受控路由探针，明确增加需求缺口或不可逆条件；不得篡改主案例输入来伪造 Dispatch 结果。
