---
name: flyweel-real-cash-payback
description: Use when a Flyweel user asks what their ad money brought back. What did the cash my cards paid buy? What is my real cost per lead, signup, deal or customer (real CAC)? Did last month or last quarter pay off? How long does ad spend take to come back as revenue? Which platform pays back fastest? How much ad cash is still out? Works from the real cash the Flyweel cards paid, not the spend the ad platform reports. Works with or without a CRM, and when CRM data is thin or messy. Needs the Flyweel card tools and query_metrics.
license: Apache-2.0
compatibility: Requires the Flyweel MCP server with cards set up.
metadata:
  author: Flyweel
  version: "2.3"
---

# Real Cash Payback

Money leaves on the card today. Leads, deals and revenue land later. This skill puts dollars and days on that gap, per ad platform, so the next dollar goes where money comes back.

It starts from the real cash the cards paid. That is the one number that is always right. Then it answers with the deepest result the data can honestly support. Missing or messy CRM data is never treated as zero, and never stops the answer. The skill steps down to a shallower result and says why.

## How to talk to the user

- Answer first, in one sentence, in the owner's words.
- Short sentences. Everyday words. Say "cost per lead" and "money back per dollar", not finance terms.
- Call results what the business calls them: leads, signups, booked calls, quotes, signed deals, revenue.
- Label every figure: **Paid** (card cash), **Counted** (a result that passed its checks), **Forecast** (a projection).
- Numbers after the plain answer, in a small table, so they can be checked.
- End with the two or three fixes that would let the next answer go deeper, each with its size.

## The deepest result we can trust

Deepest first. Use the deepest one that passes its checks, chosen for each platform on its own.

| Depth | Result | What it answers |
|---|---|---|
| 1 | Revenue landed (value of won deals) | Money back per dollar out |
| 2 | Signed deals (count) | Real cost per customer |
| 3 | Open deals or qualified leads | Real cost per real opportunity |
| 4 | CRM leads | Real cost per lead the business saw |
| 5 | Platform result (signups, leads, purchases as the platform counts them) | Real cost per platform result |

**Picking the depth-5 result.** Use the result the user named. Otherwise look at `extendedMetricsAvailable` in any `query_metrics` reply and take the named result that is not zero and matches what the business sells: `registration`, `leads`, `purchases` or similar. A named result that is not zero beats the campaign objective; say the objective beside it. If two fit, show both and ask. `conversions` is a broad count that mixes installs, clicks and leads; use it only when nothing named exists, with the `objective` dimension, and say what it counts.

## Finding the CRM data

- Send CRM queries in their own `query_metrics` call. A CRM error fails the whole call, ads queries included.
- First send one probe: `dataSource: crm`, metric `deals_won`, the window's dates. A reply with `setupRequired` means no CRM is connected, whatever the metric name. Use depth 5, say so once, and pass on the connection link the reply returns. Do not open it.
- If the probe returns data or an error that lists valid fields, take the CRM metric and dimension names from there or from the `query_metrics` description. Do not guess further names. If the names cannot be read, say so, stay on depth 5, and list it under "Not checked".

## Checks a result must pass

Defaults below. Change them when the user's business calls for it, and say so.

| Check | Passes when | If it fails |
|---|---|---|
| Present | The result returns data | Step down one depth. Not connected is not zero |
| Covered | The platform's card cash went to ad accounts Flyweel can see | See Coverage |
| Valued | At least 80 percent of signed deals carry an amount | Depth 1 fails; depth 2 stands |
| Attributed | At least 70 percent of deals carry a platform | Drop per-platform revenue. Give one blended figure: all card cash against all revenue |
| Enough | At least 10 results per platform in the window | Double the window once, never back past the first card charge. Then step down |
| Mature (depths 1 to 3) | The leads are older than the CRM's usual time to close | Show them as still open, never as a poor return |
| Not lopsided | No single deal or week is over 40 percent of the total | Show the figure with and without it. Without a week: take out its results, and cash equal to its platform spend times the line's cash ratio (line cash divided by line platform spend over the window). Never take out the charges dated that week; charges lag the spend. Without a deal: take out that deal only, and keep the cash |
| Adds up | CRM leads are between half and double the platform results; wins do not exceed deals created | Flag broken tracking or mismatched dates; do not rank on that depth |
| Fresh | Open deals are younger than twice the usual time to close | Leave stale deals out |
| Currency | CRM revenue is in the card's currency | Convert and label, or keep apart |

**Coverage.** Cash for an ad account Flyweel cannot see would make cost per result look worse than it is. Check what the data allows:
- Google charge descriptions carry the ad account number. Compare each with `list_ad_accounts`. Cash for a number that is not connected goes on its own line, "cash with no visible results", and stays out of every cost figure.
- A connected platform or account with card cash but zero results: report the cash with the words "no result recorded", give no cost.
- A platform that `query_metrics` says is not connected: its cash goes on its own line as "cash with no visible results", with the reconnect in the fix list.
- Other platforms' descriptions carry no account number, so coverage cannot be checked. Say so under "Not checked".

## Steps

1. **Setup.** `get_setup_status` and `list_ad_accounts`. Setup gaps are findings to report, not reasons to stop.
2. **The clock.** The earliest `lastSync` across the connected ad platforms, read from `get_setup_status` (`query_metrics` does not return it), as a UTC date, is the last data day. The **last full day** is the day before it. Every window ends there. A platform counts as connected when the `query_metrics` sync status says so; if setup status disagrees, report both, go with `query_metrics` on whether it is connected, and leave that platform out of the clock. A platform whose last sync failed, or that has no selected accounts, sets no clock: report it and leave it out. Weeks run Monday to Sunday.
3. **Window.** Default the last 90 days, in weeks. Use the user's window if given ("September" is 1 to 30 September). Either way, clip the start to the first card charge and say so: results from before the cards were paying have no cash to set against.
   **No card charge yet.** If the cards have no charge at all, or none in the window, there is no cash to measure. Say so in the first sentence. Skip the cost steps; one ads spend query by platform is enough for the fix list. Give the fix list: which platforms show ad spend that is not on these cards, and that the first answer is possible about two weeks after the first charge. Point to flyweel-mcp-deep-ad-analysis for what the platforms report in the meantime.
4. **Cash.** `list_card_transactions` over the window, paged until `hasMore` is false. Keep rows of `type: charge` with status settled or pending, by `occurredAt`. Group by platform, and by week for the checks. The answer shows one total per platform; weeks appear only when a check needs them. One line per platform; split a platform only if it bills in two currencies, and change foreign amounts to the card's currency at each charge's own rate.
5. **Platform results.** `query_metrics`, `dataSource: ads`, the result metric, dimensions `channel`, `currency` and `date`.
6. **CRM.** Separate call. Each depth's metric by platform and date. Run the checks. Pick each platform's depth.
7. **Cost.** Covered cash divided by results at the chosen depth. Where a platform is split by currency, divide each line's cash by that line's own results, the ones in the same currency. Results with no currency count in the platform's total only, never in a cost for one currency. For depth 1 also give money back per dollar out. Beside each platform's cash, note what the platform itself reports as spend for the same days; a gap of more than 20 percent is worth one sentence (billing lag, tax, or an account Flyweel cannot see). Platform spend with no currency cannot be compared: say "currency not recorded" and skip the gap check for it.
   - If the result only starts part-way through the window (zero every day, then not, with at least 7 days of platform spend before), tracking may have begun then. A quiet spell looks the same, so test it on each line on its own, one platform in one currency: its results from the first result on, divided by its days with spend from then on, times its zero days with spend before it. A switch also counts, whatever the test gives: another result on the same line, not zero before, falls under 10 percent of its earlier daily average within a day of this one starting. The tracked event was changed; say so. Under 5 with no switch, keep the earlier cash in and say the early zeros may be a quiet spell. At 5 or more, or on a switch, tracking began then. Count cash from that day, run the Enough and Not lopsided checks on that part only, and show the earlier cash on its own line as "before tracking".
   - A platform with cash and zero results, with no shallower depth left, gets its cash and the words "no result recorded". No cost figure.
8. **Days to come back.** The average date of the results, weighted by count or value, minus the average date of the card charges, weighted by amount. On depths 1 to 3 use mature leads only. A negative number is real and worth saying: platforms often charge the card after the result lands.
9. **Cash still out.** Depth 1 only: card cash minus revenue landed from the same weeks. On other depths say it cannot be measured yet.
10. **Forecast.** Depths 1 to 4 only. For weeks still open, project from this business's own past rate of turning results into the next depth, and show how many past weeks that rate rests on. Keep it on its own line. Never add it to Counted. At depth 5 there is nothing to project into; write "no forecast at this depth".

## "Did it pay off?"

With revenue (depth 1): yes when money back per dollar is above 1 on mature weeks, with the open weeks shown separately.

Without revenue: the honest answer is "it bought N results at X each", set against the same business's cost per result in the window before. If the window before has under 7 days of card cash or under 10 results, compare the second half of the window with the first half instead. If a half has under 10 results, that is thin too: say there is no earlier cost to compare, and give the cost each and the volume on their own. Cost each better than the comparison, with results per week within 20 percent or higher: say it paid off at the level the data can see. Worse: say so. Then say in one line what connecting the CRM would add: cost per signed deal and money back per dollar.

## What to tell the user

```
<One sentence: what the cash bought, at the deepest result the data supports.>

Your <platform> ads: depth <N>, <result>
  Cash out (Paid): X    <of which Y went to an account Flyweel cannot see>
  <Result> (Counted): N    Cost each: X
  Days from card charge to <result>: N
  Cash still out: X | not measurable at this depth
  Still open: <weeks>, Forecast N more (from N past weeks)
  Why this depth: <the check that stopped the deeper one, with the number>

Not checked: <checks the data could not support>
Fix list:
  1. <what to connect or clean, and what it unlocks, with its size>
  2. ...
Numbers as of <last data day> for ads and cards.
```

Rank platforms only against others on the same depth. Mixed depths go side by side, unranked, with one line on why they cannot be compared.

A fix list example: "38 of 90 signed deals have no amount. Fill them and money back per dollar becomes available." "681 went to a Google account that is not connected. Connect it and Google gets a cost per result."

## Limits of this skill

- A projection is never shown as a result. A shallower depth stated honestly is the useful answer.
- Money is never put on an ad account or a campaign. Counts by campaign are fine.
- Whether to add more money to a platform is judged by flyweel-where-to-spend-next. Whether the cards can carry it is judged by flyweel-card-top-up.
