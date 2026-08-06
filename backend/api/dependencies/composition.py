from fastapi import Request

from backend.infrastructure.composition import InfrastructureComposition


def get_composition(request: Request) -> InfrastructureComposition:
    return request.app.state.composition
