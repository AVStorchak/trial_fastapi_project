from pydantic import BaseModel


class Query(BaseModel):
    filename: str
