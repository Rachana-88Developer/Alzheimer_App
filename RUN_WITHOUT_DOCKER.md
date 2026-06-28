# Running locally in VS Code WITHOUT Docker

This project runs fine without Docker. It defaults to a local **SQLite**
database file (`backend/cdss.db`), so you do not need to install PostgreSQL.
You only need **Python 3.11+** and **Node.js 18+**.

Open two terminals in VS Code (Terminal > Split Terminal).

## Terminal 1 - Backend

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

First start creates the SQLite DB, seeds users, and trains the model.
Leave it running. API docs: http://localhost:8000/docs

## Terminal 2 - Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 and log in with `doctor` / `doctor123`.

## Notes
- No `.env` is required for local use; defaults work out of the box.
- To use PostgreSQL instead, set `DATABASE_URL` (see `.env.example`).
- To reset all data, stop the backend and delete `backend/cdss.db`.
- Recommended VS Code extensions: Python, Pylance, ESLint.
