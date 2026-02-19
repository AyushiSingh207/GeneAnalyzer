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

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hackathon ke liye ok
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ YAHAN SE NAYA CODE ADD KARO ============

@app.get("/")
async def root():
    return {"message": "PharmaGuard API is running", "status": "active"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "server": "running"}

# ============ YAHAN TAK NAYA CODE ============

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


if __name__ == "__main__":
    import uvicorn
    print("🚀 PharmaGuard Server starting on http://localhost:8000")
    print("📝 API Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)