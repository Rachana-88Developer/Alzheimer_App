"""Generator for built-in sample brain MRI scans matching Kaggle Augmented Alzheimer Dataset classes.

Allows doctors/testers to test deep learning inference with 1-click sample selection.
"""
import os
import numpy as np
from PIL import Image

SAMPLE_CLASSES = [
    ("non_demented", "Non Demented", 0.15),
    ("very_mild", "Very Mild Demented", 0.38),
    ("mild", "Mild Demented", 0.58),
    ("moderate", "Moderate Demented", 0.82)
]


def generate_sample_brain_mri(samples_dir: str):
    """Generates synthetic brain MRI slice images representing the 4 Alzheimer classes."""
    os.makedirs(samples_dir, exist_ok=True)
    
    h, w = 224, 224
    y, x = np.ogrid[:h, :w]
    cy, cx = 112, 112

    for key, label, atrophy_level in SAMPLE_CLASSES:
        filename = f"sample_mri_{key}.png"
        filepath = os.path.join(samples_dir, filename)
        
        # 1. Skull / Brain boundary (ellipse)
        brain_ellipse = (((x - cx) / 80.0)**2 + ((y - cy) / 95.0)**2) <= 1.0
        
        # 2. Cortex & White Matter background texture
        dist_from_center = np.sqrt((x - cx)**2 + (y - cy)**2)
        cortex_pattern = np.sin(dist_from_center / 6.0) * 0.12 + 0.55
        
        mri = np.where(brain_ellipse, cortex_pattern, 0.05)
        
        # 3. Ventricles (enlarge with higher atrophy level)
        ventricle_size = 12.0 + atrophy_level * 22.0
        v1 = (((x - (cx - 15)) / (ventricle_size * 0.6))**2 + ((y - cy) / ventricle_size)**2) <= 1.0
        v2 = (((x - (cx + 15)) / (ventricle_size * 0.6))**2 + ((y - cy) / ventricle_size)**2) <= 1.0
        
        mri[v1 | v2] = 0.10 # Dark cerebrospinal fluid in enlarged ventricles
        
        # 4. Temporal lobe / Hippocampus atrophy sulci widening
        sulci = (np.cos(x / 8.0) * np.sin(y / 8.0)) * (atrophy_level * 0.25)
        mri = np.clip(mri - np.abs(sulci) * brain_ellipse, 0.0, 1.0)
        
        # Convert to 8-bit grayscale image
        img_255 = (mri * 255.0).astype(np.uint8)
        pil_img = Image.fromarray(img_255, mode='L')
        pil_img.save(filepath)

    return True
