# ECC — Harness-Native Operator System for Agentic Work

**A complete operating layer for AI coding and operator agents.** Not just config files: skills, instincts, memory optimization, continuous learning, security scanning, and research-first development. Production-ready agents, skills, hooks, rules, and MCP configurations evolved from intensive daily use building real products.

Works across **Cursor**, **Claude Code**, **Codex**, **OpenCode**, **Gemini**, **Zed**, and **GitHub Copilot**.

---

## What ECC does

ECC wraps any AI agent harness with a structured performance layer:

| Layer | What it provides | Result |
|---|---|---|
| **Skills** | Reusable, on-demand task procedures loaded only when needed | Lean context windows, the agent loads only relevant skills |
| **Instincts** | Patterns that fire automatically on specific triggers | The agent reliably does the right thing (e.g. check rules before acting) without being reminded |
| **Memory optimization** | Hooks that save and load context across sessions | The agent keeps continuity instead of starting cold each session |
| **Continuous learning** | Auto-extracts patterns from sessions into new skills | The system improves itself the more it is used |
| **Security scanning** | Pre-tool hooks detect secrets, block unsafe reads/commands | Prevents leaking credentials and unsafe agent actions |
| **Verification loops** | Checkpoint and continuous evals with grader types | The agent's work is validated, not just produced |

Key topics covered by the system: token optimization, memory persistence, continuous learning, verification loops, parallelization (git worktrees), and subagent orchestration.

---

## Avalara GTM Engineering Use Case

ECC is the **reliability and governance backbone** for Avalara's GTM agents. It is what keeps a sales agent on-task, compliant, and improving instead of hallucinating or losing context mid-workflow.

| GTM need | How ECC delivers | Business result |
|---|---|---|
| Agents must never skip compliance steps | Instincts fire automatically (e.g. always check ROE / opt-out before any outreach) | 100% rule adherence, no manual reminders |
| No leaking of customer data or credentials | Pre-tool security hooks detect secrets and block unsafe reads | Safe to run against Salesforce exports and internal data |
| Agents that keep context across a rep's day | Memory hooks persist and reload session context | The agent remembers the account it was working without re-research |
| Turn one rep's best workflow into a repeatable skill | Continuous learning extracts patterns into shareable skills | Top-performer playbooks scale to the whole GTM org |
| Reliable multi-step qualification and outreach | Verification loops and subagent orchestration | Multi-step tasks complete consistently, the same way every time |
| One stack, many tools | The same skills work across Cursor, Claude, Codex, Gemini | No rewriting when the team changes tools |

**Net impact for Avalara:** ECC turns ad-hoc AI prompting into a governed, repeatable, self-improving GTM engineering platform. It reduces agent error and hallucination on repeated workflows, enforces compliance automatically, and converts individual rep knowledge into org-wide reusable skills.

---

## Quick Start

Get up and running in a couple of minutes. Clone the repo and run the local installer for your harness.

```bash
# Clone the repo
git clone <your-internal-remote>/ECC.git
cd ECC

# Install dependencies (pick your package manager)
npm install        # or: pnpm install | yarn install | bun install
```

### Install for Cursor (Avalara default)

```bash
# macOS/Linux
./install.sh --target cursor typescript
./install.sh --target cursor python golang
```

```powershell
# Windows PowerShell
.\install.ps1 --target cursor typescript
.\install.ps1 --target cursor python golang
```

### Install for Claude Code

```bash
# Minimal profile (rules, agents, commands, core workflow skills; no runtime hooks)
./install.sh --profile minimal --target claude
```

```powershell
.\install.ps1 --profile minimal --target claude
```

Add hooks later only if you want runtime enforcement:

```bash
./install.sh --target claude --modules hooks-runtime
```

### Full manual install (fallback)

Use this only if you want every component installed:

```bash
./install.sh --profile full
```

```powershell
.\install.ps1 --profile full
```

> Do not stack install methods. Pick one path. If a setup looks duplicated, use the uninstaller below before reinstalling.

### Find the right components first

If you are not sure which profile or component to install, ask the packaged advisor from any project:

```bash
npx ecc consult "security reviews" --target cursor
```

It returns matching components, related profiles, and preview/install commands.

### Reset / Uninstall

From the repo root, preview removal first, then remove ECC-managed files:

```bash
node scripts/uninstall.js --dry-run
node scripts/uninstall.js
```

If ECC-managed files look broken, repair before reinstalling:

```bash
node scripts/ecc.js list-installed
node scripts/ecc.js doctor
node scripts/ecc.js repair
```

---

## What's Included (Cursor target)

| Component | Count | Details |
|-----------|-------|---------|
| Hook Events | 15 | sessionStart, beforeShellExecution, afterFileEdit, beforeMCPExecution, beforeSubmitPrompt, and more |
| Hook Scripts | 16 | Thin Node.js scripts delegating to `scripts/hooks/` via a shared adapter |
| Rules | 34 | 9 common (alwaysApply) + 25 language-specific |
| Agents | 48 | `.cursor/agents/ecc-*.md`, prefixed to avoid collisions |
| Skills | Shared + Bundled | `.cursor/skills/` |
| Commands | Shared | `.cursor/commands/` |
| MCP Config | Shared | `.cursor/mcp.json` |

### Cursor hook architecture (DRY adapter pattern)

Cursor exposes more hook events than some harnesses. The `.cursor/hooks/adapter.js` module transforms Cursor's stdin JSON to the shared hook format, so `scripts/hooks/*.js` are reused without duplication.

```
Cursor stdin JSON → adapter.js → transforms → scripts/hooks/*.js (shared)
```

Key hooks:
- **beforeShellExecution** — Blocks dev servers outside tmux, git push review
- **afterFileEdit** — Auto-format + type check + console.log warning
- **beforeSubmitPrompt** — Detects secrets (`sk-`, `ghp_`, `AKIA` patterns) in prompts
- **beforeTabFileRead** — Blocks reading `.env`, `.key`, `.pem` files
- **beforeMCPExecution / afterMCPExecution** — MCP audit logging

### Cursor rules format

Cursor rules use YAML frontmatter with `description`, `globs`, and `alwaysApply`:

```yaml
---
description: "TypeScript coding style extending common rules"
globs: ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx"]
alwaysApply: false
---
```

---

## License

MIT, see [LICENSE](LICENSE).
