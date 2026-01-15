from pydantic import BaseModel
from typing import Literal

Type = Literal["bug", "feature", "test"]
Status = Literal["open", "in_progress", "testing", "done"]
Severity = Literal["low", "medium", "high", "critical"]

class Ticket(BaseModel):
    id: int
    title: str
    type: Type
    status: Status
    severity: Severity
    assignee: str | None
