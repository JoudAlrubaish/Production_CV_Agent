#Image expected flow: Upload image - Check file type - Check image validity - Check model.pt - model missing - 503 error 
from io import BytesIO
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from PIL import Image, UnidentifiedImageError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.schemas import PredictionResponse
from backend.app.services.inference import predict_image_bytes
from backend.app.services.prediction_service import save_prediction


router = APIRouter(
    prefix="/api/v1/predict",
    tags=["Predictions"],
)


ALLOWED_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

MAX_UPLOAD_SIZE = 5 * 1024 * 1024


@router.post(
    "",
    response_model=PredictionResponse,
)
async def predict_image(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # 1. Validate file type
    if image.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported image type. Use JPEG, PNG, or WEBP.",
        )

    # 2. Read uploaded image
    image_bytes = await image.read()

    # 3. Validate file size
    if len(image_bytes) > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Image is too large. Maximum size is 5 MB.",
        )

    # 4. Validate that the uploaded file is a real image
    try:
        uploaded_image = Image.open(
            BytesIO(image_bytes)
        )
        uploaded_image.verify()

    except (UnidentifiedImageError, OSError):
        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted image.",
        )

    # 5. Run real model inference
    try:
        result = predict_image_bytes(
            image_bytes
        )

    except FileNotFoundError:
        raise HTTPException(
            status_code=503,
            detail="Computer vision model is not available.",
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Model inference failed.",
        )

    # 6. Keep only the filename
    safe_image_name = Path(
        image.filename or "uploaded_image"
    ).name

    # 7. Save prediction in PostgreSQL
    try:
        prediction = save_prediction(
            db=db,
            image_name=safe_image_name,
            inference_result=result,
        )

    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Prediction could not be stored in the database.",
        )

    # 8. Return stored prediction
    return prediction