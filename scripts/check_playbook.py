#!/usr/bin/env python3
"""Validate a Clause Ledger playbook. Stdlib only. No network."""

import json
import sys
from pathlib import Path

STATUSES = {"draft-needs-counsel", "approved"}
DOC_TYPES = {"msa", "sow", "order-form", "dpa"}
POSITION_KEYS = {
    "id",
    "topic",
    "applies_to",
    "status",
    "preferred",
    "acceptable",
    "walk_away",
    "ask_counsel_if",
    "fallback_language",
    "illustration",
}
DECISION_KEYS = {
    "id",
    "position_id",
    "decider",
    "date",
    "source",
    "fallback_language",
}


def validate(data):
    errors = []
    if not isinstance(data, dict):
        return ["playbook must be a JSON object"]
    if data.get("playbook_version") != 1:
        errors.append("playbook_version must be 1")
    if not isinstance(data.get("notice"), str) or "not legal advice" not in data["notice"].lower():
        errors.append("notice must say this is not legal advice")
    positions = data.get("positions")
    decisions = data.get("decisions")
    if not isinstance(positions, list) or not positions:
        errors.append("positions must be a non-empty list")
        positions = []
    if not isinstance(decisions, list):
        errors.append("decisions must be a list")
        decisions = []

    ids = set()
    for index, position in enumerate(positions):
        label = f"positions[{index}]"
        if not isinstance(position, dict):
            errors.append(f"{label} must be an object")
            continue
        missing = POSITION_KEYS - set(position)
        if missing:
            errors.append(f"{label} missing {', '.join(sorted(missing))}")
        pid = position.get("id")
        if not isinstance(pid, str) or not pid.replace("-", "").isalnum() or pid != pid.lower():
            errors.append(f"{label}.id must be lowercase kebab-case")
        elif pid in ids:
            errors.append(f"duplicate position id {pid}")
        else:
            ids.add(pid)
        if position.get("status") not in STATUSES:
            errors.append(f"{label}.status must be draft-needs-counsel or approved")
        applies = position.get("applies_to")
        if not isinstance(applies, list) or not applies or any(item not in DOC_TYPES for item in applies):
            errors.append(f"{label}.applies_to must list msa, sow, order-form, or dpa")
        if position.get("status") == "approved":
            for field in ("preferred", "walk_away", "fallback_language"):
                value = position.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{label}.{field} is required when status is approved")
        illustration = position.get("illustration")
        if illustration is not None and not isinstance(illustration, dict):
            errors.append(f"{label}.illustration must be an object")

    decision_ids = set()
    for index, decision in enumerate(decisions):
        label = f"decisions[{index}]"
        if not isinstance(decision, dict):
            errors.append(f"{label} must be an object")
            continue
        missing = DECISION_KEYS - set(decision)
        if missing:
            errors.append(f"{label} missing {', '.join(sorted(missing))}")
        did = decision.get("id")
        if not isinstance(did, str) or not did or did in decision_ids:
            errors.append(f"{label}.id must be a unique string")
        else:
            decision_ids.add(did)
        if decision.get("position_id") not in ids:
            errors.append(f"{label}.position_id does not match a position")
        decider = decision.get("decider")
        if not isinstance(decider, str) or len(decider.strip()) < 3 or decider.strip().lower() == "counsel":
            errors.append(f"{label}.decider must be a person's name")
        date = decision.get("date")
        if not isinstance(date, str) or len(date) != 10 or date[4] != "-" or date[7] != "-":
            errors.append(f"{label}.date must be YYYY-MM-DD")
        else:
            year, month, day = date.split("-")
            if not (year.isdigit() and month.isdigit() and day.isdigit()):
                errors.append(f"{label}.date must be YYYY-MM-DD")
        if not isinstance(decision.get("fallback_language"), str) or not decision["fallback_language"].strip():
            errors.append(f"{label}.fallback_language must be non-empty")
    return errors


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def self_check():
    root = Path(__file__).resolve().parents[1]
    failures = []
    for relative in ("playbook/starter-playbook.json", "examples/northwind-playbook.json"):
        errors = validate(load(root / relative))
        if errors:
            failures.append(f"{relative}: {errors}")

    broken = {
        "playbook_version": 1,
        "notice": "Not legal advice.",
        "positions": [
            {
                "id": "liability-cap",
                "topic": "Limitation of liability",
                "applies_to": ["msa"],
                "status": "approved",
                "preferred": "cap",
                "acceptable": "",
                "walk_away": "",
                "ask_counsel_if": "",
                "fallback_language": "",
                "illustration": {},
            }
        ],
        "decisions": [],
    }
    broken_errors = validate(broken)
    if not any("walk_away" in item for item in broken_errors):
        failures.append(f"approved position with empty walk_away was accepted: {broken_errors}")
    if not any("fallback_language" in item for item in broken_errors):
        failures.append("approved position with empty fallback_language was accepted")

    duplicate = json.loads(json.dumps(broken))
    duplicate["positions"].append(json.loads(json.dumps(duplicate["positions"][0])))
    duplicate["positions"][0]["walk_away"] = "no cap"
    duplicate["positions"][0]["fallback_language"] = "cap at fees"
    duplicate["positions"][1]["walk_away"] = "no cap"
    duplicate["positions"][1]["fallback_language"] = "cap at fees"
    if not any("duplicate" in item for item in validate(duplicate)):
        failures.append("duplicate ids were accepted")

    if failures:
        raise SystemExit("self-check failed:\n" + "\n".join(failures))
    print("self-check passed")


def main(argv):
    if len(argv) == 2 and argv[1] == "--self-check":
        self_check()
        return 0
    if len(argv) != 2:
        print("usage: check_playbook.py PLAYBOOK.json | --self-check", file=sys.stderr)
        return 2
    path = Path(argv[1])
    try:
        data = load(path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"{path}: {exc}", file=sys.stderr)
        return 1
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"{path}: {error}", file=sys.stderr)
        return 1
    print(f"{path}: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
