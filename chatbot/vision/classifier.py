import time
from io import BytesIO

import torch
from PIL import Image
from torchvision.models import mobilenet_v2, MobileNet_V2_Weights


class ImageClassifier:
    def __init__(self):
        self.weights = MobileNet_V2_Weights.DEFAULT
        self.model = mobilenet_v2(weights=self.weights)
        self.model.eval()
        self.preprocess = self.weights.transforms()
        self.categories = self.weights.meta["categories"]

    @torch.inference_mode()
    def predict(self, image_bytes: bytes, top_k: int = 5):
        start = time.perf_counter()

        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        tensor = self.preprocess(image).unsqueeze(0)

        outputs = self.model(tensor)
        probabilities = torch.softmax(outputs[0], dim=0)

        scores, indices = torch.topk(probabilities, top_k)

        predictions = [
            {
                "label": self.categories[idx.item()],
                "score": round(score.item(), 4),
            }
            for score, idx in zip(scores, indices)
        ]

        latency_ms = round((time.perf_counter() - start) * 1000, 2)

        return {
            "model": "mobilenet_v2",
            "task": "image_classification",
            "top_k": top_k,
            "latency_ms": latency_ms,
            "predictions": predictions,
        }