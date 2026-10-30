# Tech Experiments

Technologies worth a look, collected for the team. Each entry has a link and
one line on what it is. Categories and the entries inside them are in
alphabetical order.

<!-- techs:start -->
## AI Agents

| Tech | What it is | Added |
|---|---|---|
| [Cloudflare Code Mode](https://developers.cloudflare.com/agents/tools/codemode/) | Agents write code that calls MCP/tools as typed methods, run in a sandbox, instead of one call each | 2026-10-28 |
| [Cua](https://cua.ai) | Open-source infrastructure for computer-use agents: sandboxes, desktop driver and SDK | 2026-10-24 |
| [dimensional-drawing](https://github.com/enesozturk/dimensional-drawing) | Agent skill that turns a UI component into an Apple-style dimensional spec sheet, with optional motion | 2026-10-26 |
| [Hallmark](https://www.usehallmark.com/) | Design skill for coding agents: 48 themes and a browser linter that rejects AI-looking pages | 2026-10-24 |
| [Jev Ultrafast](https://github.com/browser-use/jev-ultrafast) | Browser agent where TypeSafe's Jev picks operation and element; a small LLM only types text | 2026-10-28 |

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
