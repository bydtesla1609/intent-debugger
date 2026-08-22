# DeepSeek adapter

DeepSeek's Chat Completion API accepts a `system` message, but its official API documentation does not define a Claude Code-style directory that automatically discovers `SKILL.md`. This adapter therefore loads the shared Skill as a system prompt instead of pretending that file-based installation is available.

## Supported path

Use this adapter with the DeepSeek API or a client that lets you set a system prompt:

1. Read the complete contents of `skill/intent-debugger/SKILL.md`.
2. Send that content as the first `system` message.
3. Send the user's rough idea as the following `user` message.
4. For each stateless API request, retain the system message and the relevant clarification history until alignment is complete.

For ordinary requirements clarification, `SKILL.md` is sufficient. If the user explicitly asks to package feedback about Intent Debugger as a public contribution candidate, append the complete contents of `skill/intent-debugger/references/contribution-candidate.md` to the same system message as well. DeepSeek cannot follow a local Markdown link unless the calling application supplies that file's contents.

Minimal message shape:

```json
{
  "messages": [
    {"role": "system", "content": "<complete contents of skill/intent-debugger/SKILL.md>"},
    {"role": "user", "content": "<rough idea to clarify>"}
  ]
}
```

The model name, SDK, and transport are deliberately left to the calling application; they do not change Intent Debugger's behavior.

## Web-chat fallback

If a DeepSeek interface does not expose a system prompt, paste the complete `SKILL.md` contents at the start of a new conversation and ask the model to apply them to the next message. This is a best-effort fallback, not persistent installation, and its instruction priority may be weaker than an API system message.

Official reference: [DeepSeek Chat Completion API](https://api-docs.deepseek.com/api/create-chat-completion/).
