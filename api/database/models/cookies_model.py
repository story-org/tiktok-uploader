from sqlmodel import SQLModel, Field


class Cookies(SQLModel, table=True):
    id: str = Field(primary_key=True)
    value: str
