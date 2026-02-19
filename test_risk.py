from vcf_parser import parse_vcf
from phenotype_engine import get_phenotype
from risk_engine import assess_risk

parsed = parse_vcf("sample.vcf")

supported_drugs = [
    "CODEINE",
    "WARFARIN",
    "CLOPIDOGREL",
    "SIMVASTATIN",
    "AZATHIOPRINE",
    "FLUOROURACIL"
]
for drug in supported_drugs:
    print("\n==============================")
    print("Drug:", drug)
    print("==============================")

    for gene, data in parsed.items():

        phenotype = get_phenotype(gene, data["star"])
        risk, severity, confidence = assess_risk(drug, gene, phenotype)

        if risk != "Unknown":
            print("Gene:", gene)
            print("Diplotype:", data["star"])
            print("Phenotype:", phenotype)
            print("Risk:", risk)
            print("Severity:", severity)
            print("Confidence:", confidence)
            print("----------------------------")