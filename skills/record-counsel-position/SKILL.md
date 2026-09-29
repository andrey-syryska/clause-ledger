---
name: record-counsel-position
description: Records a counsel or procurement decision into the company clause playbook. Use when the user says counsel accepted language, rejected a term, or wants a clause topic saved for the next contract. Refuses to mark a position approved without a named decider, a date, and the exact fallback language.
---

# Record a counsel position

The playbook is the company's paper. You only write down a decision the user actually made. You do not invent a legal position, and you do not copy `illustration` into the live fields unless the user explicitly tells you to adopt that illustration and still supplies a decider and a date.

## Collect these before you edit

- Playbook path. Ask if you do not have it.
- Position `id`. If the topic is new, propose a kebab-case id and wait for a yes.
- `status` to write. Use `approved` only for a real decision. Otherwise leave `draft-needs-counsel`.
- The exact `fallback_language` the company will send back. The user's words, not a paraphrase you improve.
- `preferred`, `acceptable`, and `walk_away` in the user's words.
- `ask_counsel_if`, if they named a condition that still needs a lawyer.
- Decider name. A role alone is not enough. "Counsel" is not a name.
- Date in `YYYY-MM-DD`.
- Source the user cites, such as an email, a call, or a redline. If they have none, write `user-stated` and say so in the reply.

If any of decider, date, or fallback language is missing, stop. Ask for the missing item. Do not mark the position approved.

## Write

Edit the JSON in place.

1. Update the matching `positions` entry. Create it if the user confirmed a new id.
2. Set `status` to `approved` only when the required decision fields are present.
3. Append one object to `decisions`:

```json
{
  "id": "dec-YYYYMMDD-<position-id>",
  "position_id": "<id>",
  "decider": "<name>",
  "date": "YYYY-MM-DD",
  "source": "<source>",
  "fallback_language": "<exact text>"
}
```

4. Leave `illustration` untouched. It is not policy.
5. Run:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/check_playbook.py" PATH_TO_PLAYBOOK
```

If the script fails, undo your edit and show the error.

Then reply with the position id, the new status, the decider, the date, and the validator result. Remind the user that a teammate should commit the playbook in the company repository. Do not upload the playbook or any contract to a third-party host.
