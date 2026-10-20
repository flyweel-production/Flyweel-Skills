# AGENTS.md

Guidance for AI coding agents working in this repository.

> `CLAUDE.md` is a symlink to this file.

## What this repo is

Agent skills for the [Flyweel](https://flyweel.co) MCP server. The skills are plain text: there is no build and no package. Customers install them straight from GitHub with `npx skills add flyweel-production/flyweel-skills`, or as a Claude Code plugin.

`main` is what customers install. It is protected: changes go through a pull request and CI must pass.

## Layout

```
skills/<name>/SKILL.md          one folder per skill; folder name = `name` in frontmatter
skills/<name>/references/       optional extra files a skill loads on demand
evals/evals.json                test questions each skill was built against
scripts/readability.py          reading-ease and jargon check (CI)
.claude-plugin/                 Claude Code plugin + marketplace manifests (also adds the Flyweel MCP server)
```

Skill format: [agentskills.io/specification](https://agentskills.io/specification).

## Checks

Run before every pull request. CI runs the first two.

```bash
python3 scripts/readability.py                 # every skill and README.md: reading ease >= 70, no listed jargon
npx skills add . --list                        # all six skills parse
claude plugin validate .claude-plugin/plugin.json
```

## Writing rules

- Write for the business owner, not the media buyer. Short sentences, everyday words. If `readability.py` fails, reword; do not edit its word list to get a pass.
- A skill states only what the data confirms. If the Flyweel MCP does not expose a link, the skill must not infer it.
- Skills that change something (a card budget, a freeze) show a preview first and act only after the user says yes. Keep it that way.
- Never put real account data, card numbers or customer names in a skill, an example or an eval.
- Keep the two older skill names (`flyweel-mcp-deep-ad-analysis`, `ad-performance-analyser-flyweel`) as they are. Existing installs and links depend on them.

## Changing a skill

1. Pick the questions for that skill from `evals/evals.json`.
2. Run each with a fresh agent that has only the skill file and a connected Flyweel MCP server. Keep the answers.
3. Make the change.
4. Run them again with fresh agents. Run at least one question twice. If two runs on the same data give different money figures, a rule is loose: find the sentence and fix it.
5. Ask each run to list every sentence that made it guess. That list is where the next fix comes from.
6. Say in the pull request what the answers were before and after.

Keep every test run read-only. Never pass a `confirmToken`, and never call `set_card_budget`, `freeze_card`, `unfreeze_card`, `issue_card`, `trigger_sync`, `select_ad_accounts` or `connect_ad_platform`.

## Flyweel MCP server behaviour the skills rely on

Each of these shaped a rule in a skill. Check a skill still handles them before changing it.

- **No link from a card to an ad account.** A card charge names the merchant, not the ad account, so card skills work per platform and never put money on an ad account. Google is the exception: its charge description carries the account number.
- **`query_metrics` can start a sync.** A read returns `syncTriggered: true` when data is stale. Skills never call `trigger_sync`, but a sync may start anyway.
- **The `query_metrics` description gets cut off** in some clients before the CRM metric names. `flyweel-real-cash-payback` sends one probe query to work around it.
- **One CRM query fails the whole batch** when no CRM is connected. Send CRM queries in a call of their own.
- **`account.spendRestrictions.budget`** copies the limit, and its balance stays at zero while cards spend. Ignore it.
- **`list_cards` does not state the account's currency.** Read it from the transactions.
- **Setup status and `query_metrics` can disagree** on whether a platform is connected. Report both and go with `query_metrics`.
- **Google spend can come back with a null currency.** Treat it as "cannot see".
- **Named results live in `extendedMetricsAvailable`**, not the main metric list. `conversions` is a broad count; prefer the named result (for example `registration`).
- **A refused card charge is not retried quickly.** `flyweel-card-top-up` treats that money as still owed.
