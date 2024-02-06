"""FastAPI app and endpoints."""

import uuid
from pathlib import Path
from typing import List, Tuple

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi_auth_middleware import AuthMiddleware, FastAPIUser
from starlette.authentication import BaseUser, requires
from starlette.requests import Request

from apis_in_ml.classifier import TextClassifier
from apis_in_ml.models import ClassificationInput, Participant
from apis_in_ml.sqlite import SQLiteClient


# TODO: for fellows to add
def verify_authorization_header(auth_header: str) -> Tuple[List[str], BaseUser]:
    # Usually you would decode the JWT here and verify its signature to extract
    # the 'sub'
    user = FastAPIUser(first_name="Alex", last_name="Rogers", user_id=1)
    # You could for instance use the scopes provided in the JWT or request them
    # by looking up the scopes with the 'sub' somewhere
    scopes = ["admin"]
    return scopes, user


app = FastAPI()

# TODO: for fellows to add
app.add_middleware(AuthMiddleware, verify_header=verify_authorization_header)


@app.get("/")
def root(request: Request):
    return {"message": f"Hello MLE Fellowship, user {request.user.first_name}!"}


@app.get("/participant/{id}")
# TODO: fellows to add request parameter
def get_participant(request: Request, id: int) -> Participant:
    """Retrieve a participant from the database."""

    db = SQLiteClient(db_file_path=Path(f"fellowship.db"))
    participant = db.get_participant(participant_id=id)

    if participant is None:
        raise HTTPException(status_code=404, detail="Participant not found")

    return participant


@app.delete("/participant/{participant_id}")
# TODO: for fellows to add decorator and request parameter
@requires("poweruser")
def delete_participant(request: Request, participant_id: int) -> Participant:
    """Delete a participant from the database."""

    db = SQLiteClient(db_file_path=Path(f"fellowship.db"))
    participant = db.get_participant(participant_id=participant_id)

    if participant is None:
        raise HTTPException(status_code=404, detail="Participant not found")

    return participant


# TODO: to be added by the fellows
@app.post("/participant/")
# TODO: for fellows to add decorator and request parameter
@requires("admin")
def add_participant(request: Request, participant: Participant) -> Participant:
    """Add participant to the database."""

    db = SQLiteClient(db_file_path=Path(f"fellowship.db"))

    return db.add_participant(participant=participant)


# TODO: fellows to add all of the below with detailed instructions
@app.post("/classify/")
def classify(
    classification_input: ClassificationInput, background_tasks: BackgroundTasks
):
    """Run classification prediction for input."""

    run_id = str(uuid.uuid4())

    classifier = TextClassifier(model_path="classifier/")
    background_tasks.add_task(
        classifier.predict_and_store,
        classification_input.text,
        classification_input.label_candidates,
        run_id,
    )

    return {"message": f"Inference triggered with ID {run_id}"}


@app.get("/classify/{run_id}")
def get_classify(run_id: str):
    """Get classification results."""

    db = SQLiteClient(db_file_path=Path(f"fellowship.db"))
    result = db.get_classification_result(run_id=run_id)

    if result is None:
        return {"message": f"Result not ready for run {run_id}"}

    return result
