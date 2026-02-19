import json

# Load CPIC rules
with open("data/cpic_rules.json", "r") as f:
    CPIC_RULES = json.load(f)

# Map star alleles to phenotype categories
PHENOTYPE_MAP = {
    'CYP2D6': {
        '*1/*1': 'NM',      # Normal Metabolizer
        '*1/*2': 'IM',      # Intermediate Metabolizer
        '*1/*4': 'IM',      # Intermediate Metabolizer
        '*4/*4': 'PM',      # Poor Metabolizer
        '*1/*10': 'IM',     # Intermediate Metabolizer
        '*10/*10': 'PM',    # Poor Metabolizer
    },
    'CYP2C9': {
        '*1/*1': 'NM',      # Normal Metabolizer
        '*1/*2': 'IM',      # Intermediate Metabolizer
        '*2/*2': 'PM',      # Poor Metabolizer
        '*1/*3': 'IM',      # Intermediate Metabolizer
        '*3/*3': 'PM',      # Poor Metabolizer
    },
    'VKORC1': {
        '-1639G/G': 'NM',   # Normal
        '-1639G/A': 'IM',   # Intermediate
        '-1639A/A': 'PM',   # Poor/Sensitive
    },
    'CYP2C19': {
        '*1/*1': 'NM',      # Normal Metabolizer
        '*1/*2': 'IM',      # Intermediate Metabolizer
        '*2/*2': 'PM',      # Poor Metabolizer
        '*1/*3': 'IM',      # Intermediate Metabolizer
        '*3/*3': 'PM',      # Poor Metabolizer
    }
}

def assess_risk(drug_name, gene, phenotype):
    # Convert drug name to uppercase for JSON lookup
    drug_upper = drug_name.upper()
    
    # Special handling for VKORC1 with warfarin
    if gene == 'VKORC1' and drug_upper == 'WARFARIN':
        # Use VKORC1-specific rules
        drug_key = 'WARFARIN_VKORC1'
    else:
        drug_key = drug_upper
    
    drug_data = CPIC_RULES.get(drug_key)
    
    if not drug_data:
        return "Unknown", "moderate", 0.5
    
    expected_gene = drug_data.get("gene")
    
    # If drug doesn't relate to this gene
    if gene != expected_gene:
        return "Unknown", "moderate", 0.5
    
    # Convert star allele to phenotype category
    phenotype_category = phenotype
    if gene in PHENOTYPE_MAP and phenotype in PHENOTYPE_MAP[gene]:
        phenotype_category = PHENOTYPE_MAP[gene][phenotype]
        print(f"🔄 Mapped {gene} {phenotype} -> {phenotype_category}")
    
    phenotype_rules = drug_data.get("phenotype_rules", {})
    rule = phenotype_rules.get(phenotype_category)
    
    if not rule:
        return "Unknown", "moderate", 0.5
    
    return rule["risk"], rule["severity"], 0.9