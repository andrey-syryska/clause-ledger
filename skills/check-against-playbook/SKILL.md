---
name: check-against-playbook
description: Compares an MSA, SOW, order form, or DPA with the company's own clause playbook and returns a procurement checklist. Use when the user pastes a contract, points at a contract file, or asks which terms deviate from company paper, what to walk away from, or what to send to counsel. Does not give legal advice and does not invent positions that are not approved in the playbook.
---

# Check a contract against the playbook

This is an operator checklist for procurement. It is not legal advice, not a sign-off, and not a law firm. Counsel decides what the company will sign.

## What you need

1. A playbook JSON file. If the user does not name one, ask for the path. Do not invent a company position to fill the gap.
2. The contract text, pasted or read from a file the user names. If it is missing, ask for it.
3. The document type when the user knows it: `msa`, `sow`, `order-form`, or `dpa`. If they do not say, infer it only when the title is explicit, and say what you inferred.

Read the playbook from disk. Do not search the web for "market standard" terms. Do not send the contract or the playbook to a URL, an MCP server, or any other service.

Run the validator before you trust the file:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/check_playbook.py" PATH_TO_PLAYBOOK
```

If validation fails, stop and show the script's errors. Do not check the contract against a broken playbook.

## How to read the playbook

Each position has `status` of `draft-needs-counsel` or `approved`.

- Use `preferred`, `acceptable`, `walk_away`, `ask_counsel_if`, and `fallback_language` only when `status` is `approved` and the validator has passed.
- Ignore `illustration` when deciding a deviation. Illustration text shows the shape of a position. It is not company policy.
- Skip a position whose `applies_to` does not include the document type.
- A draft position still gets a row when the contract has language on that topic. The row says counsel has not approved a position.

## How to read the contract

For each in-scope playbook topic, find the contract language that speaks to it. Quote the shortest span that carries the obligation, with a section number if one exists. If you cannot find it, say `not found`. Do not paraphrase the quote and then treat the paraphrase as the quote.

Also list contract sections that no playbook topic covers. Those go to counsel. Do not grade them.

## Output

Write the checklist in the same language the user used. Use this order and these headings.

```markdown
# Playbook check

Not legal advice. Not a sign-off. Counsel decides whether to sign.

Playbook: <path>
Document type: <type>
Validator: passed

## Walk away
Approved positions only. Include a row when the quoted term matches `walk_away`, or when `ask_counsel_if` is true.

## Deviations
Approved positions only. The quote misses `preferred` and is not inside `acceptable`.

## Within the playbook
Approved positions whose quote matches `preferred` or `acceptable`. One line each. Quote still required.

## No company position yet
Draft topics that appear in the contract, or draft topics that are missing when the topic usually has to be present for this document type. Say that illustration text was not applied.

## Outside the playbook
Contract sections with no matching topic. Route each one to counsel. Do not call them acceptable.

## Missing approvals
Names of playbook positions that are still `draft-needs-counsel`, so the user can see what counsel has not written yet.
```

Every walk-away and deviation row uses this shape:

```markdown
### <topic> (`<id>`)
Quote: "<exact span>"
Playbook says: <preferred, or acceptable if that is the match>
Fallback from the playbook: <fallback_language, or "none on file">
Send to counsel: yes or no, and why, using only `ask_counsel_if` and `walk_away`
```

Rules for the words you choose:

- Never write "safe to sign", "compliant", "enforceable", "you should sign", or "this is legal".
- Never supply fallback language that is not copied from an approved `fallback_language`.
- If the user asks whether they can sign, answer that this check only compares the contract with the playbook.
- If the playbook has zero approved positions, still return the clause map under "No company position yet" and "Outside the playbook". Say that deviation checking starts after counsel approves at least one position.

## Example

A fictional vendor excerpt and an approved sample playbook live in `examples/`. Read `examples/expected-checklist.md` for the shape of a finished check. Do not treat Northwind Outfitters as a real company or as the user's policy.
