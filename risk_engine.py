import json

# Load CPIC rules
with open("data/cpic_rules.json", "r") as f:
    CPIC_RULES = json.load(f)


def assess_risk(drug_name, gene, phenotype):

    drug_data = CPIC_RULES.get(drug_name)

    if not drug_data:
        return "Unknown", "moderate", 0.5

    expected_gene = drug_data.get("gene")

    # If drug doesn't relate to this gene
    if gene != expected_gene:
        return "Unknown", "moderate", 0.5

    phenotype_rules = drug_data.get("phenotype_rules", {})
    rule = phenotype_rules.get(phenotype)

    if not rule:
        return "Unknown", "moderate", 0.5

    return rule["risk"], rule["severity"], 0.9