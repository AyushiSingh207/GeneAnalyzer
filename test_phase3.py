# import json
# from vcf_parser import parse_vcf
# from phenotype_engine import get_phenotype
# from risk_engine import assess_risk
# from json_formatter import generate_output

# patient_id = "PATIENT_001"
# drug = "CLOPIDOGREL"

# parsed = parse_vcf("sample.vcf")

# for gene, data in parsed.items():

#     phenotype = get_phenotype(gene, data["star"])
#     risk, severity, confidence = assess_risk(drug, gene, phenotype)

#     if risk != "Unknown":

#         recommendation = "Follow CPIC guideline."

#         final_output = generate_output(
#             patient_id,
#             drug,
#             gene,
#             data["star"],
#             phenotype,
#             data["rsid"],
#             risk,
#             severity,
#             confidence,
#             recommendation
#         )

#         print(json.dumps(final_output, indent=2))

# import json
# from vcf_parser import parse_vcf
# from phenotype_engine import get_phenotype
# from risk_engine import assess_risk
# from json_formatter import generate_output
# from llm_explainer import generate_explanation

# patient_id = "PATIENT_001"
# drug = "CLOPIDOGREL"

# parsed = parse_vcf("sample.vcf")

# for gene, data in parsed.items():

#     phenotype = get_phenotype(gene, data["star"])
#     risk, severity, confidence = assess_risk(drug, gene, phenotype)

#     if risk != "Unknown":

#         explanation = generate_explanation(
#             gene,
#             data["star"],
#             phenotype,
#             drug,
#             risk
#         )

#         final_output = generate_output(
#             patient_id,
#             drug,
#             gene,
#             data["star"],
#             phenotype,
#             data["rsid"],
#             risk,
#             severity,
#             confidence,
#             explanation
#         )

#         print(json.dumps(final_output, indent=2))

import json
from vcf_parser import parse_vcf
from phenotype_engine import get_phenotype
from risk_engine import assess_risk
from json_formatter import generate_output
from llm_explainer import generate_explanation

patient_id = "PATIENT_001"
drug = "CLOPIDOGREL"

parsed = parse_vcf("sample.vcf")

for gene, data in parsed.items():

    phenotype = get_phenotype(gene, data["star"])
    risk, severity, confidence = assess_risk(drug, gene, phenotype)

    if risk != "Unknown":

        recommendation = "Follow CPIC dosing guidelines."

        explanation = generate_explanation(
            gene,
            data["star"],
            phenotype,
            drug,
            risk
        )

        final_output = generate_output(
            patient_id,
            drug,
            gene,
            data["star"],
            phenotype,
            data["rsid"],
            risk,
            severity,
            confidence,
            recommendation,
            explanation
        )

        print(json.dumps(final_output, indent=2))