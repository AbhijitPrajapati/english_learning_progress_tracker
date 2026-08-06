from fastapi import Depends

from app.application.ports.services import (
    GrammarAnalysisAdapter,
    PasswordHasher,
    TokenService,
    TranscriptionAdapter,
)
from app.infrastructure.composition import InfrastructureComposition

from .composition import get_composition


def get_transcriber(
    composition: InfrastructureComposition = Depends(get_composition),
) -> TranscriptionAdapter:
    return composition.transcriber


def get_grammar_analyzer(
    composition: InfrastructureComposition = Depends(get_composition),
) -> GrammarAnalysisAdapter:
    return composition.grammar_analyzer


def get_password_hasher(
    composition: InfrastructureComposition = Depends(get_composition),
) -> PasswordHasher:
    return composition.password_hasher


def get_token_service(
    composition: InfrastructureComposition = Depends(get_composition),
) -> TokenService:
    return composition.token_service
