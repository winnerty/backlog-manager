import json
from pathlib import Path
from .models import Ticket
from .seed import run_seed

DATA_FILE = Path(__file__).parent.parent / "data" / "tickets.json"

def init_storage():
    run_seed()

def load_tickets() -> list[Ticket]:
    with open(DATA_FILE) as f:
        data = json.load(f)
    return [Ticket(**t) for t in data]

def save_tickets(tickets: list[Ticket]) -> None:
    with open(DATA_FILE, "w") as f:
        json.dump([t.model_dump() for t in tickets], f, indent=2)

def update_ticket(ticket_id: int, updated_data: dict) -> Ticket:
    tickets = load_tickets()
    for i, ticket in enumerate(tickets):
        if ticket.id == ticket_id:
            updated_ticket = ticket.model_copy(update=updated_data)
            tickets[i] = updated_ticket
            save_tickets(tickets)
            return updated_ticket
    raise ValueError(f"Ticket {ticket_id} not found")
