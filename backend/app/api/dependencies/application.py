from typing import Annotated

from fastapi import Depends, Request

from app.container import ApplicationContainer


def get_container(request: Request) -> ApplicationContainer:
    return request.app.state.container


ContainerDependency = Annotated[ApplicationContainer, Depends(get_container)]
