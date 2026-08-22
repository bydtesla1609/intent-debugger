# Intent Debugger（意图调试器）

用户的想法也可能有“bug”：词不达意、前后矛盾，或者自己还没想清楚。Intent Debugger 专门处理这些还没有说清楚的需求，把零散描述整理成一份清楚、具体、可以继续使用的需求说明。

## 它解决什么问题

当用户只说“我想做一个……”时，AI 很容易一边猜需求，一边开始设计甚至写代码。最后得到的东西也许并不是用户真正想要的。

用户不需要先学会写提示词，也不需要知道准确的专业名词。只要尽量把想要的效果、使用方式、担心的问题和能想到的例子说出来即可，哪怕表达得绕、别扭，或者只能说“像某个东西”。把这些话转成清楚、具体的需求，并在可能的专业概念上标明对应关系，是 Intent Debugger 的工作。

整理后会得到一份有依据、可核对的需求理解：它不是把用户的原话简单换一种说法，而是把零散描述之间的关系梳理清楚。用户可以直接判断“啊对对对，就是这样”，也能及时指出“这里理解错了”。

Intent Debugger 将会完成以下任务：

1. 根据用户提供的信息，形成一份有依据、可核对的需求理解；
2. 整理功能目标、核心功能、用户流程和约束等关键信息；
3. 区分已知信息、合理暂定和待澄清事项；
4. 指出会影响结果的歧义、冲突、边界和风险；
5. 用具体问题推动双方达成明确一致。

## 它和 Codex 的 Plan 模式有什么不同

Intent Debugger 处理的是需求，Plan 处理的是执行。

| | Intent Debugger | Plan 模式 |
|---|---|---|
| 要回答的问题 | 到底要做什么，为什么做，边界在哪里？ | 已经确认的需求该怎么落地？ |
| 适合的输入 | 口语化想法、愿景、零散功能、互相冲突的描述 | 范围和验收标准已经清楚的任务 |
| 主要产出 | 整理后的需求、尚未解决的问题、需要用户确认的选择 | 结合现有项目形成的实施步骤、改动范围和验证办法 |
| 是否进入技术层面 | 不进入 | 可以进入，但仍不等于已经开始执行 |

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

在当前共识阶段，AI 会评估当前理解是否已经与用户的需求对齐，以及现有的关键问题是否已经尽可能解决。用户确认后，Intent Debugger 的任务就结束了；它不会自动转入任何规划、设计或实现工作，也不会替用户决定下一步做什么。

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
- 是否在未对齐前避免技术方案和代码。
- 需求梳理是否既准确，又比用户原话更清楚、更具体；
- 表达是否自然，有没有机械套模板、重复解释或滥用术语。
