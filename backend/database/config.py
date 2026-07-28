from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    url: str
