import re

from medquery.guardrails.result import GuardrailResult

MEDICAL_TERMS = {
    "disease",
    "symptom",
    "symptoms",
    "diagnosis",
    "treatment",
    "medicine",
    "medication",
    "drug",
    "doctor",
    "medical",
    "health",
    "healthcare",
    "illness",
    "condition",
    "infection",
    "pain",
    "fever",
    "cancer",
    "diabetes",
    "insulin",
    "blood pressure",
    "cholesterol",
    "heart",
    "lung",
    "kidney",
    "liver",
    "brain",
    "pregnancy",
    "pregnant",
    "allergy",
    "allergic",
    "vitamin",
    "therapy",
    "surgery",
    "vaccine",
    "vaccination",
}


def check_topic(query: str) -> GuardrailResult:
    normalized_query = query.lower()

    for term in MEDICAL_TERMS:
        if re.search(rf"\b{re.escape(term)}\b", normalized_query):
            return GuardrailResult(
                allowed=True,
                reason=f"Medical term detected: {term}",
            )

    return GuardrailResult(
        allowed=False,
        reason="No recognized medical terminology detected.",
    )