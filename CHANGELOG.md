# Changelog

## 2.0.0

First release from this repository.

**Six skills in one repo**, installable with one command.

- `flyweel`: start here. Checks setup, routes broad questions, gives a rundown.
- `flyweel-card-top-up`: forecasts what each ad platform will charge the cards, from daily ad spend. Answers top-up, how-long-will-it-last, scaling, pause, decline and pay-down questions.
- `flyweel-real-cash-payback`: what the cash the cards paid brought back, at the deepest result the data supports. Works with or without a CRM.
- `flyweel-where-to-spend-next`: one call per platform (add, hold, trim, cut, cannot see) with a weekly amount. Finds the last budget change on its own.
- `flyweel-mcp-deep-ad-analysis`: rewritten for the current Flyweel MCP server. TikTok, named result metrics, currency handling, destination check.
- `ad-performance-analyser-flyweel`: shortened. Benchmarks and report templates moved to `references/`.

**Written for the business owner.** Every skill body and description scores 70 or more on reading ease and avoids a list of jargon words. `scripts/readability.py` checks it in CI.

**Claude Code plugin manifest** added. Installing the plugin also connects the Flyweel MCP server.

Replaces the separate repos `flyweel-mcp-deep-ad-analysis`, `ad-performance-analyser-flyweel` and `flyweel-skill-cli`.
