# Phase 5: Recommendation Engine, PDF Report & Patient Audit History

> **Flowchart Nodes Covered:**
> - `Recommendation Engine (Care Plan / Next Steps)`
> - `Generate Clinical Report (PDF)`
> - `Store Patient, Assessment, Prediction & Image Data (PostgreSQL)`
> - `View Patient History / Previous Reports`
> - `End`

---

## 1. Phase Objectives

1. Build an expert Clinical Recommendation Engine that maps predicted dementia stage, MMSE scores, and risk factors to evidence-based care plans, clinical trial recommendations, and lifestyle/pharmacological next steps.
2. Develop an automated PDF Clinical Report Generator that compiles patient demographics, cognitive scores, MRI predictions, SHAP heatmaps, and personalized care recommendations into a professional medical PDF.
3. Persist complete audit history to the database (PostgreSQL/SQLite).
4. Provide a Patient Records & History portal for doctors to review longitudinal progression over time.

---

## 2. Technical Specifications

### Recommendation Engine (`backend/app/recommendations.py`)
- Maps stage predictions & cognitive scores to actionable clinical guidelines:
  - **Non-Demented**: Routine 12-month follow-up, cognitive wellness activities.
  - **Very Mild Demented (MCI)**: 6-month cognitive tracking, MRI follow-up, Cholinesterase inhibitor evaluation, lifestyle interventions.
  - **Mild Demented**: Neurologist referral, caregiver support planning, medication regimen (Donepezil/Memantine), safety assessment.
  - **Moderate Demented**: Comprehensive specialized care, safety & environmental monitoring, clinical trial eligibility check.

### PDF Report Generator (`backend/app/reports.py`)
- Uses Python `reportlab` library to generate multi-page PDF documents containing:
  - Hospital / Clinic Header & Doctor Metadata.
  - Patient Demographics & Medical History Table.
  - Clinical Assessment Scores (MMSE, ADL, CDR).
  - MRI Staging & Confidence Badge.
  - Embedded SHAP Visual Heatmap image.
  - Formatted Care Plan & Next Steps.

### Backend Endpoints (`backend/app/routers/assessments.py`)
- `GET /api/reports/pdf/{assessment_id}`: Stream generated clinical PDF report for download/print.
- `GET /api/patients/{patient_id}/history`: Fetch longitudinal assessment history and past report links for a patient.

### Frontend Components (`frontend/src/pages/Records.jsx` & `Result.jsx`)
- **Download PDF Button**: Downloads clinical report directly from backend.
- **Patient History Portal (`Records.jsx`)**: Timeline viewer showing score progression (MMSE trends over time, MRI stage changes).

---

## 3. Database Persistence Schema

```sql
CREATE TABLE clinical_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id INTEGER UNIQUE NOT NULL,
    patient_id INTEGER NOT NULL,
    pdf_file_path VARCHAR(500) NOT NULL,
    care_plan_summary TEXT NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assessment_id) REFERENCES clinical_assessments(id),
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);
```

---

## 4. Acceptance & Verification Criteria

- [ ] Recommendation engine generates appropriate clinical care plans based on patient stage & MMSE scores.
- [ ] PDF report generates without formatting errors and includes embedded SHAP heatmap graphics.
- [ ] Generated PDF can be downloaded and opened in standard PDF viewers.
- [ ] Patient history portal accurately lists previous assessments and score trends over time.
