# Backend (FastAPI) - Alzheimer's CDSS

## Run with Docker
See root `README.md` and `docker-compose.yml`.

## Run locally (no Docker)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Point to a local Postgres (or install one). Example:
export DATABASE_URL="postgresql+psycopg2://cdss:cdss_password@localhost:5432/cdss_db"
export JWT_SECRET_KEY="dev-secret"
export SEED_DEFAULT_USERS=true
export AUTO_TRAIN_MODEL=true

uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

## Train the model manually

```bash
python -m app.ml.train
```
This generates a synthetic dataset, trains the configured model, and writes the artifact to `ml/artifacts/model.pkl`.
