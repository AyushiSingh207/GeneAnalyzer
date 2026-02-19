from vcf_parser import parse_vcf

# Parse karo sample.vcf
result = parse_vcf("sample.vcf")
print("Parsed VCF data:")
print(result)

# Check karo specific genes
genes_to_check = ["CYP2C9", "VKORC1", "CYP2C19", "CYP2D6"]
for gene in genes_to_check:
    if gene in result:
        print(f"\n{gene} found: {result[gene]}")
    else:
        print(f"\n{gene} not found in VCF")