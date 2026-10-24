# Changelog

## 2.3.0

Fixes found by running 2.2.0 on live data.

- `flyweel-mcp-deep-ad-analysis`, `flyweel-real-cash-payback` and `flyweel-where-to-spend-next` 2.3: a switched event counts as tracking starting, whatever the rate test gives. That is when another result on the same line, not zero before, falls under 10 percent of its earlier daily average within a day of this one starting.
- `flyweel-real-cash-payback` and `flyweel-where-to-spend-next` 2.3: the clock reads each platform's `lastSync` from `get_setup_status`, since `query_metrics` does not return it. `query_metrics` still decides whether a platform is connected.
- `flyweel-where-to-spend-next` 2.3: a line with no spend in the last 7 days is stopped. It is called Hold at zero, skips the change scan, and goes last when ranking what to cut. Days where both 7-day averages are zero never count as a change.
- `flyweel-real-cash-payback` 2.3: the figure without a lopsided week takes out that week's results and cash equal to its platform spend times the cash ratio, not the charges dated that week.

## 2.2.0

Fixes found by running 2.1.0 on live data.

- `flyweel-where-to-spend-next` 2.2: the result is picked for each platform. A platform that does not record the chosen result (Google has no signups) uses its own named result or `conversions`, and is never called zero results. The account's average cost per result is kept per result, and costs are ranked only among lines on the same result.
- `flyweel-where-to-spend-next` 2.2 and `flyweel-real-cash-payback` 2.2: a platform whose last sync failed, or with no selected accounts, no longer sets the clock.
- `flyweel-where-to-spend-next` 2.2: the change scan ends on day 36 of the 42, so the last 7-day window ends on the last full day.
- `flyweel-mcp-deep-ad-analysis` 2.2, `flyweel-real-cash-payback` 2.2 and `flyweel-where-to-spend-next` 2.2: the tracking-start test runs on each platform and currency on its own, and results per day divide by days with spend, not calendar days.

## 2.1.0

Fixes five places where a skill could give the wrong money figure.

- `flyweel-card-top-up` 2.2: the pay-up-front amount now adds money already owed on the account. Before, it only took off credit, so it came out too low.
- `flyweel-where-to-spend-next` 2.1: the before window can no longer run past the 42 days of data. When there is too little history before a change, both windows shrink to the same length, and after still ends on the last full day.
- `flyweel-where-to-spend-next` 2.1: adding back after a cut that hurt is now sized as before weekly cash minus after weekly cash, not 20 percent of the after level.
- `flyweel-real-cash-payback` 2.1: results are split by currency, so a platform billed in two currencies divides each currency's cash by its own results.
- `flyweel-mcp-deep-ad-analysis`, `flyweel-real-cash-payback` and `flyweel-where-to-spend-next`: a run of zero results before the first one counts as tracking starting only when the later rate would have given 5 or more results over those days. Otherwise the spend stays in and the answer says the early zeros may be a quiet spell.

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
