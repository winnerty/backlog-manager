# Backlog Manager

A simple full-stack ticket management app built with **FastAPI** (backend) and **Vue.js** (frontend).

## Features

- 📋 View all tickets
- ➕ Create new tickets (auto-generated IDs)
- ✏️ Edit ticket status, severity, assignee
- 💾 Persistent JSON storage
- ✅ 13 comprehensive API tests

## Tech Stack

- **Backend:** FastAPI, Pydantic, Python 3.13+
- **Frontend:** Vue 3, Vite, Tailwind CSS
- **Styling:** Tailwind CSS, PostCSS, Autoprefixer
- **Storage:** JSON file
- **Testing:** pytest

## Quick Start

### Prerequisites
- Python 3.13+
- Node.js 18+

### 1. Clone & Setup Backend

```bash
cd backend
pip install fastapi uvicorn pydantic pytest
python run.py
```

Backend runs on `http://localhost:8000`

### 2. Setup Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173` with Tailwind CSS styling

### 3. Open in Browser

Go to `http://localhost:5173` and start managing tickets!

## Project Structure

```
backlog-manager/
├── backend/
│   ├── app/
│   │   ├── main.py       (FastAPI app, endpoints)
│   │   ├── models.py     (Pydantic models)
│   │   ├── storage.py    (JSON persistence)
│   │   └── seed.py       (Initial data)
│   ├── tests/
│   │   └── test_api.py   (13 API tests)
│   ├── data/
│   │   └── tickets.json  (Auto-generated)
│   └── run.py
│
├── frontend/
│   ├── src/
│   │   ├── App.vue       (Main component)
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tickets` | Get all tickets |
| POST | `/tickets` | Create new ticket |
| PUT | `/tickets/{id}` | Update ticket |

## Testing

Run backend tests:

```bash
cd backend
pytest tests/ -v
```

## Ticket Fields

| Field | Type | Values |
|-------|------|--------|
| id | int | Auto-generated |
| title | string | Required |
| type | Literal | `bug`, `feature`, `test` |
| status | Literal | `open`, `in_progress`, `testing`, `done` |
| severity | Literal | `low`, `medium`, `high`, `critical` |
| assignee | string \| null | Optional, defaults to `null` |
