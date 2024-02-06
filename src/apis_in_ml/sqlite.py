from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel, select

from apis_in_ml.models import Classification, Participant


class SQLiteClient:
    """Client for fetching data from sqlite DB."""

    def __init__(self, db_file_path: str) -> None:
        self.engine = create_engine(f"sqlite:///{db_file_path}")

    def get_participant(self, participant_id: int) -> Participant:
        """Retrieve a participant from the database.

        Attributes:
            participant_id (int): A participant ID.
        """

        with Session(self.engine) as session:
            statement = select(Participant).where(Participant.id == participant_id)
            participant = session.exec(statement).first()
            session.close()

        return participant

    def delete_participant(self, participant_id: int) -> Participant:
        """Delete a participant from the database.

        Attributes:
            participant_id (int): A participant ID.
        """

        with Session(self.engine) as session:
            statement = Participant.delete().where(Participant.id == participant_id)
            participant = session.exec(statement)
            session.commit()

        return participant

    def add_participant(self, participant: Participant) -> Participant:
        """Add a participant to the database.

        Attributes:
            participant (Participant): A participant object.
        """

        with Session(self.engine) as session:
            session.add(participant)
            session.commit()

        return participant

    # Note: Proper implementation of this would likely separate out these
    # two different database interactions
    def get_classification_result(self, run_id: str) -> Classification:
        """Retrieve a classification result from the database.

        Attributes:
            run_id (int): A run ID.
        """

        with Session(self.engine) as session:
            statement = select(Classification).where(Classification.run_id == run_id)
            result = session.exec(statement).first()
            session.close()

        return result

    def add_classification_result(
        self, classification: Classification
    ) -> Classification:
        """Add a classification result to the database.

        Attributes:
            classification (Classification): A Classification object.
        """
        with Session(self.engine) as session:
            session.add(classification)
            session.commit()

        return classification


def create_db_and_tables() -> None:
    """Create the database and tables."""

    client = SQLiteClient(db_file_path="fellowship.db")

    SQLModel.metadata.create_all(client.engine)
