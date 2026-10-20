---
name: flyweel-mcp-deep-ad-analysis
description: Use when a Flyweel user asks how their ads are doing. Uses what Google, Meta and TikTok report. Covers a weekly or monthly ad review, a platform or campaign comparison, where money is being wasted, a campaign deep dive, a check on where ads send traffic, and ad spend set against CRM deals. Also use for any question about query_metrics, cost per lead or cost per result on live Flyweel data. For the real cash the cards paid, use flyweel-real-cash-payback.
license: Apache-2.0
compatibility: Requires the Flyweel MCP server with at least one ad platform connected.
metadata:
  author: Flyweel
  version: "2.0"
---

# Flyweel MCP: Ad Analysis

This skill reads what the ad platforms report: spend, clicks, results, by campaign and by day. It is the fastest view of what is working. It is not the cash view: what the platform says it spent and what the card paid can differ by tax, fees and timing. For money that left the business, use flyweel-real-cash-payback.

The question behind every request is the same: is this working, and what should change? Answer that from the live data. Report numbers only as far as they support a decision.

## Tools

| Tool | Use |
|---|---|
| `get_setup_status` | Call first. Shows connected platforms, selected accounts, sync state. |
| `list_organizations` | When the user has more than one organisation. Ask which one; never pick for them. |
| `list_ad_accounts` | Account names, selection state, last sync time. |
| `query_metrics` | All analysis. Up to 5 queries per call. |
| `get_connection_status`, `get_sync_status` | Quick checks on a connection or a running sync. |
| `connect_ad_platform`, `select_ad_accounts`, `trigger_sync` | Change setup. Use only when the user asks for it. |

Card tools belong to the card skills listed at the end.

## Reading the data correctly

These five points are where analyses of this data go wrong.

1. **Take metric and dimension names from the tool, not from memory.** The `query_metrics` description lists them, and they change. Names such as `spend`, `clicks`, `channel`, `campaign` and `week` are typical. Check the list before using any other.
2. **`conversions` is not the business result.** It counts whatever each campaign's objective tracks, so it mixes leads, installs and clicks on a button. Every response returns `extendedMetricsAvailable`: named results such as `registration`, `leads` or `purchases`. Use the named result that matches what the business sells. If only `conversions` exists, add the `objective` dimension and say what it counts.
3. **Spend can mix currencies with no label.** Two accounts on one channel may bill in different currencies and the total adds them as if they were one. Add the `currency` dimension to any spend query, and never sum or compare cost figures across currencies. Counts are safe to add.
4. **CRM goes in its own call.** If no CRM is connected, one CRM query fails the whole batch, ads queries included. A `setupRequired` response means the CRM is not connected. That is a setup step. It is not zero deals. Say so once, pass on the connection link, and answer from ads data.
5. **A named result may start part-way through the window.** If it is zero and then non-zero, tracking began on that day. Measure cost per result from that day on, and say so.

Do not start a sync as a reflex. `query_metrics` may start one itself (`syncTriggered` in the response). Quote the last sync time, and offer `trigger_sync` only when the user wants fresher data.

## Workflow

1. **Orient.** `get_setup_status`. Note what is connected, selected and synced. A platform with a failed sync or no selected accounts is a finding to report; carry on with the rest.
2. **Scope.** Default to the last 30 days against the 30 before. Use the user's period, platform or account if given.
3. **Query in batches.** Group related ads queries into one call. Set `limit` to what will be shown.
4. **Compare.** A number alone says nothing. Give each one its prior period and the change.
5. **Answer.** Use the format below.

Example batch for an overview:

```json
{
  "queries": [
    {
      "dataSource": "ads",
      "metrics": ["spend", "clicks", "impressions", "registration"],
      "dimensions": ["channel", "currency"],
      "dateRange": { "preset": "last_30_days" }
    },
    {
      "dataSource": "ads",
      "metrics": ["spend", "registration"],
      "dimensions": ["week", "channel", "currency"],
      "dateRange": { "preset": "last_90_days" },
      "orderBy": { "column": "week", "direction": "asc" }
    },
    {
      "dataSource": "ads",
      "metrics": ["spend", "registration"],
      "dimensions": ["campaign", "currency"],
      "dateRange": { "preset": "last_30_days" },
      "filters": { "campaign_status": ["ENABLED"] },
      "orderBy": { "column": "spend", "direction": "desc" },
      "limit": 10
    }
  ]
}
```

Swap `registration` for the user's own result metric.

## Playbooks

**Weekly check.** Results and spend by `channel` for `last_week` and the week before. Top five active campaigns by spend. Report the change, the best and worst campaign, and one thing to do.

**Budget efficiency audit.** Spend and results by `campaign`, last 30 days, top 20 by spend. Weekly spend and results over 90 days. Flag campaigns that take real spend and return no results, and campaigns whose cost per result rose three weeks in a row.

**Channel comparison.** Spend, results and cost per result by `channel` and `currency`. Weekly trend over 90 days. Compare channels only on the same result metric and in the same currency. If they differ, show them side by side and say why they cannot be ranked.

**Campaign deep dive.** One campaign by `date` for 30 days, and by `week` for 90 for context. Look for a learning period after launch, a slow rise in cost per result, and day-of-week swings.

**Destination check.** Group by `destination_domain`. Any domain the user does not recognise is a sign the ad account has been taken over. Raise it at the top of the answer.

**Full funnel.** Ads results by `channel` in one call. Deals created, deals won and revenue by source channel in a second, CRM-only call, with names taken from the tool description. Then: ad spend per won deal, and revenue per dollar of spend. Deals take time to close, so a recent month with few wins is still open. It has not failed.

## Sample size

- Fewer than 100 clicks: draw no conclusion from click rate.
- Fewer than 30 results: cost per result is a rough guide. Fewer than 10: do not rank on it.
- Fewer than 7 days: too short for a trend.

The account's own history is the benchmark. Do not judge a campaign against industry averages.

## What to tell the user

```
<One sentence: the most important finding, with its number>

| | <period> | <prior period> | Change |
| <result metric> | | | |
| Spend (<currency>) | | | |
| Cost per <result> | | | |

By channel: <same three rows per channel, currencies kept apart>

What changed: <what moved and the likely reason, from the data>

Do next:
1. <specific action, and what it should change>
2. ...

Data notes: last sync <time>; result metric used and why; anything not connected; sample-size warnings.
```

## Setup gaps

- Nothing connected: offer `connect_ad_platform`.
- Connected, no accounts selected: show `list_ad_accounts`, ask which to select.
- Selected, never synced: offer `trigger_sync`, then `get_sync_status`.
- Sync failed: report the error; a reconnect usually fixes an expired token.
- No data in the period: widen the range and say when data starts.

## Related skills

Platform spend is what the platform says it charged. What the card paid is the cash figure. For questions about cash, cards and funding:

- `flyweel-real-cash-payback`: what the cash the cards paid brought back, and how long it took.
- `flyweel-where-to-spend-next`: add, hold, trim or cut, per platform, with an amount.
- `flyweel-card-top-up`: will a card decline, how much to top up, how often to pay it down.
