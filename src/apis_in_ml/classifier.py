import json
from typing import List

from loguru import logger
from sqlalchemy.orm.session import Session
from transformers import pipeline

from apis_in_ml.crud import add_classification_result
from apis_in_ml.models import Classification


class TextClassifier:
    """
    Text classifcation wrapper.
    Predicts the most appropriate label for a given string from a
    list of candidate labels.
    """

    def __init__(self, model_path: str, db: Session) -> None:
        self.pipe = pipeline("zero-shot-classification", model=model_path)
        self.db = db

    def predict_and_store(
        self, text: str, label_candidates: List[str], run_id: str
    ) -> None:
        """Run classification prediction and store in the database.

        Attributes:
            text (str): Text to classify
            label_candidates (List[str]): Possible labels
            run_id (str): Unique run ID
        """

        # Note: this has been implemented like this for ease of demo
        predictions = self.pipe(text, candidate_labels=label_candidates)
        logger.info(f"Prediction complete for run {run_id}.")

        top_prediction = predictions.get("labels")[0]
        top_prediction_confidence = predictions.get("scores")[0]

        add_classification_result(
            db=self.db,
            classification=Classification(
                run_id=run_id,
                status="COMPLETE",
                text=text,
                label_candidates=json.dumps(label_candidates),
                chosen_label=top_prediction,
                confidence=top_prediction_confidence,
            ),
        )

        logger.info(f"Prediction stored in DB for run {run_id}.")
