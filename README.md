# Clause Ledger

Clause Ledger compares an MSA, SOW, order form, or DPA with your company's own clause playbook. The result is a procurement checklist: walk-away terms, deviations, clauses nobody has approved yet, and sections that sit outside the playbook.

It is not a law firm, and the checklist is not legal advice. It will not tell you the contract is safe to sign. Counsel writes the positions. The plugin only applies positions counsel has marked approved.

The playbook stays in your repository. The plugin does not upload the contract or the playbook to a hosted service. A team hosts the paper by committing `playbook.json` next to the rest of its files and pointing the check at that path.

## What you get

- A starter playbook with ten common commercial topics. Every topic starts as `draft-needs-counsel`. The checker will map those clauses and will not treat the sample sentences as your policy.
- A validator that rejects an approved position with no preferred term, no walk-away, or no fallback sentence.
- A skill that quotes the contract, sorts walk-aways first, and sends uncovered sections to counsel.
- A second skill that records a named person's decision into the playbook, then runs the validator.

Sample sentences live under `illustration`. They show the shape of a position. The checker ignores them. Copy one into the live fields only after a named person adopts it.

## Set up

Copy `playbook/starter-playbook.json` into the private repository where your contracts already live. Fill `owner` and `counsel_contact`. Leave every position in draft until counsel gives you language.

Check the file:

```bash
python3 scripts/check_playbook.py playbook/starter-playbook.json
python3 scripts/check_playbook.py --self-check
```

In Claude Code, install this folder as a local plugin, then use `/check-contract` with the playbook path and the contract. Use `/record-position` when counsel actually accepts fallback language. The record skill refuses to mark a position approved without a person's name, a date, and the exact sentence.

## What the check will not do

- It will not invent a company position.
- It will not call a term enforceable, compliant, or safe.
- It will not look up "market standard" language to fill a blank.
- It will not send the document anywhere. There is no MCP server and no account.

Read `playbook/FORMAT.md` for the fields. The fictional Northwind files in `examples/` show a finished checklist shape. They are not a real policy.

## License

MIT. See `LICENSE`.
