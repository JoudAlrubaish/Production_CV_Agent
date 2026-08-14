import torch
from torchvision import models
from torch.utils.data import DataLoader
from pathlib import Path

from dataset import create_dataset
from transforms import (
    get_train_transforms,
    get_eval_transforms,
)


NUM_CLASSES = 6


def create_model():
    model = models.mobilenet_v3_small(
        weights=models.MobileNet_V3_Small_Weights.DEFAULT
    )

    in_features = model.classifier[-1].in_features

    model.classifier[-1] = torch.nn.Linear(
        in_features,
        NUM_CLASSES,
    )

    return model


BATCH_SIZE = 32


def create_dataloaders(data_dir: Path):
    train_dataset = create_dataset(
        data_dir / "train",
        transform=get_train_transforms(),
    )

    valid_dataset = create_dataset(
        data_dir / "valid",
        transform=get_eval_transforms(),
    )

    test_dataset = create_dataset(
        data_dir / "test",
        transform=get_eval_transforms(),
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
    )

    valid_loader = DataLoader(
        valid_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
    )

    return train_loader, valid_loader, test_loader


# ============================================
# Model training and evaluation functions
# ============================================

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
NUM_EPOCHS = 10
LEARNING_RATE = 1e-4


def train_one_epoch(model, loader, criterion, optimizer):
    model.train()

    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in loader:
        images = images.to(DEVICE)
        labels = labels.to(DEVICE)

        optimizer.zero_grad()

        outputs = model(images)
        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        running_loss += loss.item() * images.size(0)

        _, predicted = torch.max(outputs, 1)
        correct += (predicted == labels).sum().item()
        total += labels.size(0)

    epoch_loss = running_loss / total
    epoch_accuracy = correct / total

    return epoch_loss, epoch_accuracy


def evaluate(model, loader, criterion):
    model.eval()

    running_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in loader:
            images = images.to(DEVICE)
            labels = labels.to(DEVICE)

            outputs = model(images)
            loss = criterion(outputs, labels)

            running_loss += loss.item() * images.size(0)

            _, predicted = torch.max(outputs, 1)
            correct += (predicted == labels).sum().item()
            total += labels.size(0)

    epoch_loss = running_loss / total
    epoch_accuracy = correct / total

    return epoch_loss, epoch_accuracy


def train_model(data_dir: Path, output_path: Path):
    train_loader, valid_loader, test_loader = create_dataloaders(data_dir)

    model = create_model()
    model = model.to(DEVICE)

    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

    best_valid_accuracy = 0.0

    for epoch in range(NUM_EPOCHS):
        train_loss, train_acc = train_one_epoch(
            model, train_loader, criterion, optimizer
        )
        valid_loss, valid_acc = evaluate(model, valid_loader, criterion)

        print(
            f"Epoch {epoch + 1}/{NUM_EPOCHS} | "
            f"train_loss={train_loss:.4f} train_acc={train_acc:.4f} | "
            f"valid_loss={valid_loss:.4f} valid_acc={valid_acc:.4f}"
        )

        if valid_acc > best_valid_accuracy:
            best_valid_accuracy = valid_acc
            torch.save(model.state_dict(), output_path)
            print(f"  -> saved new best model (valid_acc={valid_acc:.4f})")

    test_loss, test_acc = evaluate(model, test_loader, criterion)
    print(f"Final test accuracy: {test_acc:.4f}")

    return model


if __name__ == "__main__":
    data_dir = PROJECT_ROOT / "data" / "raw"
    output_path = Path("models/model.pt")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    train_model(data_dir, output_path)