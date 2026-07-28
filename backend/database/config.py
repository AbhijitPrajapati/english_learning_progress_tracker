from pydantic import BaseModel


class PostgresConfig(BaseModel):
    user: str
    password: str
    host: str
    db: str
