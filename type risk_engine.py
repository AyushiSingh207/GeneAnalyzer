import json
from vcf_parser import parse_vcf
from risk_engine import assess_risk

print("=== Testing VCF Parser ===")
vcf_data = parse_vcf("sample.vcf")
print("VCF Parser Output:")
print(json.dumps(vcf_data, indent=2))

if not vcf_data:
    print("❌ VCF parser returned no data!")
    exit()

print("\n=== Testing Risk Engine with Warfarin ===")
for gene, data in vcf_data.items():
    phenotype = data['star']
    risk, severity, confidence = assess_risk("warfarin", gene, phenotype)
    print(f"Gene: {gene}, Phenotype: {phenotype}")
    print(f"Risk: {risk}, Severity: {severity}, Confidence: {confidence}")
    print("-" * 30)