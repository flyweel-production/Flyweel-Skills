---
name: flyweel
description: Use when a Flyweel user's request is broad, vague or does not name one task. Help me with Flyweel. What can you do with my data? How is my ad money doing? Give me a morning or weekly rundown. Is everything set up right? Connect or pick an ad account. Sync my data. Which platform should I cut? Also use for any request that spans ad results and card funding, such as scaling spend and checking the cards can carry it. Start here when unsure which Flyweel skill fits.
license: Apache-2.0
compatibility: Requires the Flyweel MCP server.
metadata:
  author: Flyweel
  version: "1.0"
---

# Flyweel

The starting point for Flyweel questions. It checks what is connected, picks the skill that answers the question, and handles setup. The other skills do the analysis.

Two kinds of money show up in Flyweel. **What the platform reports**: spend, clicks and results as Google, Meta or TikTok count them. **What the cards paid**: the cash that left the business. The ad analysis skill uses the first. The card skills use the second. When a question is about money, that choice decides the skill.

## First: orient

Call `get_setup_status`. It shows which ad platforms are connected, which accounts are selected, whether data has synced, and whether a CRM is connected. Call `list_cards` if the question touches money, funding or cards. Three facts decide the route:

- **Ads data present?** Without it, only setup and the card funding skills apply.
- **Cards set up?** `cardsSetUp: false` means the card skills do not apply. Say so; do not report zero spend.
- **CRM connected?** If not, revenue questions are answered with the closest result the ad platforms track, and the answer says that.

More than one organisation: call `list_organizations` and ask which one. Never pick for the user.

## Route

Load the skill named, then follow it. Where two are listed, run them in that order.

| The user wants | Skill |
|---|---|
| How ads are doing, as the platforms report it; a weekly or monthly review; a platform or campaign comparison; where money is wasted; where ads send traffic | `flyweel-mcp-deep-ad-analysis` |
| What the cash the cards paid brought back; real cost per lead, signup, deal or customer; did a month pay off; how long money takes to come back | `flyweel-real-cash-payback` |
| Where to put more money, and how much; what to trim or cut | `flyweel-where-to-spend-next`, then `flyweel-card-top-up` to check the cards can carry it |
| A planned increase in spend: are we ok? | `flyweel-card-top-up` with the increase as the planned change |
| Will a card decline; how much to top up; how long the balance lasts; why a charge was declined; how often to pay the card down; the case for a higher limit | `flyweel-card-top-up` |
| Which platform to cut | `flyweel-where-to-spend-next` when cards are set up. Otherwise `flyweel-mcp-deep-ad-analysis` |
| A file, export or pasted numbers the user supplies | `ad-performance-analyser-flyweel` |

Tie-breakers:

- Data lives in Flyweel: use the Flyweel MCP skills. `ad-performance-analyser-flyweel` is for data the user hands over.
- The question is about money that left the bank: a card skill. About what the platforms report: the ad analysis skill.
- Still unclear after orienting: ask one short question that names the two candidate readings.

## Rundown

For "how is my ad money doing", a morning check or a weekly rundown, answer in three short parts and stop:

1. **Return**: `flyweel-real-cash-payback` over the last 30 days. Cash out per platform and what it bought.
2. **Funding**: `flyweel-card-top-up` over the next 7 days. Safe, close, or the amount to pay and by when.
3. **One thing to do**: the single action with the most money behind it.

Leave out a part whose data is missing, and say which and why.

## Setup requests

- Connect a platform: `connect_ad_platform`, give the user the link.
- Choose accounts: show `list_ad_accounts`, ask which, then `select_ad_accounts`.
- Refresh data: `trigger_sync`, then `get_sync_status`. Note that `query_metrics` can start a sync by itself.
- "Is everything set up right?": report from `get_setup_status` and `list_cards` as a short list of what works and what is missing, each gap with its fix. Check too for card charges from a platform whose spend Flyweel cannot see; that is an ad account not connected or not selected.
- "What can you do?": list the rows of the route table in plain words, marking any that the current setup cannot support yet.

## Changing things

Some tools change the account: `set_card_budget`, `freeze_card`, `unfreeze_card`, `issue_card`. Each is two-step. Call it without `confirmToken` to get a preview, show the preview, and apply only after the user says yes in their own words. Never confirm for them.
