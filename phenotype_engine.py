PHENOTYPE_MAP = {
    "CYP2C19": {
        "*1/*1": "NM",
        "*1/*2": "IM",
        "*2/*2": "PM"
    },
    "CYP2D6": {
        "*1/*1": "NM",
        "*1/*4": "IM",
        "*4/*4": "PM"
    },
    "CYP2C9": {
        "*1/*1": "NM",
        "*1/*3": "IM",
        "*3/*3": "PM"
    },
    "SLCO1B1": {
        "*1/*1": "NM",
        "*1/*5": "IM",
        "*5/*5": "PM"
    },
    "TPMT": {
        "*1/*1": "NM",
        "*1/*3A": "IM",
        "*3A/*3A": "PM"
    },
    "DPYD": {
        "*1/*1": "NM",
        "*1/*2A": "IM",
        "*2A/*2A": "PM"
    }
}
def get_phenotype(gene, diplotype):
    gene_map = PHENOTYPE_MAP.get(gene)
    if not gene_map:
        return "Unknown"
    return gene_map.get(diplotype, "Unknown")