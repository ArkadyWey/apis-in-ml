from sqlalchemy.orm.session import Session

from apis_in_ml.models import Classification, Participant


def get_participant(db: Session, participant_id: int) -> Participant:
    """Retrieve a participant from the database.

    Attributes:
        db (Session): Database session.
        participant_id (int): A participant ID.
    """
    return db.query(Participant).filter(Participant.id == participant_id).first()


def delete_participant(db: Session, participant_id: int) -> Participant:
    """Delete a participant from the database.

    Attributes:
        db (Session): Database session.
        participant_id (int): A participant ID.
    """
    participant = (
        db.query(Participant).filter(Participant.id == participant_id).delete()
    )
    db.commit()
    return participant


def add_participant(db: Session, participant: Participant) -> Participant:
    """Add a participant to the database.

    Attributes:
        db (Session): Database session.
        participant (Participant): A participant object.
    """

    db.add(participant)
    db.commit()
    db.refresh(participant)

    return participant


# Note: Proper implementation of this would likely separate out these
# two different database interactions
def get_classification_result(db: Session, run_id: str) -> Classification:
    """Retrieve a classification result from the database.

    Attributes:
        db (Session): Database session.
        run_id (int): A run ID.
    """
    return db.query(Classification).filter(Classification.run_id == run_id).first()


def add_classification_result(
    db: Session, classification: Classification
) -> Classification:
    """Add a classification result to the database.

    Attributes:
        db (Session): Database session.
        classification (Classification): A Classification object.
    """
    db.add(classification)
    db.commit()
    db.refresh(classification)

    return classification
