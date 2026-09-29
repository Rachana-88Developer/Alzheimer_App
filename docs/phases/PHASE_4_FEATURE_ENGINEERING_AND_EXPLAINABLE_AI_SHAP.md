# Phase 4: Feature Engineering & Explainable AI (SHAP)

> **Flowchart Nodes Covered:**
> - `Submit Assessment + MRI Data`
> - `Clinical Scoring (Calculate Assessment Scores)`
> - `Feature Engineering (Prepare ML + DL Features)`
> - `DL Prediction (Brain Image Classification + Stage)`
> - `Explainable AI - SHAP (Feature Contributions & Heatmap)`
> - `SHAP Heatmap (Highlights important regions on brain image)`

---

## 1. Phase Objectives

1. Combine tabular clinical features (MMSE, ADL, age, ApoE-e4, family history) with Deep Learning MRI feature embeddings into a multimodal feature vector.
2. Implement Explainable AI (XAI) using **SHAP (SHapley Additive exPlanations)**:
   - Calculate feature importance attributions for clinical risk factors.
   - Generate visual SHAP heatmaps overlaying brain MRI scans to highlight key regions of tissue atrophy (hippocampus, ventricles, cerebral cortex).
3. Provide transparent diagnostic reasoning to help clinicians verify AI predictions.

---

## 2. Technical Specifications

### Feature Engineering (`backend/app/ml/features.py`)
- **Combined Feature Construction**:
  ```python
  multimodal_vector = [
      age, gender_encoded, mmse_score, adl_score, cdr_score,
      apoe_e4_encoded, family_history_flag, hypertension_flag,
      *dl_image_embeddings  # extracted from penultimate layer of ResNet
  ]
  ```
- Standardize clinical variables with `StandardScaler`.

### Explainable AI Module (`backend/app/ml/explainability.py`)
- **SHAP Feature Attribution**:
  - Computes TreeExplainer / KernelExplainer SHAP values for tabular clinical features.
  - Outputs relative percentage contributions of MMSE, Age, ADL, and ApoE-e4 to the risk classification.
- **Gradient/SHAP Heatmap Generation**:
  - Generates Grad-CAM / Integrated Gradients / SHAP image attribution maps on the input MRI tensor.
  - Overlays a jet/plasma color heatmap onto the original grayscale MRI scan to visually highlight regions driving the stage classification.
  - Saves generated heatmap PNG to `backend/app/static/heatmaps/`.

---

## 3. API Response Specification (`POST /api/assessments/submit`)

```json
{
  "assessment_id": 102,
  "patient_id": 15,
  "clinical_score": {
    "mmse_risk": "High",
    "composite_index": 0.82
  },
  "mri_prediction": {
    "stage": "Mild Demented",
    "confidence": 91.4
  },
  "explainable_ai": {
    "feature_contributions": [
      {"feature": "MMSE Score (18/30)", "contribution": "+34%"},
      {"feature": "MRI Atrophy Score", "contribution": "+28%"},
      {"feature": "ADL Score (45/100)", "contribution": "+18%"},
      {"feature": "ApoE-e4 Positive", "contribution": "+12%"},
      {"feature": "Age (74)", "contribution": "+8%"}
    ],
    "heatmap_url": "/static/heatmaps/shap_patient_15_102.png"
  }
}
```

---

## 4. Frontend Visualization (`frontend/src/pages/Result.jsx`)

- **SHAP Heatmap Viewer**: Side-by-side comparison of original grayscale MRI vs. SHAP visual heatmap highlighting atrophied brain regions.
- **Feature Contribution Chart**: Horizontal bar chart showing exact feature impact on the overall risk prediction.

---

## 5. Acceptance & Verification Criteria

- [ ] Feature engineering creates a clean, unified multimodal vector.
- [ ] SHAP feature attributions calculate accurately and sum to 100%.
- [ ] SHAP heatmap overlay generates clearly over brain MRI images.
- [ ] UI renders the side-by-side MRI heatmap viewer and feature contribution chart.
