from fastapi import Depends

from application.speeches.transcription import TranscriptionAdapter
from backend.application.speeches.grammar_analysis import GrammarAnalysisAdapter
from backend.application.users.password_hasher import PasswordHasher
from backend.application.users.token_service import TokenService
from backend.infrastructure.composition import InfrastructureComposition

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
