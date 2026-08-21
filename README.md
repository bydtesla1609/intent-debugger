# Intent Debugger（意图调试器）

用户的想法也可能有“bug”：词不达意、前后矛盾，或者自己还没想清楚。Intent Debugger 放在想法和执行之间，先把这些问题找出来，再把零散描述整理成一份清楚、具体、可以继续使用的需求说明。

## 它解决什么问题

当用户只说“我想做一个……”时，AI 很容易一边猜需求，一边开始设计甚至写代码。最后得到的东西也许做得很完整，却不是用户真正想要的。

用户不需要先学会写提示词，也不需要知道准确的专业名词。只要尽量把想要的效果、使用方式、担心的问题和能想到的例子说出来即可，哪怕表达得绕、别扭，或者只能说“像某个东西”。把这些话转成清楚、具体的需求，并在可能的专业概念上标明对应关系，是 Intent Debugger 的工作。

整理后的内容不是单纯润色，而是一份供双方核对的对照稿：用户可以直接判断“这就是我的意思”，也能及时指出“这里理解偏了”。

Intent Debugger 先做五件事：

1. 忠实复述已经表达的意图；
2. 整理功能目标、核心功能、用户流程和约束；
3. 区分已知信息、合理暂定和待澄清事项；
4. 指出会影响结果的歧义、冲突、边界和风险；
5. 用具体问题推动双方达成明确一致。

它不会擅自加功能，也不会把猜测写成已经确认的需求。

## 它和 Plan 模式有什么不同

Intent Debugger 处理的是需求，Plan 处理的是执行。最顺手的使用顺序是：

```text
模糊想法 → Intent Debugger → 已确认的需求 → Plan → 实现与验证
```

| | Intent Debugger | Plan 模式 |
|---|---|---|
| 要回答的问题 | 到底要做什么，为什么做，边界在哪里？ | 已经确认的需求该怎么落地？ |
| 适合的输入 | 口语化想法、愿景、零散功能、互相冲突的描述 | 范围和验收标准已经清楚的任务 |
| 主要产出 | 整理后的需求、尚未解决的问题、需要用户确认的选择 | 结合现有项目形成的实施步骤、改动范围和验证办法 |
| 是否进入技术层面 | 不进入 | 可以进入，但仍不等于已经开始执行 |

两者都可能提问，只是问题服务的决策不同：Intent Debugger 问的是产品和需求选择，例如“普通成员能不能删除资料”；Plan 更可能问实施取舍，例如“要不要兼容现有数据”。

如果需求本身还说不清楚，直接进入 Plan，往往只会得到一份很细致的错误计划。反过来，如果任务已经明确到几乎没有分歧，也不用为了走流程强行调用 Intent Debugger。

这里的 Plan 指 AI 编码工具在执行前制定落地方案的阶段。Codex、Claude Code 和其他工具的具体模式会变化，但这份职责划分不依赖某一家产品。

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
├── examples/
│   └── team-knowledge-base.md
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

## 需求梳理

第一部分叫“需求梳理”。它先用一两句话说明 AI 对需求的整体理解，再按目标、场景、功能、流程和约束展开。该换成专业术语的地方就换，但不堆术语，也不把一句简单的话包装得故作高深。

例如，用户说“首页 / 控制面板 / 键盘这样一级一级跳过去”，可以整理成“网页中加入面包屑导航”，然后继续写清楚层级、哪些节点能点、点击后去哪里，以及还有哪些细节没确定。

## 预期输出

每轮澄清都包含：

1. 需求梳理
2. 还没说清楚的地方
3. 需要你确认的问题
4. 当前共识

这四部分不需要写得一样长，也不用为了显得完整而硬凑内容。没有明显冲突就直接说明，没有必要追问就不要制造问题。

即使用户一开始就说“直接开发”，只要关键需求仍不明确，Skill 还是先把问题问清楚。等关键问题解决、用户确认需求并明确同意进入下一阶段后，再交给 Plan 或实现阶段。

## 完整示例

[`examples/team-knowledge-base.md`](examples/team-knowledge-base.md) 展示了一个完整过程：用户先用很口语的方式描述“团队找资料”，Intent Debugger 经过两轮确认形成需求，最后再把结果交给 Plan。示例里不会提前讨论技术栈或代码。

## 验收

使用 [`evals/cases.md`](evals/cases.md) 中的场景进行行为验收。重点检查实际决策，而不是逐字匹配标题：

- 是否忠实保留原意；
- 是否把推测标为待确认，而非伪装成事实；
- 是否发现真实的歧义或冲突；
- 是否提出可直接回答、会影响决策的问题；
- 是否在未对齐前避免技术方案和代码。
- 需求梳理是否既准确，又比用户原话更清楚、更具体；
- 表达是否自然，有没有机械套模板、重复解释或滥用术语。

## 边界

本 Skill 负责把需求说清楚，不负责架构、技术选型、开发排期或代码实现。需求已经完整时，简短确认就够了，不要为了套流程继续制造问题。
