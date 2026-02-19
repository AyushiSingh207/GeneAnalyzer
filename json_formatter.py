from datetime import datetime


# def generate_output(
#     patient_id,
#     drug,
#     gene,
#     diplotype,
#     phenotype,
#     rsid,
#     risk,
#     severity,
#     confidence,
#     recommendation_text
# ):

#     return {
#         "patient_id": patient_id,
#         "drug": drug,
#         "timestamp": datetime.utcnow().isoformat(),

#         "risk_assessment": {
#             "risk_label": risk,
#             "confidence_score": confidence,
#             "severity": severity
#         },

#         "pharmacogenomic_profile": {
#             "primary_gene": gene,
#             "diplotype": diplotype,
#             "phenotype": phenotype,
#             "detected_variants": [
#                 {
#                     "rsid": rsid
#                 }
#             ]
#         },

#         "clinical_recommendation": {
#             "recommendation": recommendation_text
#         },

#         "llm_generated_explanation": {
#     "summary": llm_summary
# },


#         "quality_metrics": {
#             "vcf_parsing_success": True
#         }
#     }

# def generate_output(
#     patient_id,
#     drug,
#     gene,
#     diplotype,
#     phenotype,
#     rsid,
#     risk,
#     severity,
#     confidence,
#     recommendation_text,
#     llm_summary
# ):
#     from datetime import datetime

#     return {
#         "patient_id": patient_id,
#         "drug": drug,
#         "timestamp": datetime.utcnow().isoformat(),

#         "risk_assessment": {
#             "risk_label": risk,
#             "confidence_score": confidence,
#             "severity": severity
#         },

#         "pharmacogenomic_profile": {
#             "primary_gene": gene,
#             "diplotype": diplotype,
#             "phenotype": phenotype,
#             "detected_variants": [
#                 {
#                     "rsid": rsid
#                 }
#             ]
#         },

#         "clinical_recommendation": {
#             "recommendation": recommendation_text
#         },

#         "llm_generated_explanation": {
#             "summary": llm_summary
#         },

#         "quality_metrics": {
#             "vcf_parsing_success": True
#         }
#     }

from datetime import datetime
def generate_output(
    patient_id,
    drug,
    gene,
    diplotype,
    phenotype,
    rsid,
    risk,
    severity,
    confidence,
    recommendation_text,
    llm_summary,
    genes_detected=1
):
    """
    Generates final structured JSON output exactly matching hackathon schema.
    """

    return {
        "patient_id": patient_id,
        "drug": drug,
        "timestamp": datetime.utcnow().isoformat(),

        "risk_assessment": {
            "risk_label": risk,
            "confidence_score": confidence,
            "severity": severity
        },

        "pharmacogenomic_profile": {
            "primary_gene": gene,
            "diplotype": diplotype,
            "phenotype": phenotype,
            "detected_variants": [
                {
                    "rsid": rsid
                }
            ]
        },

        "clinical_recommendation": {
            "recommendation": recommendation_text
        },

        "llm_generated_explanation": {
            "summary": llm_summary
        },

        "quality_metrics": {
            "vcf_parsing_success": True,
            "genes_detected": genes_detected
        }
    }