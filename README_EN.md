<p align="center">
  <a href="README.md">简体中文</a>
  &nbsp;·&nbsp;
  <strong>English</strong>
</p>

<p align="center">
  <img src="assets/social-preview.jpg" alt="Intent Debugger: requirements clarification and intent alignment" width="960">
</p>

<h1 align="center">Intent Debugger</h1>

<p align="center">
  <strong>Requirements clarification and intent alignment</strong><br>
  Turn hard-to-express ideas into clear, specific, and verifiable requirements.
</p>

<p align="center">
  <a href="skill/intent-debugger/SKILL.md"><img src="https://developers.openai.com/favicon.svg" alt="Codex icon" width="20" height="20"></a>
  <a href="skill/intent-debugger/SKILL.md"><img src="https://img.shields.io/badge/Codex-Skill-111827" alt="Codex Skill"></a>
  &nbsp;
  <a href="adapters/claude-code/README.md"><img src="https://claude.ai/favicon.svg" alt="Claude Code icon" width="20" height="20"></a>
  <a href="adapters/claude-code/README.md"><img src="https://img.shields.io/badge/Claude_Code-Compatible-D97757" alt="Claude Code Compatible"></a>
  &nbsp;
  <a href="adapters/deepseek/README.md"><img src="https://www.deepseek.com/favicon.ico" alt="DeepSeek icon" width="20" height="20"></a>
  <a href="adapters/deepseek/README.md"><img src="https://img.shields.io/badge/DeepSeek-Compatible-4D6BFE" alt="DeepSeek Compatible"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/bydtesla1609/intent-debugger?color=2563eb" alt="License"></a>
  <a href="https://github.com/bydtesla1609/intent-debugger/stargazers"><img src="https://img.shields.io/github/stars/bydtesla1609/intent-debugger?style=flat&amp;color=f5a623" alt="GitHub Stars"></a>
  <a href="metrics/acquisitions.json"><img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fbydtesla1609%2Fintent-debugger%2Fmain%2Fmetrics%2Facquisitions-badge.json" alt="Total acquisitions"></a>
  <a href="https://github.com/bydtesla1609/intent-debugger/releases/latest/download/intent-debugger-skill.zip"><img src="https://img.shields.io/github/downloads/bydtesla1609/intent-debugger/intent-debugger-skill.zip?label=ZIP%20downloads&amp;color=7c3aed" alt="ZIP downloads"></a>
</p>

<p align="center">
  <a href="#-quick-start">⚡ Quick start</a>
  &nbsp;·&nbsp;
  <a href="#-usage-example">📝 Usage example</a>
  &nbsp;·&nbsp;
  <a href="#-how-is-this-different-from-plan-mode">🧐 Compared with Plan</a>
  &nbsp;·&nbsp;
  <a href="#-contributing">🤝 Contributing</a>
</p>

## ✏ Before we begin

When a user asks an AI to design a project or feature, the AI may respond with a long list of implementation techniques. To someone unfamiliar with those terms, the answer can look professional while still making it difficult to tell whether the AI understood the request. Starting with the **desired outcome, usage, and functional boundaries** makes it easier to form a requirements understanding that both sides can read and verify.

The underlying problem is that ideas are often difficult to express clearly in one attempt. You may already know roughly what the result should look like but not know the corresponding professional term; you may describe the idea in detail and still be misunderstood; or the AI may start designing or coding before either side has checked that the direction is correct.

Intent Debugger does not require you to learn professional prompt writing first. Describe the outcome, usage, concerns, and examples in your own words. Even if the wording is awkward or incomplete, it will organize that information into a **structured and consistent requirements draft** so you can judge whether the AI understood what you actually want to build.

## 🧩 What it does

Each clarification turn has three parts:

1. **🧭 Requirements draft**: gives a concise overall interpretation, then organizes the goal, scenario, core behavior, user flow, and constraints.
2. **❓ Issue clarification and confirmation**: for each consequential issue, explains what is unclear, why it matters, and asks a specific, directly answerable question that affects the requirement.
3. **✅ Current alignment**: distinguishes confirmed information, tentative interpretations, and unresolved decisions, then states whether the requirements are aligned.

Until the user confirms alignment, Intent Debugger keeps updating the same draft: it preserves settled information, applies corrections, and asks only about decisions that still matter.
Intent Debugger finishes when the user confirms the requirements, all decision-critical questions are answered, and no major ambiguity remains. It does not automatically move into planning, design, or implementation.

## 🧐 How is this different from Plan mode?

Intent Debugger answers “What exactly should be built?” Plan mode answers “How should an already-defined requirement be implemented in this project?”

| | Intent Debugger | Plan mode |
| --- | --- | --- |
| Main question | What should be built, why, and where are the boundaries? | How should the confirmed requirement be implemented? |
| Best input | Conversational ideas, visions, scattered features, or conflicting descriptions | A task with a clear scope and acceptance criteria |
| Main output | A clarified requirements draft, unresolved decisions, and confirmation points | Implementation steps, affected areas, and verification methods based on the current project |
| Technical detail | Does not enter the implementation layer | May discuss implementation, but does not itself begin execution |

This is a comparison of responsibilities, not a required sequence. Either tool can be used independently.

## ⚡ Quick start

To get only the core skill, download [`intent-debugger-skill.zip`](https://github.com/bydtesla1609/intent-debugger/releases/latest/download/intent-debugger-skill.zip). It extracts to a complete `intent-debugger` folder that you can place in the directory used by your platform.

The “total acquisitions” badge combines full repository clones with downloads of the official `intent-debugger-skill.zip` release asset. It measures how often the project was actively obtained, not installations or active users. [View the public metric breakdown](metrics/acquisitions.json).

### <img src="https://developers.openai.com/favicon.svg" alt="Codex icon" width="22" height="22"> Codex

Copy [`skill/intent-debugger`](skill/intent-debugger) into your personal Codex skills directory:

```text
$CODEX_HOME/skills/intent-debugger
```

Reload skills, then invoke it explicitly:

```text
Use $intent-debugger to clarify this idea: I want to build a tool that helps a team find shared materials.
```

Codex may also select the skill automatically when a request clearly involves clarifying vague requirements.

### <img src="https://claude.ai/favicon.svg" alt="Claude Code icon" width="22" height="22"> Claude Code

Claude Code can load `SKILL.md`. Copy [`skill/intent-debugger`](skill/intent-debugger) to either location:

- Personal: `~/.claude/skills/intent-debugger/`
- Project: `.claude/skills/intent-debugger/`

Invoke it explicitly with `/intent-debugger`, or let Claude Code select it from the frontmatter `description`. See the [Claude Code adapter](adapters/claude-code/README.md) for details.

### <img src="https://www.deepseek.com/favicon.ico" alt="DeepSeek icon" width="22" height="22"> DeepSeek

The DeepSeek API does not provide the same file-based skill discovery mechanism. In the DeepSeek API or a client that supports a system prompt, send the complete contents of [`SKILL.md`](skill/intent-debugger/SKILL.md) as the first `system` message, then send the idea as the `user` message. See the [DeepSeek adapter](adapters/deepseek/README.md) for details.

> All three platforms use the same platform-neutral core skill. The adapters document how to load it; they do not claim identical live behavior across every client or model version.

## 📝 Usage example

Original description:

> I want something on the website that goes Home / Control Panel / Keyboard, level by level, and shows me where I am.

Intent Debugger first connects the description to a useful professional term:

> Add **breadcrumb navigation** to the website to show the user's current location in the hierarchy and allow navigation back to parent levels.

It then checks the details that still affect the requirement: which levels are clickable, whether the current page is clickable, how long paths should be displayed, and how the path is determined when a user enters the page from another route. The answers are written back into the same requirements draft.

[View the full team knowledge base example (Chinese) →](examples/team-knowledge-base.md)

## 🤝 Contributing

You can contribute without direct write access to the repository. Intent Debugger can organize your feedback into a reviewable improvement candidate for a public Issue. If you already have a concrete change, you can also fork the repository and open a Pull Request.

- [Submit an improvement candidate](https://github.com/bydtesla1609/intent-debugger/issues/new?template=improvement-candidate.yml)
- [Read the contribution guide](CONTRIBUTING.md)
- [Browse Issues](https://github.com/bydtesla1609/intent-debugger/issues)

All candidates are reviewed publicly by the maintainer. AI-generated content is not written or merged automatically.

## 📖 Behavioral checks

The scenarios in [`evals/cases.md`](evals/cases.md) check the skill's decisions and boundaries rather than merely checking whether it prints fixed headings.

<details>
<summary><strong>View the main acceptance criteria</strong></summary>

- Forms an evidence-based, verifiable requirements understanding without changing the user's goal;
- Marks reasonable inferences as tentative instead of presenting them as user-confirmed facts;
- Finds real ambiguities, conflicts, boundary cases, and risks;
- Explains why each consequential issue matters and asks a directly answerable confirmation question;
- Avoids technical proposals and code before alignment;
- Preserves confirmed information across turns, applies corrections, and stops repeating resolved questions;
- Uses natural language without mechanical templates, repetition, or unnecessary terminology.

</details>

## 📄 License

This project is open source under the [MIT License](LICENSE).

<p align="center">
  <strong>Clarify what should be built, then verify whether the AI truly understood you.</strong><br>
  If this project helps you, consider giving it a Star ⭐
</p>
