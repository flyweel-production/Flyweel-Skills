# Paying it down

Part of flyweel-card-top-up. Terms such as biggest charge, pay-by date, room left and the paces are defined in SKILL.md.

For a monthly spend target. The target is in the account's currency.

If the target is no more than the limit minus the biggest charge, one payment a month covers it. Say so, give the amount and the day it must land, and skip the rest of this file.

- Daily pace = target divided by 30.
- Room you can use between payments = limit minus biggest charge. That much room stays free for the biggest charge to land.
- Days between payments = that room divided by daily pace, rounded down.
- Payment size = daily pace times the days between payments. When the days fall as weekdays with uneven gaps (every 4 days is close to Monday and Thursday), use the longer gap, so each payment covers it.
- Next payment must land by: day 1 plus (room left minus biggest charge, minus any charge owed now) divided by daily pace, rounded down. Then take off the landing time of the way of paying, as in the pay-by date.
- At the heavy pace (the heavy paces of all lines, added up), give the days between payments once more, in one sentence. The judgement below is on the normal pace only.
- Pay once up front instead: target minus limit, plus the biggest charge, minus any credit already on the account. Paid at the start of the month, it leaves room for the biggest charge all month, with no schedule to keep.
- Limit that would allow one payment a week: target divided by 4, plus the biggest charge.

Judge it:

- 7 days or more between payments: once a week works. Name the day.
- 2 to 6 days: it works but leaves little slack. Give it as weekdays.
- A way of paying that takes longer to land than the gap cannot keep up. Say which ways work and which do not.
- Under 2 days, or no way of paying is fast enough: this limit cannot carry the target on a schedule. Say so, give the pay-up-front amount, and make the case for a higher limit with facts only: spend each month against the limit, payments made, each full-card decline with its date and amount, and the limit that would allow one payment a week.

Also say where the user is today (step 5). If the current pace is already near the target, say that first: the schedule is needed now.

Lay the answer out like this, one or two short sentences each:

```
**The idea.** <the limit is the most you can owe at once; paying it down
  opens it again; this target needs N pay-downs a month>
**Where you are now.** <pace per day and per month, against the target>
**What to do.** Pay about <amount> every <N> days (<weekdays>).
  Next payment needs to land by <date>.
**How to pay.** <which ways land in time, which are too slow, and how long each took>
**The easy alternative.** Put <amount> in at the start of the month.
**Why every <N> days and not weekly.** <biggest charge, usable room, the
  limit a weekly payment would need>
**What went wrong before.** <each time the card was full, and how soon
  the next payment arrived>
```

For this question the working is the figures in the list above, plus the pace block for each line from the layout under "Show the working" in SKILL.md. There is no day-by-day forecast to show.
