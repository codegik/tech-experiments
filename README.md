# Tech Experiments

Technologies worth a look, collected for the team. Each entry has a link and
one line on what it is. Categories and the entries inside them are in
alphabetical order.

<!-- techs:start -->
## AI Agents

| Tech | What it is | Added |
|---|---|---|
| [Cua](https://cua.ai) | Open-source infrastructure for computer-use agents: sandboxes, desktop driver and SDK | 2026-10-24 |
| [Hallmark](https://www.usehallmark.com/) | Design skill for coding agents: 48 themes and a browser linter that rejects AI-looking pages | 2026-10-24 |

## LLM Inference

| Tech | What it is | Added |
|---|---|---|
| [AirLLM](https://github.com/lyogavin/airllm) | Runs 70B+ LLMs on a single 4GB GPU by loading layers on demand, no quantization needed | 2026-10-24 |
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
