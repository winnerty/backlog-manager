from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .storage import init_storage, load_tickets, update_ticket, create_ticket
from .models import Ticket

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CreateTicketRequest(BaseModel):
    title: str
    type: str

@app.on_event("startup")
def startup():
    init_storage()

@app.get("/tickets", response_model=list[Ticket])
def get_tickets():
    return load_tickets()

@app.put("/tickets/{ticket_id}", response_model=Ticket)
def put_ticket(ticket_id: int, ticket: Ticket):
    try:
        return update_ticket(ticket_id, ticket.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/tickets", response_model=Ticket)
def post_ticket(request: CreateTicketRequest):
    try:
        return create_ticket(request.title, request.type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
