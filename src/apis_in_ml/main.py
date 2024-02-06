"""FastAPI app and endpoints."""

import uuid
from typing import List, Tuple

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi_auth_middleware import AuthMiddleware, FastAPIUser
from sqlalchemy.orm.session import Session
from sqlmodel import SQLModel
from starlette.authentication import BaseUser, requires
from starlette.requests import Request

from apis_in_ml.classifier import TextClassifier
from apis_in_ml.crud import (
    add_participant,
    delete_participant,
    get_classification_result,
    get_participant,
)
from apis_in_ml.database import SessionLocal, engine
from apis_in_ml.models import ClassificationInput, Participant


# Dependency
def get_db():
    SQLModel.metadata.create_all(engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello MLE Fellowship!"}


@app.get("/participant/{id}")
def read_participant(id: int, db: Session = Depends(get_db)) -> Participant:
    """Retrieve a participant from the database."""

    participant = get_participant(db=db, participant_id=id)

    if participant is None:
        raise HTTPException(status_code=404, detail="Participant not found")

    return participant


@app.delete("/participant/{participant_id}")
def remove_participant(participant_id: int, db: Session = Depends(get_db)):
    """Delete a participant from the database."""

    deleted_participant_id = delete_participant(db=db, participant_id=participant_id)

    if deleted_participant_id is None:
        raise HTTPException(status_code=404, detail="Participant not found")

    return {"message": f"Deleted participant with ID {deleted_participant_id}"}
