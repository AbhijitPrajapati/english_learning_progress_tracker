from typing import Any

from app.domain.analysis import Analysis, CategoryFrequency, Mistake, MistakeCategory

CURRENT_DOCUMENT_VERSION = 2


def analysis_to_document(analysis: Analysis) -> dict[str, Any]:
    return {
        "schema_version": CURRENT_DOCUMENT_VERSION,
        "mistakes": [
            {
                "category": mistake.category.value,
                "original_text": mistake.original_text,
                "correction": mistake.correction,
                "explanation": mistake.explanation,
            }
            for mistake in analysis.mistakes
        ],
        "frequencies": [
            {
                "category": frequency.category.value,
                "occurrences": frequency.occurrences,
                "opportunities": frequency.opportunities,
            }
            for frequency in analysis.frequencies
        ],
        "feedback": analysis.feedback,
    }


def analysis_from_document(document: dict[str, Any]) -> Analysis:
    version = int(document.get("schema_version", 1))
    if version not in {CURRENT_DOCUMENT_VERSION}:
        raise ValueError(f"Unsupported analysis document version: {version}")
    frequencies = []
    for item in document.get("frequencies", []):
        frequencies.append(
            CategoryFrequency(
                category=MistakeCategory(str(item["category"])),
                occurrences=int(item["occurences"]),
                opportunities=int(item["opportunities"]),
            )
        )

    return Analysis(
        mistakes=tuple(
            Mistake(
                category=MistakeCategory(str(item["category"])),
                original_text=str(item["original_text"]),
                correction=str(item["correction"]),
                explanation=str(item["explanation"]),
            )
            for item in document.get("mistakes", [])
        ),
        frequencies=tuple(frequencies),
        feedback=str(document.get("feedback", "")),
    )
