# Intent Debugger｜需求澄清与意图对齐

很多人并不是没有想法，而是很难一次把想法说清楚：不知道对应的专业术语、描述比较零散，或者还没有发现其中的矛盾。Intent Debugger 会保留用户原本的目标，把这些表达整理成清楚、结构化、可核对的需求说明，并通过反问确认 AI 与用户是否理解一致。

## 它解决什么问题

你在使用 AI 工具时，是否遇到过这些问题？

- 用 AI 做项目，脑子里明明知道自己想要什么，但就是说不清楚，也不知道对应的专业名词；
- 已经尽量描述了需求，AI 却理解成了另一件事；
- 还没来得及确认 AI 是否真的理解，它就开始设计或写代码，最后发现错在起跑线上。

你不需要先学会写提示词，也不需要把自己的话改得很专业。只要尽量说出想要的效果、使用方式、担心的问题和能想到的例子，哪怕表达得绕、很别扭，或者只能说“有点像某个东西”，这些都可以成为理解需求的依据。

Intent Debugger 会完成以下工作：

- 在有明确依据时找到合适的专业术语，并让你看得出它与原描述的对应关系；
- 梳理目标、使用场景、核心功能、用户流程和约束，形成结构化、可核对的需求说明；
- 区分已经确认的内容、合理但暂定的理解和仍待决定的问题；
- 找出描述中的歧义、冲突、边界情况和潜在风险；
- 通过具体反问，根据你的回答持续修正需求说明，直到你确认理解一致；
- 不主动进入设计或实现，而是依据当前信息说明需求理解的对齐程度。

这里形成的是需求说明，不是技术方案或实施计划。

## 它和 Codex 的 Plan 模式有什么不同

Intent Debugger 回答“到底要做什么”，Plan 回答“在具体项目里准备怎么做”。

| | Intent Debugger | Plan 模式 |
|---|---|---|
| 要回答的问题 | 到底要做什么，为什么做，边界在哪里？ | 已经确认的需求该怎么落地？ |
| 适合的输入 | 口语化想法、愿景、零散功能、互相冲突的描述 | 范围和验收标准已经清楚的任务 |
| 主要产出 | 整理后的需求、尚未解决的问题、需要用户确认的选择 | 结合现有项目形成的实施步骤、改动范围和验证办法 |
| 是否进入技术层面 | 不进入 | 可以进入，但仍不等于已经开始执行 |

这里只比较两者的职责，不规定固定的使用顺序；它们可以独立使用。

## 仓库结构

```text
.
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── improvement-candidate.yml
│   └── PULL_REQUEST_TEMPLATE.md
├── adapters/
│   ├── claude-code/
│   │   └── README.md
│   └── deepseek/
│       └── README.md
├── assets/
│   ├── social-preview.jpg
│   └── xiaohongshu-cover.jpg
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── evals/
│   └── cases.md
├── examples/
│   └── team-knowledge-base.md
└── skill/
    └── intent-debugger/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        └── references/
            └── contribution-candidate.md
```

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

## 预期输出

每轮澄清都包含：

1. 需求梳理
2. 还没说清楚的地方
3. 需要你确认的问题
4. 当前共识
   
第一部分叫“需求梳理”。它先用一两句话给出 AI 当前对需求的整体理解，让用户能马上判断方向有没有理解错；再按目标、场景、功能、流程和约束展开。该换成专业术语的地方就换，但不堆术语，不故作高深。

例如，用户说“在网页中加上首页 / 控制面板 / 键盘这样一级一级跳过去的设计，可以显示出目前所在页面的具体路径”，可以整理成“网页中加入面包屑导航设计”，然后继续写清楚层级、哪些节点能点、点击后去哪里等等，以及还有哪些细节没确定。

在当前共识阶段，AI 会评估当前理解是否已经与用户的需求对齐，以及现有的关键问题是否已经尽可能解决。用户确认后，Intent Debugger 的任务就结束了，不会自动转入任何规划、设计或实现工作。

## 完整示例

[`examples/team-knowledge-base.md`](examples/team-knowledge-base.md) 展示了一个完整过程：用户先用很口语的方式描述“团队找资料”，Intent Debugger 经过两轮确认形成一份已经对齐的需求说明。

## 参与贡献

没有仓库写入权限也可以贡献。用户明确提出时，Intent Debugger 可以先把使用反馈整理成规范的改进候选；用户核对后通过公开 Issue 提交，已经准备好具体修改的用户也可以 Fork 仓库并发起 Pull Request。所有候选都由维护者公开审核，不会因为是 AI 生成就自动写入或合并。

- [提交改进候选](../../issues/new?template=improvement-candidate.yml)
- [查看完整贡献说明](CONTRIBUTING.md)

## 验收

使用 [`evals/cases.md`](evals/cases.md) 中的场景进行行为验收。重点检查实际决策：

- 是否在不改变用户目标的前提下，形成了有依据、可核对的需求理解；
- 是否把合理推断标为暂定理解，而不是用户已经确认的事实；
- 是否发现真实的歧义或冲突；
- 是否提出可直接回答、会影响决策的问题；
- 是否在未对齐前避免技术方案和代码；
- 需求梳理是否既准确，又比用户原话更清楚、更具体；
- 多轮确认时，是否保留已经确认的信息、及时修正错误理解，并停止追问已经解决的问题；
- 表达是否自然，有没有机械套模板、重复解释或滥用术语。
