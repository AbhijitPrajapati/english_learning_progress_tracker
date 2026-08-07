from pydantic import BaseModel, ConfigDict


class DomainObject(BaseModel):
    """Base class for all domain objects"""

    model_config = ConfigDict(frozen=True)
