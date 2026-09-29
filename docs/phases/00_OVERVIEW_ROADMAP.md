# Alzheimer's Clinical Decision Support System (CDSS) - Master Roadmap

> **Program:** B.Tech Computer Science and Engineering  
> **Project Title:** Alzheimer's Clinical Decision Support System (CDSS)

---

## 1. System Overview & Architecture Flowchart

The Alzheimer's CDSS is an end-to-end medical AI platform that integrates clinical cognitive assessment scoring with deep learning-based MRI brain scan classification and Explainable AI (SHAP heatmaps) to assist clinicians in early detection and staging of Alzheimer's Disease.

```
+-----------------------------------------------------------------------------------+
|                                  SYSTEM FLOWCHART                                 |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [Start]                                                                          |
|     |                                                                             |
|     v                                                                             |
|  Doctor Login (Enter Credentials)                                                 |
|     |                                                                             |
|     v                                                                             |
|  Authentication (Verify with Database / JWT)                                      |
|     |                                                                             |
|     v                                                                             |
|  Doctor Dashboard (Manage Patients / View History)                                |
|     |                                                                             |
|     v                                                                             |
|  Add New Patient / Select Existing Patient                                        |
|     |                                                                             |
|     v                                                                             |
|  Enter / Update Patient Information (Personal + Medical History)                  |
|     |                                                                             |
|     v                                                                             |
|  Upload / View MRI Images (DICOM / JPG / PNG)                                     |
|     |                                                                             |
|     +----------------------------+                                                |
|     |                            |                                                |
|     v                            v (Deep Learning Subsystem)                      |
|  Enter Assessment Data      +-----------------------------------------+           |
|  (MMSE, ADL/IADL, etc.)     | MRI Image Preprocessing                 |           |
|     |                       | (Resize, Normalize, Augment)            |           |
|     |                       +-----------------------------------------+           |
|     |                                    |                                        |
|     |                                    v                                        |
|     |                       +-----------------------------------------+           |
|     |                       | DL Model Classification                 |           |
|     |                       | (CNN / ResNet / EfficientNet / VGG)     |           |
|     |                       +-----------------------------------------+           |
|     |                                    |                                        |
|     |                                    v                                        |
|     |                       +-----------------------------------------+           |
|     |                       | Staging & Confidence Score              |           |
|     |                       +-----------------------------------------+           |
|     |                                    |                                        |
|     +--------------------+---------------+                                        |
|                          |                                                        |
|                          v                                                        |
|  Submit Assessment + MRI Data                                                     |
|     |                                                                             |
|     v                                                                             |
|  Clinical Scoring (Calculate Assessment Scores)                                   |
|     |                                                                             |
|     v                                                                             |
|  Feature Engineering (Prepare Combined ML + DL Features)                          |
|     |                                                                             |
|     v                                                                             |
|  DL Prediction (Brain Image Staging & Classification)                             |
|     |                                                                             |
|     v                                                                             |
|  Explainable AI - SHAP (Feature Contributions & Visual Heatmap)                   |
|     |                                                                             |
|     v                                                                             |
|  Recommendation Engine (Care Plan / Next Steps)                                   |
|     |                                                                             |
|     v                                                                             |
|  Generate Clinical Report (PDF)                                                   |
|     |                                                                             |
|     v                                                                             |
|  Store Patient, Assessment, Prediction & Image Data (Database)                    |
|     |                                                                             |
|     v                                                                             |
|  View Patient History / Previous Reports                                          |
|     |                                                                             |
|     v                                                                             |
|   [End]                                                                           |
+-----------------------------------------------------------------------------------+
```

---

## 2. Project Implementation Phases

| Phase | Phase Name | Core Flowchart Nodes | Key Deliverables |
| :--- | :--- | :--- | :--- |
| **Phase 1** | **Authentication & Doctor Portal** | Doctor Login, Authentication, Doctor Dashboard | JWT Auth, Security, Doctor Dashboard, Patient Quick Search |
| **Phase 2** | **Patient Management & Clinical Assessment** | Add/Select Patient, Medical History, Enter Assessment Data | Patient CRUD, MMSE, ADL/IADL Clinical Scoring forms |
| **Phase 3** | **MRI Processing & Deep Learning Staging** | Upload MRI (DICOM/JPG/PNG), Preprocessing, DL Model | MRI Upload pipeline, Resize/Normalize, ResNet/EfficientNet classifier |
| **Phase 4** | **Feature Engineering & Explainable AI (SHAP)** | Submit Assessment + MRI, Clinical Scoring, Feature Engineering, SHAP Heatmap | Integrated Feature Vector, SHAP attribution, Brain Heatmap Visualizer |
| **Phase 5** | **Recommendation Engine, PDF Report & Audit** | Care Plan Engine, Generate PDF Report, DB Persistence, View History | Automated Care Recommendations, PDF Export, History Log, DB Storage |

---

## 3. Technology Stack

- **Frontend:** React, Vite, Modern Vanilla CSS Design System (Glassmorphism & Sleek Dark UI).
- **Backend:** Python FastAPI, Pydantic, SQLAlchemy.
- **Database:** SQLite (local development) / PostgreSQL (production dual-compatibility).
- **Deep Learning & ML:** PyTorch / TensorFlow, Torchvision, Scikit-learn, OpenCV, SHAP.
- **Reporting & Storage:** ReportLab (PDF generation), DICOM pydicom parser.
