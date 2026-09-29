# Phase 2: Patient Management & Clinical Assessment Entry

> **Flowchart Nodes Covered:**
> - `Add New Patient / Select Existing Patient`
> - `Enter / Update Patient Information (Personal + Medical History)`
> - `Enter Assessment Data (MMSE, ADL/IADL, Clinical Data, etc.)`

---

## 1. Phase Objectives

1. Create complete Patient Lifecycle Management (registration, search, update details, view medical history).
2. Build interactive medical entry forms for clinical cognitive assessments:
   - **MMSE (Mini-Mental State Examination)** score entry (0-30 scale).
   - **ADL (Activities of Daily Living) & IADL** functional impairment scores.
   - **CDR (Clinical Dementia Rating)** and ApoE-e4 genetic risk factors.
   - Medical history (family history of dementia, hypertension, diabetes, smoking).

---

## 2. Technical Specifications

### Backend (FastAPI)
- **Router (`backend/app/routers/patients.py`)**:
  - `POST /api/patients`: Create new patient profile.
  - `GET /api/patients`: List all patients with search/filter parameters.
  - `GET /api/patients/{id}`: Fetch patient profile with medical history.
  - `PUT /api/patients/{id}`: Update patient details.
- **Router (`backend/app/routers/assessments.py`)**:
  - `POST /api/assessments`: Submit new clinical cognitive assessment.
  - `GET /api/assessments/patient/{patient_id}`: Fetch all past clinical assessments for a patient.
- **Scoring Engine (`backend/app/scoring.py`)**:
  - Validates MMSE, ADL, and CDR range values.
  - Computes composite clinical risk index.

### Frontend (React + Vite)
- **Patient Register Page (`frontend/src/pages/PatientRegister.jsx`)**:
  - Personal Information form (Name, Age, Gender, DOB, Emergency Contact).
  - Medical History checklist & risk factors.
- **Patients Management List (`frontend/src/pages/Patients.jsx`)**:
  - Filterable, searchable data table of all registered patients.
  - Status badges (Normal, Mild Cognitive Impairment, Alzheimer's Stage).
- **Assessment Entry Page (`frontend/src/pages/Assessment.jsx`)**:
  - Interactive questionnaire for MMSE, ADL/IADL, CDR, and functional scores.
  - Dynamic score preview before submission.

---

## 3. Database Schema

```sql
CREATE TABLE patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(20) NOT NULL,
    family_history_dementia BOOLEAN DEFAULT FALSE,
    hypertension BOOLEAN DEFAULT FALSE,
    diabetes BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE clinical_assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    mmse_score INTEGER CHECK(mmse_score BETWEEN 0 AND 30),
    adl_score INTEGER CHECK(adl_score BETWEEN 0 AND 100),
    cdr_score FLOAT CHECK(cdr_score IN (0, 0.5, 1, 2, 3)),
    apoe_e4_status VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);
```

---

## 4. Acceptance & Verification Criteria

- [ ] New patient registration validates required fields and saves to database.
- [ ] Patient search allows searching by name or ID.
- [ ] MMSE and ADL scores calculate correctly and enforce valid clinical bounds.
