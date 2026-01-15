from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .storage import load_tickets
from .models import Ticket

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/tickets", response_model=list[Ticket])
def get_tickets():
    return load_tickets()
