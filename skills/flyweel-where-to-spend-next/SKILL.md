---
name: flyweel-where-to-spend-next
description: Use when a Flyweel user asks where to put more ad money, how much more to spend on Meta, Google or TikTok, whether the last budget increase paid off, whether to scale a channel, which ad spend to cut or trim first, or wants a weekly call on each ad platform. Works from the real cash the Flyweel cards paid, not the spend the ad platform reports. Needs the Flyweel card tools and query_metrics.
license: Apache-2.0
compatibility: Requires the Flyweel MCP server with cards set up and at least one ad platform connected.
metadata:
  author: Flyweel
  version: "2.4"
---

# Where to Spend Next

Every budget change is a test. Spend went up, or down, on some day. What did the extra money buy, and what did each extra lead cost? This skill finds that day on its own, judges the change, and gives one call per spend line: **add**, **hold**, **trim**, **cut**, or **cannot see**, with an amount.

It works from the real cash the cards paid, not the spend the ad platform reports. Those two differ by tax, fees and timing. Cash is what left the business.

## How to talk to the user

- One line per spend line, in this order: the call, the amount, the reason. Then the detail.
- Short sentences. Everyday words. Say "cost per lead", "each extra lead", not finance terms.
- Call results what the business calls them: leads, signups, booked calls, quotes, deals.
- Numbers after the plain answer, in a small table, so they can be checked.
- End with what to do this week, with an amount and a date.

## What a spend line is

A spend line is one ad platform: "your Meta ads", "your Google ads". That is as far as the data links a card to the ads. A card charge shows the platform; it does not show the ad account. So money is never put on an ad account or a campaign. Campaign names appear only as counts: "6 signups from campaign X".

Edge case: when one platform bills the card in two currencies, it is two lines, named by currency: "your Meta ads billed in AUD". Keep each line's money in its own currency until the final table, then show it in the card's currency.

## Steps

1. **Setup.** `get_setup_status`, then `list_cards`. If `cardsSetUp` is false, say so and stop. That is not zero spend. If step 5 finds no settled or pending charge in the 42 days, the cards have not paid for any ads yet. Say so first. Then judge each line on platform spend with a cash ratio of 1, and label every amount "platform spend, not card cash". The card's currency is unknown until its first charge, so keep each line in its own currency and convert nothing. Lines with no currency stay **cannot see**, listed without a rank. If `query_metrics` later reports a platform as not connected while setup status says it is, report both; the line is cannot see either way.
2. **The result to count.** Pick it for each platform on its own. Use the result the user named. Otherwise look at `extendedMetricsAvailable` in any `query_metrics` reply and pick the named result that is not zero and matches what the business sells: `registration`, `leads`, `purchases` or similar. `conversions` is a broad count that mixes installs, clicks and leads; use it only when nothing named exists, with the `objective` dimension, and say what it counts. A platform with spend but none of that result in all 42 days may not record it. If another named result, or `conversions`, is not zero on that platform, use that one for it and say so. Never call a line zero results on a result its platform does not record. Say which result each platform used and why.
3. **The clock.** The earliest `lastSync` across the connected ad platforms, read from `get_setup_status` (`query_metrics` does not return it), as a UTC date, is the **last data day**. A platform counts as connected when the `query_metrics` sync status says so; if setup status disagrees, report both, go with `query_metrics` on whether it is connected, and leave that platform out of the clock. A platform whose last sync failed, or that has no selected accounts, sets no clock: report it and leave it out. The last data day may be short, so the **last full day** is the day before it. Every window ends on the last full day, and "the last 42 days" means the 42 days ending there.
4. **Daily ad spend and results, 42 days.** `query_metrics`, `dataSource: ads`, metrics `spend` and the result, dimensions `date`, `channel`, `currency`. One line per platform; split a platform only if it shows more than one currency.
5. **Real cash per line.** `list_card_transactions` for the last 42 days, all statuses, paged until `hasMore` is false. Count settled and pending charges; leave out declined and voided. Group charges by platform, and by `foreignCurrency` only where a platform has charges in more than one. For each line, the **cash ratio** = card charges whose `occurredAt` falls in the 42 days, settled or pending, divided by ad spend over the same 42 days, in the line's own currency.
   - Between 0.7 and 1: billing lag. The card has not yet been charged for the last few days and will be. Treat the ratio as exactly 1.
   - Above 1: tax or fees sit on top. Keep the ratio.
   - Under 0.7: something other than these cards paid part of it. See the trust checks.
   - The card paid but the platform shows no spend, or spend with no currency: **cannot see**. Its weekly cash is its 42-day card cash divided by 6, with any foreign-currency charges changed to the account's currency and added in.
   Real cash for any window = ad spend in that window times the cash ratio, then changed to the account's currency with the card's own rate (card amount divided by foreign amount on the latest settled charge).
6. **Find the last change.** A line with no spend in the last 7 days is **stopped**: skip the scan and step 7, and go to the call. For every other line, go back from the last full day. For each day, compare the average daily spend over the 7 days starting that day with the average over the 7 days before it. Scan from day 8 of the 42 to day 36, the last day whose 7 days starting there end on the last full day, so each day has 7 full days on both sides. The **change day** is the latest day where the after average is more than 25 percent above or below the before average, and the window from the change day to the last full day is at least 7 days long, both ends counted. It is the latest change that gets judged, even if the line launched earlier. Days where both averages are zero never qualify. If no day qualifies, the line is **steady**. If the before average is zero, or under 10 percent of the after average, the line is **new**: it started on the change day, and there is no before window to compare.
7. **Judge the change.** Take the window from the change day to the last full day (**after**), and the same number of days just before the change day (**before**). If the 42 days hold fewer days than that before the change day, shorten both: **before** is every day before the change day, and **after** is the same number of days, ending on the last full day.
   - Cost per result in each window = real cash divided by results.
   - **Cost of each extra result** = (cash after minus cash before) divided by (results after minus results before). Only when both went up.
   - Results per week in each window, so the user sees volume as well as cost.
   - A steady line is judged on its last 14 days against the 14 before.
   - A new line is judged on its after window alone, against the **account's average cost per result**. That is one fixed number per result for the whole answer: over the full 42 days, add up real cash (ad spend times cash ratio, in the account's currency) on every line counting that result with at least one in those 42 days, and divide by those results. If no line has any of a result in the 42 days, use the average for the result that most of the spend counts. No clipping for tracking.
   - Weekly cash for any window = its real cash divided by its days, times 7.
8. **Trust checks.** Say these out loud when they bite.
   - **Too thin**: fewer than 10 results in the after window. The call is hold, and the line says what count would be enough.
   - **Lopsided**: more than 40 percent of the after window's results fell in its last 2 days. Say so; the step may be newer than it looks.
   - **Result tracking started part-way**: zero results on every day before some date, with at least 7 days of real spend (above 10 percent of the after pace) before it. A quiet spell looks the same, so test it on this line alone: its results from that date on, divided by its days with spend from then on, times its zero days with spend before it. A switch also counts, whatever the test gives. That is when another result on the same line (often `conversions`) averaged at least 1 a day over the 14 days before this one started, and over the 7 days from the start averages under 10 percent of that. The tracked event was changed; say so. If that comes to 5 or more, or on a switch, tracking started then. Count cash and results only from that date, in both windows, and say so. Under 5 with no switch, keep every day in and say the early zeros may be a quiet spell, not missing tracking. Empty days after the first result do not count; only the run of zeros before it.
   - **Platform spend far above card cash** (cash ratio under 0.7): something other than these cards paid part of it. No cost figure; say what was seen.
9. **The call**, one per line:

| What happened | Call |
|---|---|
| Spend went up, results went up, each extra result cost no more than 1.25 times the before cost per result | **Add** |
| Spend went up, results went up, each extra result cost more than that | **Hold**: the last step cost too much. Say the figure |
| Spend went up, results flat or down | **Trim** back to the before level: the extra money bought nothing |
| Spend went down, cost per result got better | **Hold** at the new level; note what was saved |
| Spend went down, cost per result got worse | **Add** back to the before level: the cut hurt |
| Steady, cost per result within 25 percent of the 14 days before, 10 or more results | **Add**, as a first step |
| Steady, cost per result worse by more than 25 percent | **Hold**: the same money is buying less. Find out why before adding |
| Stopped: no spend in the last 7 days. Test this row first | **Hold** at zero: there is nothing left to cut. Say the last day it spent |
| Zero results in the after window. Test this row next | **Cut** if the last 14 days' real cash is more than twice the account's average cost per result. Otherwise **Hold**, and say the cash at which it becomes a cut |
| New line, 10 or more results, cost per result no more than 1.25 times the account's average | **Add** |
| New line, 10 or more results, cost per result above that | **Hold**: dearer than the rest. Say the figure |
| Platform shows no spend for cash the card paid | **Cannot see**: connect the ad account |
| Too thin, or after window under 7 days | **Hold**: too early to tell. Say when there will be enough |

Too thin outranks every row except stopped and zero results. Lopsided does not change the call. It adds a review date: the last full day plus 7.

10. **Amounts.**
   - Add: 20 percent on top of the after window's weekly cash, stated per week in the account's currency, and the extra results that should buy at the after window's cost per result.
   - Add back after a cut that hurt: the before window's weekly cash minus the after window's weekly cash, not 20 percent. The extra results are the before window's results per week minus the after window's.
   - Trim: back to the before window's weekly cash. Say the weekly cash freed.
   - Cut: the line's weekly cash over its last 14 days, all freed. The same 14 days the cut test used.
   - "Which should I cut first?": rank lines worst first. Zero-result lines at the top, then cannot-see lines by weekly cash, then lines with a cost, dearest first. Rank costs only among lines on the same result; list lines on another result after them, with the result named. Stopped lines go last, since they free nothing. Give the weekly cash each frees. For a cannot-see line say that cutting it is a guess, since its results are not visible, and that connecting the ad account is the better fix.
11. **Funding, one line.** Add the "add" amounts up and say: "flyweel-card-top-up will tell you whether the cards can carry that." Do not forecast the cards here.

## What to tell the user

```
<Line>: <Add | Hold | Trim | Cut | Cannot see>. <Amount per week>. <One-sentence reason>.
...

The week ahead: <total to add, total freed>. flyweel-card-top-up will tell you whether the cards can carry that.

Your Meta ads
  Change found: spend <went up | went down | steady> from <date>
                Before      After
  Days          N           N
  Real cash     X           X        (platform spend x cash ratio of R)
  Signups       N           N
  Cost each     X           X
  Each extra signup cost: X | not tested
  Results per week: N, then N
  Checks: <too thin | lopsided: N of M in the last 2 days | tracking started D | none>
  Where they came from: <counts by campaign, no money; "none" when there were no results>

Result counted: <name>, because <reason>.
Not counted: <lines with no spend and no cash in 42 days>.
Numbers as of <ads lastSync> for ad spend and <account.lastSyncedAt> for cards.
```

## Limits of this skill

- It moves money between platforms. It does not pick campaigns; counts by campaign are there to help the user pick.
- Daily ad spend is by calendar day in the platform's own clock. The last data day is left out of every window, since it may be short.
- A call made on 10 results is a first step, not a plan. Say so.
- Revenue, when a CRM is connected, is judged by flyweel-real-cash-payback. This skill stops at the result the platform counts.
- Card budgets and the account limit are judged by flyweel-card-top-up.
