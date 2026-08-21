# Intent Debugger（意图调试器）

用户的想法可视为可能有bug的程序，而 Intent Debugger 是一个位于“想法”和“方案”之间的需求澄清 Skill。它把模糊、口语化、直觉性的描述整理成专业、结构化、可确认的需求草稿，并在进入设计或实现前识别歧义、冲突和风险。

## 它解决什么问题

当用户说“我想做一个……”“帮我设计一个……”或只描述了零散想法时，Agent 很容易过早补全需求、选择技术栈甚至开始写代码。Intent Debugger 会先完成五件事：

1. 忠实复述已经表达的意图；
2. 整理功能目标、核心功能、用户流程和约束；
3. 区分已知信息、合理暂定和待澄清事项；
4. 指出会影响结果的歧义、冲突、边界和风险；
5. 用具体问题推动双方达成明确一致。

它不会擅自添加功能，也不会把尚未确认的假设写成既定需求。

## 仓库结构

```text
.
├── adapters/
│   ├── claude-code/
│   │   └── README.md
│   └── deepseek/
│       └── README.md
├── README.md
├── evals/
│   └── cases.md
└── skill/
    └── intent-debugger/
        ├── SKILL.md
        └── agents/
            └── openai.yaml
```

核心方法只在 `skill/intent-debugger/SKILL.md` 中维护；平台适配器只说明如何加载这份规则，不复制或改写核心方法。`agents/openai.yaml` 仅提供 Codex 的界面元数据。

## 在 Codex 中使用

将 `skill/intent-debugger` 目录复制到 Codex 的个人 Skill 目录：

```text
$CODEX_HOME/skills/intent-debugger
```

重新加载 Skill 后，可以显式调用：

```text
使用 $intent-debugger 帮我澄清这个想法：我想做一个帮助团队找资料的工具。
```

它也允许在明显属于模糊需求澄清的场景中被自动选择。

## 在 Claude Code 中使用

Claude Code 原生支持 `SKILL.md`。把 `skill/intent-debugger` 复制到以下任一位置：

- 个人级：`~/.claude/skills/intent-debugger/`
- 项目级：`.claude/skills/intent-debugger/`

然后输入 `/intent-debugger` 显式调用，也可以由 Claude Code 根据 `description` 自动选择。详见 [`adapters/claude-code/README.md`](adapters/claude-code/README.md)。

## 在 DeepSeek 中使用

DeepSeek API 没有与 Claude Code 相同的文件式 Skill 发现机制。对于 DeepSeek API 或支持 system prompt 的客户端，把 `skill/intent-debugger/SKILL.md` 的完整内容作为首条 `system` 消息，把具体想法作为 `user` 消息。详见 [`adapters/deepseek/README.md`](adapters/deepseek/README.md)。

## 结构化、专业化、规范化复述

“需求复述”和“结构化说明”合并为一个输出部分。它先用一两句话给出专业、准确的需求定义，再按目标、场景、功能、流程和约束展开；既能检查整体理解，也能暴露缺失信息，不再让两个相邻部分重复表达同一内容。

以“首页 / 控制面板 / 键盘一级一级跳转”为例，合并后的输出会先将其定义为“面包屑导航”，再在同一部分中列明层级路径、可点击节点、跳转流程和待确认约束。

## 预期输出

每轮澄清都包含：

1. 结构化、专业化、规范化复述
2. 潜在问题
3. 澄清问题
4. 对齐确认

即使用户一开始就提到“开发”或“实现”，只要关键需求仍不明确，Skill 仍先完成澄清。只有关键问题已经解决、用户确认需求并明确授权进入下一阶段后，才退出本 Skill；设计、技术选型和代码不属于本 Skill 的输出。

## 验收

使用 [`evals/cases.md`](evals/cases.md) 中的场景进行行为验收。重点检查实际决策，而不是逐字匹配标题：

- 是否忠实保留原意；
- 是否把推测标为待确认，而非伪装成事实；
- 是否发现真实的歧义或冲突；
- 是否提出可直接回答、会影响决策的问题；
- 是否在未对齐前避免技术方案和代码。
- 合并后的复述是否同时包含准确的整体定义和可逐项确认的字段拆解。

## 边界

本 Skill 负责需求澄清，不负责产品设计、架构设计、技术选型、项目排期或代码实现。若用户提供的需求已经完整且明确，它应简短确认对齐状态，而不是为了套流程制造无意义问题。
