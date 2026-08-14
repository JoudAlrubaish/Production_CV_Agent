
import json
import time
from io import BytesIO
from pathlib import Path
import torch
from PIL import Image
from torchvision import models

from backend.app.config import settings
from training.transforms import get_eval_transforms


NUM_CLASSES = 6

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

_MODEL = None
_LABELS = None


def create_model():
    model = models.mobilenet_v3_small(
        weights=None
    )

    in_features = model.classifier[-1].in_features

    model.classifier[-1] = torch.nn.Linear(
        in_features,
        NUM_CLASSES,
    )

    return model


def load_labels():
    global _LABELS

    if _LABELS is not None:
        return _LABELS

    labels_path = (
        Path(settings.model_path).parent
        / "labels.json"
    )

    if not labels_path.exists():
        raise FileNotFoundError(
            f"Labels file not found: {labels_path}"
        )

    with open(labels_path, "r") as file:
        labels = json.load(file)

    _LABELS = {
        int(key): value
        for key, value in labels.items()
    }

    return _LABELS


def load_model():
    global _MODEL

    if _MODEL is not None:
        return _MODEL

    model_path = Path(settings.model_path)

    if not model_path.exists():
        raise FileNotFoundError(
            f"Model file not found: {model_path}"
        )

    model = create_model()

    state_dict = torch.load(
        model_path,
        map_location=DEVICE,
        weights_only=True,
    )

    model.load_state_dict(state_dict)

    model.to(DEVICE)
    model.eval()

    _MODEL = model

    return _MODEL


def is_model_loaded():
    return _MODEL is not None


def predict_image_bytes(
    image_bytes: bytes,
    top_k: int = 3,
):
    model = load_model()
    labels = load_labels()

    image = Image.open(
        BytesIO(image_bytes)
    ).convert("RGB")

    transform = get_eval_transforms()

    input_tensor = (
        transform(image)
        .unsqueeze(0)
        .to(DEVICE)
    )

    start_time = time.perf_counter()

    with torch.no_grad():
        outputs = model(input_tensor)

        probabilities = torch.nn.functional.softmax(
            outputs[0],
            dim=0,
        )

    inference_ms = (
        time.perf_counter() - start_time
    ) * 1000

    k = min(top_k, len(labels))

    top_probs, top_indices = torch.topk(
        probabilities,
        k=k,
    )

    top_predictions = [
        {
            "class_name": labels[index.item()],
            "probability": round(
                probability.item(),
                4,
            ),
        }
        for probability, index
        in zip(top_probs, top_indices)
    ]

    return {
        "predicted_class":
            top_predictions[0]["class_name"],

        "confidence":
            top_predictions[0]["probability"],

        "top_predictions":
            top_predictions,

        "inference_ms":
            round(inference_ms, 2),

        "model_version":
            settings.model_version,
    }