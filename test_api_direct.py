import requests
import json

# 1. First check if VCF parser works
from vcf_parser import parse_vcf

print("=== Testing VCF Parser ===")
vcf_data = parse_vcf("sample.vcf")
print("VCF Parser Output:")
print(json.dumps(vcf_data, indent=2))

if not vcf_data:
    print("❌ VCF parser returned no data!")
    exit()

# 2. Test risk engine directly
from risk_engine import assess_risk

print("\n=== Testing Risk Engine ===")
for gene, data in vcf_data.items():
    phenotype = data['star']
    risk, severity, confidence = assess_risk("warfarin", gene, phenotype)
    print(f"Gene: {gene}, Phenotype: {phenotype}")
    print(f"Risk: {risk}, Severity: {severity}, Confidence: {confidence}")
    print("-" * 30)