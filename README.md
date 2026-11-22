# Tech Experiments

Technologies worth a look, collected for the team. Each entry has a link and
one line on what it is. Categories and the entries inside them are in
alphabetical order.

<!-- techs:start -->
## AI Agents

| Tech | What it is | Added |
|---|---|---|
| [Cloudflare Code Mode](https://developers.cloudflare.com/agents/tools/codemode/) | Agents write code that calls MCP/tools as typed methods, run in a sandbox, instead of one call each | 2026-10-28 |
| [Craft Anything (ArtCraft)](https://getartcraft.com/apps/craft-anything) | Study a site, app or game with evidence-backed tools, then rebuild your own with a coding agent | 2026-11-05 |
| [Cua](https://cua.ai) | Open-source infrastructure for computer-use agents: sandboxes, desktop driver and SDK | 2026-10-24 |
| [dimensional-drawing](https://github.com/enesozturk/dimensional-drawing) | Agent skill that turns a UI component into an Apple-style dimensional spec sheet, with optional motion | 2026-10-26 |
| [Factory skills (Builder.io)](https://github.com/BuilderIO/skills/blob/main/docs/factory/README.md) | Builder.io agent skills that turn feedback, errors and telemetry into verified, policy-gated PRs | 2026-11-20 |
| [Hallmark](https://www.usehallmark.com/) | Design skill for coding agents: 48 themes and a browser linter that rejects AI-looking pages | 2026-10-24 |
| [Jev Ultrafast](https://github.com/browser-use/jev-ultrafast) | Browser agent where TypeSafe's Jev picks operation and element; a small LLM only types text | 2026-10-28 |
| [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview) | Framework for agent graphs: explicit nodes, edges and shared state, with checkpoints and human approval | 2026-10-30 |
| [OpenBot](https://github.com/CopilotKit/OpenBot) | Self-hosted AI coworkers for teams: own browser, files and granted tools; every action audited | 2026-11-03 |
| [OpenJarvis](https://openjarvis.stanford.edu/) | Stanford's local-first framework for personal AI agents on your own hardware; cloud is optional | 2026-11-22 |
| [Security Audit skill (Cloudflare)](https://github.com/cloudflare/security-audit-skill) | Cloudflare's agent skill for multi-phase security audits; every finding is independently re-verified | 2026-11-20 |
| [UTCP](https://www.utcp.io/) | Lets agents call tools directly via their native APIs, without an MCP-style wrapper server | 2026-11-03 |

## Developer Tools

| Tech | What it is | Added |
|---|---|---|
| [Floci](https://github.com/floci-io/floci) | Free local AWS emulator (LocalStack alternative): no account or token, just docker compose up | 2026-11-03 |
| [Handy](https://handy.computer) | Free, open source offline speech-to-text desktop app: press a shortcut, speak, text is typed | 2026-11-04 |
| [Kiri](https://runkiri.com) | Rust container runtime replacing Docker Desktop/OrbStack; speaks Docker API, ~2.5 ms starts | 2026-11-04 |
| [Rune](https://github.com/anomalyco/rune) | Native GPU-rendered Rust UI framework; headless mode lets agents render to PNG and drive the app | 2026-11-15 |
| [Scala Native](https://scala-native.org/en/latest/) | Ahead-of-time compiler (LLVM) that turns Scala into native binaries: fast startup, no JVM, C interop | 2026-11-22 |
| [UI SDK (Vercel)](https://ui-sdk.dev/) | Vercel's 50+ UI behaviors (focus, popups, selection) for agents to build and drive components | 2026-11-20 |

## LLM Customization

| Tech | What it is | Added |
|---|---|---|
| [Heretic](https://heretic-project.org/) | Training-free LLM editing (abliteration): removes refusals, cuts slop and sycophancy | 2026-11-03 |

## LLM Inference

| Tech | What it is | Added |
|---|---|---|
| [AirLLM](https://github.com/lyogavin/airllm) | Runs 70B+ LLMs on a single 4GB GPU by loading layers on demand, no quantization needed | 2026-10-24 |

## Testing

| Tech | What it is | Added |
|---|---|---|
| [e2e (TesterArmy)](https://github.com/tester-army/e2e) | E2E testing framework for web and mobile: an agent drives the app from natural-language goals | 2026-10-28 |

## Web Standards

| Tech | What it is | Added |
|---|---|---|
| [HTTP QUERY method (RFC 10008)](https://www.rfc-editor.org/rfc/rfc10008.html) | New HTTP method: safe, idempotent, cacheable request with a body, for queries too big for GET | 2026-10-30 |
<!-- techs:end -->

## How to add a tech

Run the script from the repo root. It inserts the entry in the right place
and creates the category if it doesn't exist yet:

```sh
./techs.sh add --name "Cua" --url "https://cua.ai" \
  --category "AI Agents" --desc "One line on what it is"
./techs.sh publish "Add Cua"
```

Editing `README.md` by hand works too. Keep the row format below and run
`./techs.sh check` before you commit:

```
| [Name](https://official-site-or-repo) | One line on what it is | YYYY-MM-DD |
```

- Link the official site. When there isn't one, link the GitHub repo, not an
  article about it.
- No `|` in the description.
- A tech appears once. `check` rejects duplicate names and links.
