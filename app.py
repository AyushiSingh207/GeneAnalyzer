from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os
import json

from vcf_parser import parse_vcf
from phenotype_engine import get_phenotype
from risk_engine import assess_risk
from json_formatter import generate_output
from llm_explainer import generate_explanation

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.post("/analyze")
async def analyze_vcf(
    patient_id: str = Form(...),
    drug: str = Form(...),
    file: UploadFile = File(...)
):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    parsed = parse_vcf(file_path)

    for gene, data in parsed.items():

        phenotype = get_phenotype(gene, data["star"])
        risk, severity, confidence = assess_risk(drug, gene, phenotype)

        if risk != "Unknown":

            recommendation = "Follow CPIC dosing guidelines."

            explanation = generate_explanation(
                gene,
                data["star"],
                phenotype,
                drug,
                risk
            )

            result = generate_output(
                patient_id,
                drug,
                gene,
                data["star"],
                phenotype,
                data["rsid"],
                risk,
                severity,
                confidence,
                recommendation,
                explanation
            )

            return result

    return {
        "error": "No relevant pharmacogenomic variant found for this drug."
    }


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hackathon ke liye ok
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)