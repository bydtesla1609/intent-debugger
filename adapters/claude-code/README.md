# Claude Code adapter

Claude Code natively supports the same `SKILL.md` structure used by Intent Debugger, so this adapter does not maintain a second prompt.

## Install

Copy the entire `skill/intent-debugger` directory to one of Claude Code's supported locations:

- Personal, available in every project: `~/.claude/skills/intent-debugger/`
- Project, available only in one repository: `.claude/skills/intent-debugger/`

The resulting path must contain `SKILL.md` directly:

```text
~/.claude/skills/intent-debugger/SKILL.md
```

Restart Claude Code only if the top-level skills directory did not exist when the session started. Otherwise, Claude Code detects `SKILL.md` changes during the current session.

## Invoke and verify

Use `/intent-debugger` to invoke it explicitly, or describe a vague product or feature idea and allow Claude Code to select it from the frontmatter description. Use `/skills` to confirm that it is discoverable.

Do not copy `agents/openai.yaml` into a Claude-specific configuration file. It is Codex UI metadata and is not part of the shared behavior contract.

Official reference: [Extend Claude with skills](https://code.claude.com/docs/en/skills).
