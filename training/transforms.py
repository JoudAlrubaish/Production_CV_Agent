from torchvision import transforms
from torchvision.transforms import functional as F


IMAGE_SIZE = 224

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]


class ResizeWithPadding:
    def __init__(self, size):
        self.size = size

    def __call__(self, image):
        image = F.resize(
            image,
            self.size,
            antialias=True,
        )

        width, height = image.size

        pad_width = max(self.size - width, 0)
        pad_height = max(self.size - height, 0)

        left = pad_width // 2
        top = pad_height // 2
        right = pad_width - left
        bottom = pad_height - top

        image = F.pad(
            image,
            [left, top, right, bottom],
            fill=0,
        )

        image = F.center_crop(image, [self.size, self.size])

        return image


def get_train_transforms():
    return transforms.Compose([
        ResizeWithPadding(IMAGE_SIZE),

        transforms.RandomHorizontalFlip(p=0.5),

        transforms.ColorJitter(
            brightness=0.15,
            contrast=0.15,
            saturation=0.10,
            hue=0.02,
        ),

        transforms.ToTensor(),

        transforms.Normalize(
            mean=IMAGENET_MEAN,
            std=IMAGENET_STD,
        ),
    ])


def get_eval_transforms():
    return transforms.Compose([
        ResizeWithPadding(IMAGE_SIZE),

        transforms.ToTensor(),

        transforms.Normalize(
            mean=IMAGENET_MEAN,
            std=IMAGENET_STD,
        ),
    ])