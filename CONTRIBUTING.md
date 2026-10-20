# Contributing

Issues and pull requests are welcome.

## Layout

- `skills/<name>/SKILL.md`: one folder per skill. The folder name must match `name` in the frontmatter. Format: [agentskills.io/specification](https://agentskills.io/specification).

## Check your change

```bash
python3 scripts/check_skills.py   # the six skills, frontmatter and length rules
npx skills add . --list       # all skills parse
python3 scripts/readability.py   # reading ease 70 or more, no jargon
```

## Changing a skill

- Write for the business owner, not the media buyer. Short sentences, everyday words. The readability script fails under a score of 70 and on the words it lists.

- Run the skill against real data before and after your change, and say in the pull request what the answer was each time.
- A skill states only what the data confirms. If the Flyweel MCP does not expose a link, the skill must not infer it.
- Skills that can change something (a card budget, a freeze) preview first and act only after the user says yes. Keep it that way.
- Never put real account data, card numbers or customer names in a skill or an example.
