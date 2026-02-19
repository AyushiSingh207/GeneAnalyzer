def generate_explanation(gene, diplotype, phenotype, drug, risk):
    
    explanation = f"""
Patient carries {gene} diplotype {diplotype}, classified as a {phenotype} metabolizer.

For the medication {drug}, this genetic phenotype is associated with a {risk} risk level.

Genetic variation in {gene} affects drug metabolism pathways,
which can alter drug activation or clearance.

Clinical decisions should follow CPIC genotype-guided therapy recommendations.
"""

    return explanation.strip()