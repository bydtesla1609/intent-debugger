# Intent Debugger behavior checks

These cases test decisions and boundaries, not exact wording. A response may use the user's language and natural formatting as long as it preserves the required five-part contract.

## Case 1 — Vague product idea

**Prompt**

> 我想做一个帮团队找资料的东西，最好方便一点。

**Expected behavior**

- Rephrase only the stated goal; do not decide what “资料” means or add collaboration features.
- Mark target users, material types, search behavior, and “方便”的 meaning as unresolved.
- Ask concrete questions that distinguish plausible product boundaries.
- Do not recommend a framework, database, search engine, architecture, or code.

## Case 2 — Colloquial feature description

**Prompt**

> 一个网页索引，一级一级跳过去，比如首页/控制面板/键盘。

**Expected behavior**

- Identify “面包屑导航（Breadcrumb Navigation）” as a likely professional term without treating uncertain details as confirmed.
- Preserve the described hierarchy and stepwise navigation.
- Ask whether each level is clickable, how the current level appears, and what happens when a path is unavailable if those decisions remain unknown.
- Do not add global navigation, search, routing libraries, or visual design requirements.

## Case 3 — Conflicting expectations

**Prompt**

> 我想做一个完全离线的笔记应用，而且手机和电脑上的内容要随时自动同步，不依赖任何外部设备或服务。

**Expected behavior**

- Surface the conflict between complete isolation and cross-device automatic synchronization.
- Explain the decision that must be made without choosing for the user.
- Ask which constraint has priority or what form of local transfer is acceptable.
- Do not hide the conflict behind a technical proposal.

## Case 4 — Premature implementation request

**Prompt**

> 帮我把会员系统写出来，能登录、付费、到期提醒，直接开始写代码。

**Expected behavior**

- Explain that implementation is blocked by decision-critical requirements such as actors, membership states, payment scope, reminder behavior, and acceptance boundaries.
- Produce the five clarification sections and no code or technical stack.
- Do not treat “直接开始写代码” as permission to invent the missing product rules.

## Case 5 — Alignment reached

**Conversation state**

The user has answered every material question, corrected the draft, and says: “需求没问题，就按这个版本。” They have not asked to start design or implementation.

**Expected behavior**

- Keep the five sections concise, state that the requirements are aligned, and mark the clarification gate complete.
- Ask whether to enter the next phase.
- Do not automatically provide design, technical planning, or code.

## Failure conditions

Any of the following is a failure:

- invented features or constraints are presented as confirmed;
- a material contradiction is ignored;
- questions are generic, repetitive, or unrelated to a decision;
- technology choices, architecture, or code appear before the exit gate and explicit authorization;
- the response mechanically invents issues after the requirements are already complete.
