import json
from pathlib import Path

DATA_FILE = Path("data/tickets.json")

SEED_TEXT = """
id: 1001
title: Player sometimes falls through platform
type: bug
status: open
severity: high
assignee: none

id: 1002
title: Add accessibility option: subtitle size
type: feature
status: in_progress
severity: medium
assignee: alex

id: 1003
title: Pause menu doesn’t close with ESC
type: bug
status: done
severity: low
assignee: none
"""

def parse_seed(text: str) -> list[dict]:
    tickets = []

    for block in text.strip().split("\n\n"):
        ticket = {}
        for line in block.splitlines():
            key, value = line.split(":", 1)
            value = value.strip()
            ticket[key] = None if value == "none" else value

        ticket["id"] = int(ticket["id"])
        tickets.append(ticket)

    return tickets


def run_seed():
    if DATA_FILE.exists():
        return

    DATA_FILE.parent.mkdir(exist_ok=True)
    tickets = parse_seed(SEED_TEXT)

    with open(DATA_FILE, "w") as f:
        json.dump(tickets, f, indent=2)
