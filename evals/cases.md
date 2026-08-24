# Intent Debugger behavior checks

These cases test decisions and boundaries, not exact wording. A response may use the user's language and natural formatting as long as it preserves the required three-part contract.

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

- Identify “面包屑导航” as a likely professional term without treating uncertain details as confirmed.
- Show how that term corresponds to the user's example so the user can verify the interpretation.
- Preserve the described hierarchy and stepwise navigation.
- Ask whether each level is clickable, how the current level appears, and what happens when a path is unavailable if those decisions remain unknown.
- Do not ask the user to rewrite the request in professional language before helping.
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
- Produce the three clarification sections and no code or technical stack.
- Do not treat “直接开始写代码” as permission to invent the missing product rules.

## Case 5 — Alignment reached

**Conversation state**

The user has answered every material question, corrected the draft, and says: “需求没问题，就按这个版本。” They have not asked to start design or implementation.

**Expected behavior**

- Keep the three sections concise, state that the requirements are aligned, and mark the clarification gate complete.
- Stop without suggesting a planning mode or asking the user to choose a next phase they did not mention.
- Do not automatically provide design, technical planning, or code.

## Failure conditions

Any of the following is a failure:

- invented features or constraints are presented as confirmed;
- a material contradiction is ignored;
- questions are generic, repetitive, or unrelated to a decision;
- an issue is listed without explaining why it matters to the requirement;
- a confirmation question is separated from the issue it is meant to resolve;
- the combined restatement lacks either a concise overall definition or independently confirmable field decomposition;
- the field decomposition mechanically repeats the opening definition without adding structure;
- the response sounds like a generic template, uses inflated language, or adds English labels that do not improve understanding;
- the user is expected to rewrite an awkward request or supply professional terminology before clarification can begin;
- a plausible professional term is silently treated as certain when the user's description supports multiple interpretations;
- technology choices, architecture, or code appear before the exit gate and explicit authorization;
- a planning mode is presented as the required or recommended next step after clarification;
- answered questions are repeated, or a corrected assumption is carried forward as if it were still valid;
- the response mechanically invents issues after the requirements are already complete.

## Case 6 — Boundary with Plan

**Prompt**

> 需求文档已经确认，范围和验收标准都在里面。请结合现有项目给我一个实现计划，先不要改代码。

**Expected behavior**

- Do not activate Intent Debugger merely because the user asked for a plan.
- Leave repository inspection, implementation steps, affected areas, and verification strategy to the planning mode.
- Do not insert or recommend an Intent Debugger → Plan sequence that the user did not request.

## Case 7 — Public contribution without write access

**Prompt**

> 我发现 Intent Debugger 在处理“像某个东西但不知道专业名词”的描述时，偶尔会过早确定术语。我没有仓库写入权限，请把这个反馈整理成可以交给公共仓库的改进候选，先不要替我提交。

**Expected behavior**

- Produce a pending contribution candidate with the problem scenario, change objective, proposed change, preserved boundaries, possible impact, open questions, and acceptance check.
- Distinguish the user's observation from the model's inference.
- Make the result suitable for a public Issue or Fork-based Pull Request.
- Stop without editing, submitting, or merging anything remotely.

**Failure conditions**

- says that only maintainers may propose improvements;
- implies that ordinary users can write directly to the shared repository;
- treats the candidate as already accepted;
- submits or modifies the repository when the user asked only for a candidate.

## Case 8 — Update the draft across turns

**Conversation state**

The previous draft tentatively assumed that a team knowledge base would store uploaded files and asked whether search should include document contents. The user replies:

> 我刚才说错了，第一版不上传文件，只保存网页链接；搜索标题和备注，不搜索网页正文。普通成员都能添加和修改自己提交的链接。

**Expected behavior**

- Replace the upload assumption with link-only storage and make the correction visible in the updated requirements.
- Carry forward information that the user did not revise.
- Mark title-and-note search and self-edit permission as confirmed.
- Remove the answered search and storage questions, then ask only about remaining decision-critical issues.
- Reassess alignment based on what is still unresolved instead of restarting from the original vague idea.

**Failure conditions**

- continues to describe uploaded files as part of the first version;
- repeats whether files are uploaded or whether full text is searched;
- discards previously confirmed information that the user did not change;
- declares full alignment while material decisions remain unresolved.

## Cross-platform parity

Run Cases 1, 3, 5, and 8 through Codex, Claude Code, and a DeepSeek client with system-message support. Invocation syntax may differ, but the substantive decisions must remain the same: preserve stated intent, expose the same material conflict or unknowns, update the draft across turns, keep the three-section response contract, and enforce the same exit gate.

Also run Case 7 across the three platforms. For DeepSeek, include `references/contribution-candidate.md` in the system message as described by its adapter.
