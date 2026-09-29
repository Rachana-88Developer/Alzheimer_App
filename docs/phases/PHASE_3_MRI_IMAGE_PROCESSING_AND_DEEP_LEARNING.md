# Phase 3: MRI Image Processing & Deep Learning Subsystem

> **Flowchart Nodes Covered:**
> - `Upload / View MRI Images (Upload DICOM / JPG / PNG)`
> - `MRI Images (Preprocessed)`
> - `Image Preprocessing (Resize, Normalize, Augment)`
> - `DL Model (CNN / ResNet / EfficientNet / VGG / DenseNet)`
> - `Prediction (Alzheimer's Stage, Confidence Score)`

---

## 1. Phase Objectives

1. Support multi-format MRI brain image uploads: DICOM (`.dcm`), PNG, JPG/JPEG.
2. Build an automated medical image preprocessing pipeline:
   - DICOM pixel extraction & intensity normalization.
   - Skull stripping / spatial cropping and resizing (e.g., 224x224).
   - Data augmentation for training / inference normalization.
3. Train/deploy a Deep Learning Convolutional Neural Network (CNN / ResNet / EfficientNet) to classify brain MRI scans into 4 clinical stages:
   - **Non-Demented (Normal)**
   - **Very Mild Demented**
   - **Mild Demented**
   - **Moderate Demented**
4. Compute prediction probabilities and model confidence scores.

---

## 2. Technical Specifications

### Deep Learning Subsystem (`backend/app/ml/`)
- **Preprocessing Module (`backend/app/ml/preprocess.py`)**:
  - `load_mri_image(file_bytes, filename) -> np.ndarray` (handles DICOM using `pydicom` and PNG/JPG using OpenCV/PIL).
  - `preprocess_for_model(img_array) -> torch.Tensor` (resizes to 224x224, normalizes with ImageNet or brain MRI specific mean/std).
- **Model Architecture (`backend/app/ml/models.py`)**:
  - PyTorch/Torchvision ResNet-18/EfficientNet-B0 fine-tuned on Alzheimer's MRI dataset (e.g., OASIS / ADNI dataset).
- **Inference Service (`backend/app/ml/predict.py`)**:
  - `predict_mri_stage(image_bytes: bytes) -> dict`: Returns predicted stage, probability distribution across all 4 stages, and confidence percentage.

### Backend Endpoints (`backend/app/routers/assessments.py`)
- `POST /api/mri/upload`: Upload MRI scan file, save to storage, and return image metadata + preview URL.
- `POST /api/mri/analyze`: Run DL model inference on uploaded MRI image.

### Frontend Components
- **MRI Upload & Preview Widget (`frontend/src/pages/Assessment.jsx`)**:
  - Drag-and-drop file upload zone supporting DICOM/PNG/JPG.
  - Interactive MRI image viewer (slice navigation for DICOM or image preview).
  - Real-time staging prediction badge & confidence score gauge.

---

## 3. Storage & Metadata Schema

```sql
CREATE TABLE mri_scans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    format VARCHAR(20) NOT NULL, -- DICOM, PNG, JPG
    predicted_stage VARCHAR(50),
    confidence_score FLOAT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);
```

---

## 4. Acceptance & Verification Criteria

- [ ] Uploading DICOM, PNG, and JPG files returns valid preprocessed image arrays.
- [ ] Preprocessing pipeline resizes and normalizes images correctly without distortion.
- [ ] Deep Learning inference returns 4-class stage probabilities and confidence percentage.
- [ ] MRI preview renders cleanly on the frontend.
