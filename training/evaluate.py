import json
from pathlib import Path

import torch
from sklearn.metrics import classification_report, confusion_matrix

from train import create_model, create_dataloaders, DEVICE


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "model.pt"
DATA_DIR = BASE_DIR / "data" / "raw"

CLASS_NAMES = ["angry", "happy", "neutral", "sad", "suprised", "tired"]


def run_full_evaluation():
    _, _, test_loader = create_dataloaders(DATA_DIR)

    model = create_model()
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model.to(DEVICE)
    model.eval()

    all_preds = []
    all_labels = []

    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(DEVICE)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)

            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.numpy())

    print("=== Classification Report ===")
    print(classification_report(all_labels, all_preds, target_names=CLASS_NAMES))

    print("=== Confusion Matrix ===")
    cm = confusion_matrix(all_labels, all_preds)
    print("Rows = actual, Columns = predicted")
    print("Classes order:", CLASS_NAMES)
    print(cm)


if __name__ == "__main__":
    run_full_evaluation()