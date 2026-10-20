---
name: flyweel-card-top-up
description: Use when a Flyweel user asks if their ad cards have enough money. Will a card decline? How much do I top up to keep ads running for a week or a month? How long will my balance last? Can I afford to spend 20 percent more? Why was a charge declined? How often should I pay the card down? Can I spend more a month than my limit? Do I need a higher limit? Is a card budget big enough? Also use for a money check before a weekend, a holiday or a push in spend. Needs the Flyweel card tools and query_metrics.
license: Apache-2.0
compatibility: Requires the Flyweel MCP server with cards set up.
metadata:
  author: Flyweel
  version: "2.1"
---

# Card Top-Up

When a card declines, the ads stop. The platform has to relearn, and that can cost days of leads. This skill works out what each ad platform will charge the cards next, and answers the money question the user asked.

Two people asking the same question on the same day must get the same number. So every step below has one rule, with no choice left open. Where a number rests on a guess, the guess is named in the answer.

## How to talk to the user

- Answer first, in one sentence, in the owner's words. No heading above it.
- Short sentences. Everyday words. If you must use a money or ad term, say what it means.
- Name cards by platform: "your Meta card". Add the last four digits only when two cards pay the same platform. Add a currency only when one card is billed in two: "your Meta card, billed in AUD".
- Give the numbers after the plain answer, in a small table, so they can be checked.
- End with what to do next, with an amount and a date.

## Read the question first

Take these from what the user said. Where they said nothing, use the default, say that you did, and carry on. Do not stop to ask.

| What you need | Default |
|---|---|
| How far ahead | 7 days. For "how long will it last", run until the room runs out, up to 60 days |
| A planned change in ad spend | None. "Scaling 20% over the next week" is a steady rise over 7 days. "From tomorrow" is a jump |
| Which platforms the change covers | Every platform the user named. If they named none, every platform that is still billing |
| Payments the user plans to make | None, even if they paid on a pattern before |
| A monthly spend target | Ask only if the question needs one. It is in the account's currency |

"This card" in a question means the whole card account. The limit is shared by every card on it, so the answer always covers the account.

## How the card account works

- The **limit** (`account.currentLimitCents`) is the most that can be owed at one time. It is not a monthly cap.
- The **balance** (`account.currentBalanceCents`) is charges minus payments. Above zero means money is owed. Below zero means money is sitting in credit. Charges still pending are already counted, so never take them off twice.
- **Room left = limit minus balance.** Credit is used first, then the limit. An account 500 in credit with a 1,000 limit has 1,500 of room.
- A charge is refused with `accountLimitExceeded` when it would take the balance past the limit. Each payment opens the room again once it has landed.
- A **card budget** is a second cap: `spendRestrictions.budget.amountCents` per period, with `balanceCents` being what that card has spent this period. A monthly budget starts fresh on the first of the month.
- The account's currency is the `currency` on its card transactions. `list_cards` does not state it.
- Ignore `account.spendRestrictions.budget`. It copies the limit and its balance stays at zero while cards spend, so it does not track anything.

## The clock

- **Last data day** = the date in `account.lastSyncedAt` (UTC). Spend on that day may be short.
- **Day 1** of every forecast is the day after the last data day. Say both dates in the answer.
- "The last 7 days" and "the last 30 days" end on the last data day.

## Build the forecast

1. **Cards.** `list_cards`. Note the limit, the balance, and each card's status and budget. If `cardsSetUp` is false, say cards are not set up and stop. That is not zero spend.
2. **Charges.** `list_card_transactions` for the last 90 days. Page with `offset` until `hasMore` is false. Amounts are in cents. Never add two currencies together.
3. **Billing lines.** Group charges into billing lines: one card, one platform. Edge case: if the same card and platform show charges in two currencies (`foreignCurrency`), that is two lines, since each bills on its own clock. Each line is one of two kinds:
   - **Set amount.** The same amount repeats, then steps up (2, 6, 9, 22, 34, 66, 130 is common on a new Meta account). The platform charges the card each time ad spend reaches that amount. The set amount is the most recent repeated amount. It may rise again; that makes each charge bigger, not the total.
   - **No set amount.** Anything else, such as round top-ups a person adds to the ad account by hand, or odd amounts. The user controls the timing, so the past cannot time them.
   A pending charge counts as a successful charge. A refused charge does not set the kind of a line; only charges that went through do.
   A line is **still billing** if it has a settled or pending charge in the last 14 days, or if a charge is owed on it. Step 6 decides that, so come back to this test after step 6. Any other line is listed under "Not counted" with the date and size of its last charge.
4. **Daily ad spend.** The card is charged after the money is spent, so daily ad spend shows what is coming before the card does. `query_metrics`, `dataSource: ads`, metric `spend`, dimensions `date`, `channel`, `currency`, for the last 45 days.
   - Match a billing line to ad spend by platform and by currency. The data links them no further than that, so never name an ad account as the one a card pays.
   - Check the match on each line over the last 30 days: ad spend on that platform and currency, against the line's charges. Count settled, pending, and any charge refused for a full card (`accountLimitExceeded`): the spend behind a refused charge is real and the platform will bill it again. Charges lag spend by a few days, so a short window misleads; 30 days smooths that out. Within 20 percent either way is a match: use daily ad spend for that line. If the platform shows no spend (zero rows, or spend with no currency), or the gap is wider, the card is paying for something Flyweel cannot see: use card history for that line and say so.
   - If charges over those 30 days are above ad spend by more than 5 percent, tax or fees are on top. Raise the forecast on that line by the same share. Say so.
   - Change currency with the line's own rate: the card amount divided by the foreign amount on its latest settled charge.
5. **Pace for each line.** Two figures per line.
   - From daily ad spend: the **normal pace** is the 7-day average. If the 3-day average is more than 25 percent above it, spend is climbing: use the 3-day average and say so. The **heavy pace** is the biggest single day in the last 7.
   - From card history: the normal pace is charges over the last 30 days divided by 30. The heavy pace is that times 1.5.
   - **Where you are now** = the normal paces of every line that is still billing, added up in the account's currency. Give it per day and times 30 for the month.
6. **Spent but not charged yet.** On every set-amount line whose platform and currency have daily ad spend, even if its pace came from card history: add up spend from the day after the last successful charge (settled or pending) to the last data day. A charge is **owed now** when that total is within 10 percent of the set amount or past it, or when the last charge on the line was refused and ads have spent since. The last data day may be short, which is why 10 percent of slack is allowed. A refused charge is how a bill gets missed: the ads kept running and the charge is still coming. Say that it is likely still on this card, since the ad account was not seen to move, and give the figures without that owed charge in one line.
7. **Apply the planned change** to the platforms it covers.
   - A steady rise of P percent over D days: on day d of the rise, the pace is today's pace times (1 + P × d ÷ D). After day D it holds at 1 + P.
   - A jump: today's pace times (1 + P) from the day it starts.
   - A pause: pace drops to zero that day, but money spent and not yet charged is still billed.
   - The normal case starts from the normal pace. The heavy case uses the heavy pace times (1 + P) from day 1, with no rise.
   - When spend is already climbing (step 5) and the user also says they are scaling, the user's rise goes on top of the 3-day pace. Say in the assumptions that if the climb already is the scale-up, the figure is lower, and give that lower figure: the same forecast with the rise removed from every line.
8. **Forecast day by day, normal and heavy.**
   - Set-amount line: start at the amount spent but not charged, add the daily pace, and each time the total reaches the set amount, one charge of the set amount lands that day. If a charge is owed now, in the normal case one charge of the set amount lands on day 1. What carries forward is the amount owed plus day 1's pace, minus the set amount, or zero if that is negative. The heavy case carries forward the same way after its day-1 charge. In the heavy case the whole owed amount lands on day 1, or the set amount if that is larger.
   - No-set-amount line: add the daily pace to the balance each day. These lines use room; they are never "the charge that was refused".
   - Add any payment the user said they will make, on the day it lands.
   - Keep the running balance. **The day the room runs out** is the first day the balance passes the limit. Also note the first day any card passes its own budget.
9. **Past payments and declines.** Group `payment` rows by their `description`, as written. For each, the days from `occurredAt` to `settledAt` are how long that way of paying takes to open up room. Name each way by its description and that time: "payments marked 'Flyweel Inc.' landed the same minute". List declines from the last 30 days by `declinedReason`:
   - `accountLimitExceeded`: the card was full. A payment or a higher limit fixes it.
   - `mccRestrictions`: this card is not allowed to pay that kind of merchant. A payment does not fix it.
   - `expirationMismatch` and the like: the card details were typed wrongly on the platform.

## Two figures used everywhere

- **Biggest charge** = the largest single settled or pending charge in the last 30 days on a line that is still billing, taken as the card amount in the account's currency. Declined charges do not count.
- **Pay-by date** = the day before the room runs out in the heavy case, minus the days the fastest way of paying the user has used takes to land. If that is day 1 or earlier, say "pay today".
- **The next payment after a given one** = 7 more days of charges at the heavy pace, plus the biggest charge, minus whatever room is left when the given payment runs out.

Round every amount the user is asked to pay up to the next 50. Show the exact figure in the working. "Today" in any formula means day 1.

## Answer the question asked

Open with the one line that answers it.

| The user asks | Open with | How to get it |
|---|---|---|
| Will anything decline? | Safe, close, or the date the room runs out | Both cases. "Safe" means the room lasts the whole period in the heavy case |
| How much do I top up to keep ads running for N days? | The heavy amount and the pay-by date, as the safe answer. Then the normal amount in the next sentence | Charges over the period minus room left, plus the biggest charge as a spare. Give both cases |
| How long will my balance last? | Both dates in one line: normal and heavy | The day the room runs out in each case |
| Can I afford to spend X more? | Yes as things stand, or the top-up it needs | Run the forecast with the change. Also give the most extra spend a day that fits: room left over at the end of the normal case, divided by the days |
| I can only pay X. How far does it go? | Both dates in one line, with and without the X | Add X to room left on the day it lands (day 1 for the fastest way of paying) and find the day the room runs out. Then give the next payment after that, by the rule above |
| What if I pause a platform? | The room it frees | Run it with that platform paused. The gap between the two is the answer |
| Why was this declined? | The reason in plain words, and the fix | For a full card, rebuild the balance at that moment: start from today's balance and go back, taking off each later charge and adding back each later payment. Show the balance, the charge that was refused, and when the next payment landed |
| Is this card's budget big enough? | Yes, or the budget it needs | That card's charges over the period against its budget room |
| Check before a weekend or holiday | Safe, or the amount to pay before it starts | Forecast up to the next day a payment from the user could land |
| How do I spend X a month on this limit? How often do I pay it down? | An amount and how often | Read `references/paying-it-down.md` |
| Do I need a higher limit? | Yes or no, and the number | Read `references/paying-it-down.md` |

## Paying it down

For a monthly spend target bigger than the limit, how often to pay the card down, or whether a higher limit is needed: read `references/paying-it-down.md` and follow it. Everything else in this file still applies.

## Show the working

After the plain answer, for every question answered from the day-by-day forecast:

```
Day 1 is <date>, the day after the numbers were last updated.
<N> days, <currency>                        Normal pace    Heavy pace
  Your <platform> card
  ...
  Total charges
  Room left now (<credit or owed> + limit)
  Payment you said you will make
  Short by, or left over
  Spare: the biggest charge
  Top up (exact, then rounded up)
  The day the room runs out
  Pay by

Your <platform> card
  How it bills: <set amount of X | no set amount>
  Pace: X a day normal, Y a day heavy (from <daily ad spend | card history>)
  Spent but not charged yet: X, against a set amount of Y
  Card budget: X left this month

What I assumed: <each default or reading of the question, one line each>
Not counted: <lines not still billing, with their last charge; cards that will decline for another reason>
Numbers as of <account.lastSyncedAt>.
```

A card that only has declines goes under "Not counted", with what is failing and what fixes it.

## Acting on it

- A card budget is the cap in the way: offer `set_card_budget`. Call it without `confirmToken`, show the preview, and apply it only after the user says yes. Never confirm for them.
- The account limit is the cap in the way: the fix is a payment or a higher limit. This tool can do neither. Give the amount and the date; the user pays in the Flyweel app.
- A merchant type is blocked: this tool cannot change what a card may pay. The charge will keep failing until that is changed in the Flyweel app, or the merchant moves to another card.
- A card is frozen while its platform is still charging: say so and offer `unfreeze_card`, with the same two steps.

## Limits of this skill

- It works per card and platform. The data does not say which ad account a card pays.
- Daily ad spend shows what has been spent, not what is planned. A planned change counts only if the user says it.
- A forecast past 14 days is a rough guide. Say so, and suggest a fresh check each week.
- Anything charged after `account.lastSyncedAt` is not counted.
- For whether the extra spend is worth it, see flyweel-where-to-spend-next.
