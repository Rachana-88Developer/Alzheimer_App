import os
import io
from datetime import datetime, timezone
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def generate_report(patient, assessment) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, title="Alzheimer's CDSS Report")
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("t", parent=styles["Title"], fontSize=18)
    elems = []

    elems.append(Paragraph("Alzheimer's Clinical Decision Support Report", title_style))
    elems.append(Spacer(1, 0.3 * cm))
    elems.append(Paragraph(
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        styles["Normal"]))
    elems.append(Spacer(1, 0.5 * cm))

    patient_data = [
        ["Patient", patient.full_name],
        ["Age", str(patient.age)],
        ["Gender", patient.gender],
        ["Education (years)", str(patient.education_years)],
    ]
    t = Table(patient_data, colWidths=[5 * cm, 10 * cm])
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
    ]))
    elems.append(t)
    elems.append(Spacer(1, 0.5 * cm))

    elems.append(Paragraph("Assessment Scores", styles["Heading2"]))
    score_data = [
        ["MMSE", assessment.mmse_score],
        ["MoCA", assessment.moca_score],
        ["ADL/IADL", assessment.adl_score],
        ["Behaviour", assessment.behaviour_score],
        ["Language", assessment.language_score],
        ["Attention", assessment.attention_score],
        ["Executive", assessment.executive_score],
        ["MRI atrophy", assessment.mri_atrophy],
        ["Voice biomarker", assessment.voice_biomarker],
    ]
    st = Table([["Metric", "Value"]] + [[k, str(v)] for k, v in score_data],
               colWidths=[7 * cm, 8 * cm])
    st.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
    ]))
    elems.append(st)
    elems.append(Spacer(1, 0.5 * cm))

    elems.append(Paragraph(
        f"Predicted Stage: <b>{assessment.predicted_stage.upper()}</b>",
        styles["Heading2"]))
    elems.append(Spacer(1, 0.2 * cm))

    probs = assessment.stage_probabilities or {}
    if probs:
        prob_rows = [["Stage", "Probability"]] + [
            [k, f"{v * 100:.1f}%"] for k, v in probs.items()
        ]
        pt = Table(prob_rows, colWidths=[7 * cm, 8 * cm])
        pt.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ]))
        elems.append(pt)
        elems.append(Spacer(1, 0.5 * cm))

    # Embed SHAP brain heatmap if available
    if getattr(assessment, "mri_heatmap_url", None):
        rel_path = assessment.mri_heatmap_url.lstrip("/")
        abs_heatmap_path = os.path.join(os.path.dirname(__file__), rel_path)
        if os.path.exists(abs_heatmap_path):
            elems.append(Paragraph("Brain MRI Scan & SHAP Visual Heatmap", styles["Heading2"]))
            elems.append(Spacer(1, 0.2 * cm))
            elems.append(RLImage(abs_heatmap_path, width=7.5*cm, height=7.5*cm))
            elems.append(Spacer(1, 0.4 * cm))

    # Embed Explainable AI SHAP feature attributions if available
    xai = getattr(assessment, "explainable_ai", None) or {}
    contributions = xai.get("feature_contributions", [])
    if contributions:
        elems.append(Paragraph("Explainable AI - SHAP Feature Attributions", styles["Heading2"]))
        elems.append(Spacer(1, 0.2 * cm))
        xai_rows = [["Clinical Feature / Biomarker", "Value", "Attribution", "Impact"]]
        for item in contributions[:6]:
            xai_rows.append([
                item.get("label", item.get("feature", "")),
                str(item.get("value", "")),
                str(item.get("contribution", "")),
                str(item.get("impact", "")),
            ])
        xt = Table(xai_rows, colWidths=[5 * cm, 2.5 * cm, 2.5 * cm, 5 * cm])
        xt.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
        ]))
        elems.append(xt)
        elems.append(Spacer(1, 0.4 * cm))

    reasoning = xai.get("clinical_reasoning")
    if reasoning:
        elems.append(Paragraph("Clinical Diagnostic Reasoning", styles["Heading2"]))
        elems.append(Spacer(1, 0.2 * cm))
        elems.append(Paragraph(reasoning, styles["Normal"]))
        elems.append(Spacer(1, 0.4 * cm))

    elems.append(Paragraph("Recommendations & Care Plan", styles["Heading2"]))
    for r in (assessment.recommendations or []):
        elems.append(Paragraph(f"- {r}", styles["Normal"]))
    elems.append(Spacer(1, 0.5 * cm))

    elems.append(Paragraph(
        "<i>Educational/research use only. Not a medical device.</i>",
        styles["Italic"]))

    doc.build(elems)
    return buf.getvalue()

