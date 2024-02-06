import json
from pathlib import Path
from typing import List

from loguru import logger
from transformers import pipeline

from apis_in_ml.models import Classification
from apis_in_ml.sqlite import SQLiteClient


class TextClassifier:
    """Text classifcation wrapper."""

    def __init__(self, model_path: str) -> None:
        self.pipe = pipeline("zero-shot-classification", model=model_path)
        self.db = SQLiteClient(db_file_path=Path("fellowship.db"))

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

        self.db.add_classification_result(
            Classification(
                run_id=run_id,
                status="COMPLETE",
                text=text,
                label_candidates=json.dumps(label_candidates),
                chosen_label=top_prediction,
                confidence=top_prediction_confidence,
            )
        )

        logger.info(f"Prediction stored in DB for run {run_id}.")
