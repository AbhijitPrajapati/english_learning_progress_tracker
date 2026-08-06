from fastapi import Request

from app.infrastructure.composition import InfrastructureComposition

"""
Root infrastructure composition dependency
"""


def get_composition(request: Request) -> InfrastructureComposition:
    return request.app.state.composition
