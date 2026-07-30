from pydantic import BaseModel


class PostgresConfig(BaseModel):
    url: str
