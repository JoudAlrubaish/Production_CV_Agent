#Image expected flow: Upload image - Check file type - Check image validity - Check model.pt - model missing - 503 error 
from io import BytesIO
from pathlib import Path
from fastapi import APIRouter, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
from backend.app.config import settings

router = APIRouter(
    prefix="/api/v1/predict",
    tags=["Predictions"],
)


ALLOWED_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


@router.post("")
async def predict_image(
    image: UploadFile = File(...),
):
    # accept only valid file type
    if image.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported image type. Use JPEG, PNG, or WEBP.",
        )

    # read the uploaded file
    image_bytes = await image.read()

    # check that the uploaded file is actually a valid image
    try:
        uploaded_image = Image.open(BytesIO(image_bytes))
        uploaded_image.verify()
    except (UnidentifiedImageError, OSError):
        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted image.",
        )

    # the CV model is not available yet
    if not Path(settings.model_path).exists():
        raise HTTPException(
            status_code=503,
            detail="Computer vision model is not available yet.",
        )

    return {
        "message": "Model is available and ready for inference integration."
    }