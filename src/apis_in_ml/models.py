from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


# SQLModel class models can be used for both SQLAlchemy models
# and pydantic models at the same time
class Participant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    role: str


class Classification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    run_id: str
    status: str
    text: str
    label_candidates: str = Field(sa_column=Column(JSON))
    chosen_label: str
    confidence: float


# Example of a Pydantic class model
class ClassificationInput(BaseModel):
    text: str
    label_candidates: List[str]
