from pathlib import Path

from torchvision.datasets import ImageFolder


CLASS_NAMES = [
    "angry",
    "happy",
    "neutral",
    "sad",
    "suprised",
    "tired",
]


def create_dataset(data_dir: Path, transform=None):
    return ImageFolder(
        root=data_dir,
        transform=transform,
    )