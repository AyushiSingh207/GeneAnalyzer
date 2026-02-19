from vcf_parser import parse_vcf
from phenotype_engine import get_phenotype
parsed = parse_vcf("sample.vcf")
for gene, data in parsed.items():
    phenotype = get_phenotype(gene, data["star"])
    print(gene, data["star"], "→", phenotype)