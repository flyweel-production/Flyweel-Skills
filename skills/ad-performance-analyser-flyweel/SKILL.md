---
name: ad-performance-analyser-flyweel
description: Use when the user hands over ad data to look at. A CSV export, pasted numbers, a screenshot or an API reply. Google Ads, Meta Ads, LinkedIn Ads or TikTok Ads. Are the ads working? Why did cost per lead go up? Where should I spend more or less? How do I split budget between platforms? Is this campaign wearing out? What is my real return? Also writes a weekly or monthly report or a budget plan from that data. For live data in Flyweel, use flyweel-mcp-deep-ad-analysis.
license: Apache-2.0
metadata:
  author: Flyweel
  version: "2.0"
---

# Ad Performance Analyser

Ad spend is an investment. The job is to say whether it is coming back, where the next dollar should go, and how sure the data lets you be. Work from whatever the user gives you: an export, pasted rows, a screenshot, or a connected data source.

## Principles

1. **Start from what makes money.** Ask what the business counts as a result: a lead, a booked call, a signed deal, revenue. Measure against that. Clicks and platform conversions are steps on the way.
2. **Every number needs a comparison.** Prior period, the account's own average, or the target. The account's history beats any industry average.
3. **Small numbers lie.** Check sample size before reading a rate. See the rules below.
4. **Platform attribution is a claim.** Two platforms can both count the same customer. Say which attribution the numbers use.
5. **End with a decision.** Each analysis closes with specific actions and what each should change.

## First, check the data

Before any analysis, state what you were given:

- Period covered, and whether it is complete.
- Currency. If rows mix currencies, keep them apart. If the file names none, say so and report in the file's own units.
- What the "conversions" column counts. If the export does not say, state your assumption, carry on, and list it as a question for the user.
- Whether revenue or deal data is present. If it is missing, say cost per result is the deepest answer available. Missing revenue is not zero revenue.

## Depth

Match depth to the question.

- **Health check.** Spend against plan, cost per result against target, the trend over the last few weeks. Answer: on track or off, and the one lever that matters most.
- **Review.** Adds a channel breakdown, the top and bottom campaigns by cost per result, a four-week trend and three to five actions.
- **Deep dive.** Adds the funnel from impression to revenue, results by launch date or audience, and where the next block of budget should go.

## Sample size

- Fewer than 100 clicks: draw no conclusion from click rate.
- Fewer than 30 results: cost per result is a rough guide. Fewer than 10: do not rank on it. Pooling weeks to reach the count is fine for describing a campaign. It does not show the campaign would hold its cost at a higher budget.
- Fewer than 7 days: too short for a trend. Day-of-week swings dominate.
- Take the normal swing from the range of the prior weeks. A change smaller than twice that may be noise. Say so.
- The latest week may be incomplete, since results can arrive days after the click. Flag it.

## Common questions

**"Are my ads working?"** Get the target cost per result, or the value of a result, first. Compare the last 30 days with the 30 before and with the target. If cost is over target, find out which part moved using the tree below.

**"Cost per lead went up. Why?"** Scope it first, then find the cause.

1. Where: split by campaign. One campaign is a campaign problem. All of them is the market, the site or the tracking. Say how much of the total change the worst campaign explains.
2. When: find the first week it moved, and match it to a change in creative, audience, budget or page.
3. What: inside the affected campaigns, check these in order.
   - Cost per thousand impressions up: the auction got dearer (season, competitors, a smaller audience).
   - Click rate down: the ad is wearing out or reaching the wrong people.
   - Conversion rate down: the cause sits after the click, in the landing page, the offer or the tracking.
4. Narrow a conversion-rate drop. If other campaigns that share the same page and tracking held steady, a site-wide fault is unlikely; look at what is specific to this campaign. Then check lead counts in the CRM or inbox against the platform's count. If the leads are still arriving, tracking broke and cost has not really risen.

**"Where should I spend more or less?"** Average cost per result hides the answer. Look at the cost of each extra result: when spend rose, what did the extra results cost? A campaign with low spend and steady cost has room. A campaign whose cost climbs with each increase is at its limit. Recommend a specific shift and its expected effect.

**"How do I split budget between channels?"** Compare cost per result on the same result and in the same currency. If deal data exists, compare cost per won deal, since a channel with cheap leads can have dear customers. Shift in steps of about 20 percent and re-measure. Keep a small test budget on the weaker channel.

**"Is this campaign fatiguing?"** Signs: frequency above 3 on Meta, click rate falling two weeks running, cost per click rising while cost per thousand impressions holds, conversion rate slipping. Put a number on it: "click rate fell 25 percent in three weeks while impression cost held, so the creative is wearing out."

**"What is my real return?"** Give up to three figures, most trustworthy first:

1. Revenue landed from ad-sourced deals, divided by spend. Needs CRM or sales data.
2. Blended: all revenue in the period divided by all ad spend. Needs no attribution.
3. Platform-reported return. Shown last and labelled as the platform's own claim.

If deals take weeks to close, recent spend has not had time to return. Show those weeks as still open.

**"Plan next month's budget."** Use 90 days of weekly data. State the cost per result and its direction. Model flat, plus 20 percent and minus 20 percent, and say that cost per result usually rises as spend rises. Give a range.

## Red flags

Raise these whenever they appear, asked or not:

- A campaign taking more than 20 percent of spend with no results.
- A campaign whose cost per result is more than twice the account average, or up more than 30 percent week on week.
- Platform-reported results far above what the CRM or sales records show.
- One campaign taking more than 60 percent of spend.
- Frequency above 5 on Meta.
- Impression share under 50 percent on a Google brand campaign.

## How to answer

- Lead with the finding. Follow with the numbers.
- Use a table for any comparison.
- State the period and the currency every time.
- Show change as a signed percentage.
- Keep it short: one or two tables, then three or four numbered actions. End on the actions.
- If the data cannot answer the question, say what is missing.

## Reference files

Read these only when the task needs them:

- `references/report-templates.md`: weekly summary and monthly review layouts. Read when the user asks for a report.
- `references/benchmarks.md`: rough platform ranges for click rate and cost. Read only when the account has no history to compare against.
