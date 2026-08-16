# Computer Vision Model Documentation

## 1. Task

The Computer Vision task is:

```text
Multi-Class Facial Emotion Classification
```

The system predicts one of six classes:

```text
angry
happy
neutral
sad
suprised
tired
```

---

## 2. Dataset

Source:

```text
Roboflow Universe
```

Dataset URL:

```text
<ROBOFLOW_DATASET_URL>
```

The dataset is organized using an ImageFolder-compatible structure.

```text
train/
valid/
test/
```

Each split contains one folder per class.

---

## 3. Dataset Loading

The project uses:

```python
torchvision.datasets.ImageFolder
```

This means class labels are derived from directory names.

---

## 4. Input Processing

Input size:

```text
224 × 224
```

Images are converted to RGB.

The preprocessing pipeline uses a custom resize-with-padding transform to preserve the image more consistently before final cropping.

Evaluation transforms:

```text
Resize with padding
ToTensor
ImageNet normalization
```

ImageNet normalization:

```text
Mean:
[0.485, 0.456, 0.406]

Standard deviation:
[0.229, 0.224, 0.225]
```

---

## 5. Data Augmentation

Training uses:

```text
RandomHorizontalFlip
ColorJitter
```

Color jitter modifies:

```text
Brightness
Contrast
Saturation
Hue
```

The goal is to reduce overfitting and improve robustness.

---

# 6. Model Architecture

Architecture:

```text
MobileNetV3 Small
```

Framework:

```text
PyTorch
```

Transfer learning is used with ImageNet pretrained weights.

The original classifier output is replaced by a six-class linear layer.

Conceptually:

```text
Image
 ↓
MobileNetV3 Feature Extractor
 ↓
Classifier
 ↓
6-Class Output
```

---

# 7. Training Configuration

Current configuration:

```text
Batch Size: 32
Epochs: 10
Learning Rate: 1e-4
Optimizer: Adam
Loss: CrossEntropyLoss
```

Device selection:

```text
CUDA if available
otherwise CPU
```

---

# 8. Model Selection

During training, validation accuracy is monitored.

The best model checkpoint is saved as:

```text
models/model.pt
```

This ensures that the deployed model corresponds to the best validation checkpoint rather than simply the final epoch.

---

# 9. Production Artifacts

The model artifacts are:

```text
models/model.pt
models/labels.json
models/model_metrics.json
```

`model.pt` contains the model parameters.

`labels.json` maps class indices to class names.

`model_metrics.json` stores evaluation information.

---

# 10. Evaluation Results

Stored metrics:

| Metric | Result |
|---|---:|
| Best Validation Accuracy | 0.96 |
| Final Test Accuracy | 0.96 |
| Epochs | 10 |
| Number of Classes | 6 |
| Test Set Size | 127 |

Per-class F1:

| Class | F1 |
|---|---:|
| Angry | 0.96 |
| Happy | 0.97 |
| Neutral | 0.92 |
| Sad | 0.94 |
| Suprised | 0.97 |
| Tired | 1.00 |

---

# 11. Production Inference

Production inference performs:

```text
Load model
 ↓
Load labels
 ↓
Decode image
 ↓
Convert RGB
 ↓
Apply evaluation transforms
 ↓
Forward pass
 ↓
Softmax
 ↓
Top-K
 ↓
Return result
```

Output:

```json
{
  "predicted_class": "happy",
  "confidence": 0.94,
  "top_predictions": [
    {
      "class_name": "happy",
      "probability": 0.94
    }
  ],
  "inference_ms": 30.5,
  "model_version": "1.0.0"
}
```

---

# 12. Model Caching

The production backend keeps the loaded model in memory.

This avoids reloading `model.pt` for every API request.

Benefits include:

```text
Lower inference latency
Less disk I/O
Better production performance
```

---

# 13. Additional Validation

During system integration, the model was tested on images beyond the original training workflow.

The model successfully demonstrated multi-class prediction and was confirmed not to be a single-class collapsed model.

However, some external images produced noticeably weaker results than held-out dataset images.

This indicates that model generalization is sensitive to distribution differences between the original dataset and external real-world images.

---

# 14. Model Limitations

The most important limitations are:

```text
Small official test set
Dataset-specific visual distribution
Possible domain shift
Facial-expression ambiguity
External-image generalization
Class confusion for some samples
```

---

# 15. Recommended Future Work

Potential improvements include:

```text
Collect more diverse real-world images
Increase external validation size
Add targeted augmentation
Evaluate class balancing
Compare EfficientNet / ResNet / ConvNeXt
Use confidence calibration
Add face detection before classification
Perform cross-dataset evaluation
Track production prediction drift
```

---

# 16. Important Interpretation Note

The model identifies visible facial-expression patterns.

It does not determine a person's actual psychological or emotional state.

Therefore predictions should not be used for:

```text
Medical diagnosis
Psychological assessment
Employment decisions
Legal decisions
Other high-impact decisions
```
