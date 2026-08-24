"""
prediction.py — Day 9
======================
Prediction router.  Prefix: /api/prediction

This router is completely separate from energy.py (/api/energy) to guarantee
zero route duplication.

Endpoints
---------
POST /api/prediction/energy/predict
    Receive a device_id, fetch history from DB, derive features, run XGBoost,
    return predicted next energy.

GET  /api/prediction/energy/predictions/latest
    Return the latest on-request prediction for every device in the database.
    Devices without enough history are reported with status='error'.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import PredictionRequest, PredictionResponse
from ..services import prediction_service

router = APIRouter(
    prefix="/api/prediction",
    tags=["prediction"],
)


@router.post(
    "/energy/predict",
    response_model=PredictionResponse,
    summary="Predict next energy for a device",
    description=(
        "Given a device_id, fetches the last 3 readings from the database, "
        "derives all 15 XGBoost model features (direct sensor values + time + "
        "lag features), and returns the predicted next energy (kWh). "
        "Requires at least 3 stored readings for the device."
    ),
)
def predict_energy(
    request: PredictionRequest,
    db: Session = Depends(get_db),
):
    """
    POST /api/prediction/energy/predict

    Body: { "device_id": "LAB001" }

    Returns: PredictionResponse with predicted_next_energy in kWh.
    Raises 404 if device not found, 422 if < 3 readings exist, 503 if model unavailable.
    """
    return prediction_service.predict_next_energy(request.device_id, db)


@router.get(
    "/energy/predictions/latest",
    summary="Latest prediction for every device",
    description=(
        "Computes and returns an on-request prediction for every distinct device "
        "in the database. Predictions are NOT stored — they are computed fresh on "
        "each call using only historical data already in the database. "
        "Devices with fewer than 3 readings will appear with status='error'."
    ),
)
def latest_predictions(db: Session = Depends(get_db)):
    """
    GET /api/prediction/energy/predictions/latest

    Returns a list of prediction objects (one per device).
    Each item has either status='ok' with full prediction, or status='error'
    with a detail message.
    """
    return prediction_service.get_latest_predictions(db)
