import json
from pathlib import Path
from .models import Ticket
from .seed import run_seed

DATA_FILE = Path("data/tickets.json")

run_seed()

def load_tickets() -> list[Ticket]:
    with open(DATA_FILE) as f:
        data = json.load(f)
    return [Ticket(**t) for t in data]
