# Phase 1: Authentication & Doctor Dashboard Portal

> **Flowchart Nodes Covered:**
> - `Start`
> - `Doctor Login (Enter credentials)`
> - `Authentication (Verify with Database)`
> - `Doctor Dashboard (Manage Patients / View History)`

---

## 1. Phase Objectives

1. Implement secure, role-based doctor authentication using OAuth2 / JWT (JSON Web Tokens).
2. Protect API endpoints and frontend routes so only authenticated doctors can access patient records and assessments.
3. Build a high-performance Doctor Dashboard displaying patient stats, recent cognitive assessments, quick action triggers, and recent patient activity.

---

## 2. Technical Specifications

### Backend (FastAPI)
- **Security (`backend/app/security.py`)**:
  - `hash_password(password: str) -> str` (Bcrypt password hashing)
  - `verify_password(plain_password: str, hashed_password: str) -> bool`
  - `create_access_token(data: dict, expires_delta: Optional[timedelta]) -> str`
- **Router (`backend/app/routers/auth.py`)**:
  - `POST /api/auth/login`: Accepts credentials (email/password), verifies user in database, returns JWT access token & user profile.
  - `GET /api/auth/me`: Returns current logged-in doctor profile.
- **Dependencies (`backend/app/deps.py`)**:
  - `get_current_user`: Extracts JWT token from Authorization header and returns logged-in User instance.
- **Dashboard Metrics (`backend/app/routers/patients.py` / `dashboard.py`)**:
  - `GET /api/dashboard/stats`: Returns total patients count, high-risk cases count, pending assessments, and recent activity log.

### Frontend (React + Vite)
- **Login Component (`frontend/src/pages/Login.jsx`)**:
  - Sleek login form with email & password validation.
  - Interactive feedback, error alerts, loading state, and glassmorphism styling.
- **Auth Provider (`frontend/src/auth.jsx`)**:
  - React Context holding auth state, `login()`, `logout()`, and persistent token in `localStorage`.
- **Doctor Dashboard (`frontend/src/pages/Dashboard.jsx`)**:
  - Doctor Greeting & Quick Metrics Summary cards (Total Patients, High Risk Alerts, Recent Assessments).
  - Quick Search bar & Recent Patients List table.
  - Action cards: "Add New Patient", "Upload MRI Scan", "New Cognitive Assessment".

---

## 3. Database Schema

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'doctor',
    medical_license VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 4. Acceptance & Verification Criteria

- [ ] Doctor can successfully log in with valid credentials and receive a valid JWT token.
- [ ] Invalid credentials trigger a clear error notification on the UI.
- [ ] Protected routes redirect unauthenticated users back to `/login`.
- [ ] Doctor Dashboard displays real-time patient statistics and recent patient list from backend.
