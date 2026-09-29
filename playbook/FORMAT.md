# Playbook format

The playbook is one JSON file the company stores in its own repository. Clause Ledger reads that file. It does not upload the file.

`playbook_version` is `1`. `owner` is the team that maintains the file. `counsel_contact` is the person contracts go to. `notice` stays in the file so a reader sees that the checklist is not legal advice.

`positions` is the live paper. `decisions` is the log of who approved a position and when.

A position:

| Field | Meaning |
| --- | --- |
| `id` | Stable kebab-case id. Do not rename it after other files cite it. |
| `topic` | Short name a buyer will recognize. |
| `applies_to` | Any of `msa`, `sow`, `order-form`, `dpa`. |
| `status` | `draft-needs-counsel` or `approved`. Only `approved` is used to judge a deviation. |
| `preferred` | The term the company asks for first. |
| `acceptable` | A concession the company will still sign. |
| `walk_away` | A term the company does not sign without a new decision. |
| `ask_counsel_if` | A condition that still needs a lawyer even when the rest looks familiar. |
| `fallback_language` | The exact sentence the company is willing to send back. |
| `illustration` | An example of the shape. Never company policy. The checker ignores it. |

An approved position needs non-empty `preferred`, `walk_away`, and `fallback_language`. The validator rejects anything else.

A decision:

| Field | Meaning |
| --- | --- |
| `id` | Unique log id. |
| `position_id` | The position this decision changed. |
| `decider` | A person's name, not a department. |
| `date` | `YYYY-MM-DD`. |
| `source` | Where the decision was written down. |
| `fallback_language` | The exact language that was approved. |

Check a file with:

```bash
python3 scripts/check_playbook.py path/to/playbook.json
```

Start from `playbook/starter-playbook.json`. Copy it into the company repository, then replace the empty fields with language counsel has actually approved. Until you do that, the checker will map clauses and refuse to call anything a deviation.
