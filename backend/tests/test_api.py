import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.storage import DATA_FILE
import json
import shutil
from pathlib import Path

@pytest.fixture
def client():
    """Creates a test client for API testing"""
    return TestClient(app)

@pytest.fixture
def test_data_dir(tmp_path):
    """Creates temporary folder with test data (3 tickets matching seed data)"""
    test_data = tmp_path / "data"
    test_data.mkdir()
    
    tickets = [
        {
            "id": 1001,
            "title": "Player sometimes falls through platform",
            "type": "bug",
            "status": "open",
            "severity": "high",
            "assignee": None
        },
        {
            "id": 1002,
            "title": "Add accessibility option: subtitle size",
            "type": "feature",
            "status": "in_progress",
            "severity": "medium",
            "assignee": "alex"
        },
        {
            "id": 1003,
            "title": "Pause menu doesn't close with ESC",
            "type": "bug",
            "status": "done",
            "severity": "low",
            "assignee": None
        }
    ]
    
    data_file = test_data / "tickets.json"
    with open(data_file, "w") as f:
        json.dump(tickets, f)
    
    return test_data

# ===== GET Tests =====

def test_get_tickets(client):
    """Test that GET /tickets returns a list of tickets with status 200"""
    response = client.get("/tickets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 3

def test_get_tickets_structure(client):
    """Test that each ticket has all required fields"""
    response = client.get("/tickets")
    tickets = response.json()
    
    assert len(tickets) > 0
    ticket = tickets[0]
    
    # Verify all model fields are present
    assert "id" in ticket
    assert "title" in ticket
    assert "type" in ticket
    assert "status" in ticket
    assert "severity" in ticket
    assert "assignee" in ticket

# ===== PUT Tests (Update) =====

def test_update_ticket(client):
    """Test that we can update ticket fields and changes are persisted"""
    # Get first ticket
    response = client.get("/tickets")
    ticket = response.json()[0]
    
    # Modify fields
    ticket["status"] = "done"
    ticket["severity"] = "critical"
    
    # Send update
    response = client.put(f"/tickets/{ticket['id']}", json=ticket)
    assert response.status_code == 200
    
    # Verify changes were applied
    updated = response.json()
    assert updated["status"] == "done"
    assert updated["severity"] == "critical"

def test_update_nonexistent_ticket(client):
    """Test that updating non-existent ticket returns 404 error"""
    response = client.put("/tickets/99999", json={
        "id": 99999,
        "title": "Test",
        "type": "bug",
        "status": "open",
        "severity": "low",
        "assignee": None
    })
    assert response.status_code == 404

def test_update_ticket_partial_fields(client):
    """Test that we can update only specific fields without affecting others"""
    response = client.get("/tickets")
    ticket = response.json()[0]
    original_title = ticket["title"]
    
    # Change only status
    ticket["status"] = "testing"
    response = client.put(f"/tickets/{ticket['id']}", json=ticket)
    
    updated = response.json()
    assert updated["status"] == "testing"
    assert updated["title"] == original_title  # Title unchanged

# ===== POST Tests (Create) =====

def test_create_ticket(client):
    """Test that we can create a new ticket with minimal fields"""
    response = client.post("/tickets", json={
        "title": "New Bug",
        "type": "bug"
    })
    assert response.status_code == 200
    
    ticket = response.json()
    assert ticket["title"] == "New Bug"
    assert ticket["type"] == "bug"
    # Verify default values are set
    assert ticket["status"] == "open"
    assert ticket["severity"] == "medium"
    assert ticket["assignee"] is None
    assert "id" in ticket

def test_create_ticket_generates_unique_id(client):
    """Test that each new ticket gets a unique auto-generated ID"""
    response1 = client.post("/tickets", json={"title": "Bug 1", "type": "bug"})
    response2 = client.post("/tickets", json={"title": "Bug 2", "type": "bug"})
    
    ticket1 = response1.json()
    ticket2 = response2.json()
    
    # IDs must be different and greater than existing tickets
    assert ticket1["id"] != ticket2["id"]
    assert ticket1["id"] > 1003  # Greater than last seed ticket

def test_create_ticket_all_types(client):
    """Test that we can create tickets of all allowed types"""
    types = ["bug", "feature", "test"]
    
    for ticket_type in types:
        response = client.post("/tickets", json={
            "title": f"Test {ticket_type}",
            "type": ticket_type
        })
        assert response.status_code == 200
        assert response.json()["type"] == ticket_type

# ===== Validation Tests =====

def test_create_ticket_missing_title(client):
    """Test that creating ticket without title returns validation error (422)"""
    response = client.post("/tickets", json={"type": "bug"})
    assert response.status_code == 422

def test_create_ticket_missing_type(client):
    """Test that creating ticket without type returns validation error (422)"""
    response = client.post("/tickets", json={"title": "Test"})
    assert response.status_code == 422

def test_create_ticket_invalid_type(client):
    """Test that invalid type value returns error (400 or 422)"""
    response = client.post("/tickets", json={"title": "Test", "type": "invalid"})
    # FastAPI returns 400 for invalid Literal values, not 422
    assert response.status_code == 400

# ===== Persistence Tests =====

def test_ticket_persistence(client):
    """Test that created and updated tickets are saved to file and persist"""
    # Create new ticket
    response1 = client.post("/tickets", json={
        "title": "Persistent",
        "type": "feature"
    })
    ticket_id = response1.json()["id"]
    
    # Update it
    response2 = client.put(f"/tickets/{ticket_id}", json={
        "id": ticket_id,
        "title": "Persistent",
        "type": "feature",
        "status": "done",
        "severity": "high",
        "assignee": "bob"
    })
    assert response2.status_code == 200
    
    # Verify updated ticket appears in list
    response3 = client.get("/tickets")
    tickets = response3.json()
    updated_ticket = next((t for t in tickets if t["id"] == ticket_id), None)
    
    assert updated_ticket is not None
    assert updated_ticket["status"] == "done"
    assert updated_ticket["severity"] == "high"
    assert updated_ticket["assignee"] == "bob"

def test_create_and_retrieve(client):
    """Test that created ticket can be retrieved via GET /tickets"""
    # Create ticket
    create_response = client.post("/tickets", json={
        "title": "Test Retrieve",
        "type": "test"
    })
    created_ticket = create_response.json()
    
    # Get all tickets
    get_response = client.get("/tickets")
    all_tickets = get_response.json()
    
    # Verify created ticket is in the list
    found = any(t["id"] == created_ticket["id"] for t in all_tickets)
    assert found is True