import json
import time
from pathlib import Path

import torch
from PIL import Image

from train import create_model
from transforms import get_eval_transforms


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "model.pt"
LABELS_PATH = BASE_DIR / "models" / "labels.json"

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

MODEL_VERSION = "1.0.0"


def load_labels():
    with open(LABELS_PATH, "r") as f:
        labels = json.load(f)
    return {int(k): v for k, v in labels.items()}


def load_model():
    model = create_model()
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model.to(DEVICE)
    model.eval()
    return model


def predict_image(image_path, model=None, labels=None, top_k=3):
    if model is None:
        model = load_model()
    if labels is None:
        labels = load_labels()

    image = Image.open(image_path).convert("RGB")
    transform = get_eval_transforms()
    input_tensor = transform(image).unsqueeze(0).to(DEVICE)

    start_time = time.time()

    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)

    inference_ms = (time.time() - start_time) * 1000

    top_probs, top_indices = torch.topk(probabilities, k=top_k)

    top_predictions = [
        {
            "class_name": labels[idx.item()],
            "probability": round(prob.item(), 4),
        }
        for prob, idx in zip(top_probs, top_indices)
    ]

    predicted_class = top_predictions[0]["class_name"]
    confidence = top_predictions[0]["probability"]

    return {
        "predicted_class": predicted_class,
        "confidence": confidence,
        "top_predictions": top_predictions,
        "inference_ms": round(inference_ms, 2),
        "model_version": MODEL_VERSION,
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: uv run python training/inference.py <path_to_image>")
        sys.exit(1)

    image_path = sys.argv[1]
    result = predict_image(image_path)
    print(json.dumps(result, indent=2))