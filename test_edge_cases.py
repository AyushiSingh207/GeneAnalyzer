from vcf_parser import parse_vcf
from phenotype_engine import get_phenotype
from risk_engine import assess_risk

parsed = parse_vcf("sample.vcf")

print("\n=== Unknown Drug Test ===")
risk, severity, confidence = assess_risk("ASPIRIN", "CYP2C19", "PM")
print(risk, severity, confidence)

print("\n=== Unknown Phenotype Test ===")
risk, severity, confidence = assess_risk("CLOPIDOGREL", "CYP2C19", "URM")
print(risk, severity, confidence)

print("\n=== Full Flow Test ===")

for gene, data in parsed.items():
    phenotype = get_phenotype(gene, data["star"])
    risk, severity, confidence = assess_risk("CODEINE", gene, phenotype)

    print(gene, phenotype, "→", risk)