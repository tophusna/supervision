from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Tuple

import numpy as np


def _validate_class_ids(class_id: Any, n: int) -> None:
    """
    Ensure that class_id is a 1d np.ndarray with (n, ) shape.
    """
    is_valid = isinstance(class_id, np.ndarray) and class_id.shape == (n,)
    if not is_valid:
        raise ValueError("class_id must be 1d np.ndarray with (n, ) shape")


def _validate_confidence(confidence: Any, n: int) -> None:
    """
    Ensure that confidence is a 1d np.ndarray with (n, ) shape.
    """
    if confidence is not None:
        is_valid = isinstance(confidence, np.ndarray) and confidence.shape == (n,)
        if not is_valid:
            raise ValueError("confidence must be 1d np.ndarray with (n, ) shape")


@dataclass
class Classifications:
    class_id: np.ndarray
    confidence: Optional[np.ndarray] = None

    def __post_init__(self) -> None:
        """
        Validate the classification inputs.
        """
        n = len(self.class_id)

        _validate_class_ids(self.class_id, n)
        _validate_confidence(self.confidence, n)

    @classmethod
    def from_ultralytics(cls, ultralytics_results) -> Classifications:
        """
        Creates a Classifications instance from a
        (https://github.com/ultralytics/ultralytics) inference result.

        Args:
            ultralytics_results (ultralytics.engine.results.Results):
                The output Results instance from ultralytics model

        Returns:
            Classifications: A new Classifications object.

        Example:
            ```python
            >>> import cv2
            >>> from ultralytics import YOLO
            >>> import supervision as sv

            >>> image = cv2.imread(SOURCE_IMAGE_PATH)
            >>> model = YOLO('yolov8n-cls.pt')
            >>> model = YOLO('yolov8s-cls.pt')

            >>> result = model(image)[0]
            >>> classifications = sv.Classifications.from_ultralytics(result)
            ```
        """
        confidence = ultralytics_results.probs.data.cpu().numpy()
        return cls(class_id=np.arange(confidence.shape[0]), confidence=confidence)

    @classmethod
    def from_timm(cls, timm_results) -> Classifications:
        """
        Creates a Classifications instance from a
        timm (https://huggingface.co/docs/hub/timm) model.

        Args:
            timm: The output Results instance from timm model

        Returns:
            Classifications: A new Classifications object.

        Example:
            ```python
            >>> import timm
            >>> from PIL import Image
            >>> from timm.data import resolve_data_config
            >>> from timm.data.transforms_factory import create_transform

            >>> model = timm.create_model(
            ...     'hf-hub:nateraw/resnet50-oxford-iiit-pet',
            ...     pretrained=True
            ... )
            >>> model.eval()

            >>> config = resolve_data_config({}, model=model)
            >>> transform = create_transform(**config)

            >>> image = Image.open('../image.jpg').convert('RGB')
            >>> x = transform(image).unsqueeze(0)

            >>> output = model(x)

            >>> predictions = sv.Classifications.from_timm(output)
            ```
        """
        confidence = timm_results.data.cpu().numpy()[0]
        class_ids = list(range(len(confidence)))

        if len(class_ids) == 0:
            return cls(class_id=np.array([]), confidence=np.array([]))

        return cls(class_id=np.array(class_ids), confidence=confidence)

    def get_top_k(self, k: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Retrieve the top k class IDs and confidences,
            ordered in descending order by confidence.

        Args:
            k (int): The number of top class IDs and confidences to retrieve.

        Returns:
            Tuple[np.ndarray, np.ndarray]: A tuple containing
                the top k class IDs and confidences.

        Example:
            ```python
            >>> import supervision as sv

            >>> classifications = sv.Classifications(...)

            >>> classifications.get_top_k(1)

            (array([1]), array([0.9]))
            ```
        """
        if self.confidence is None:
            raise ValueError("top_k could not be calculated, confidence is None")

        order = np.argsort(self.confidence)[::-1]
        top_k_order = order[:k]
        top_k_class_id = self.class_id[top_k_order]
        top_k_confidence = self.confidence[top_k_order]

        return top_k_class_id, top_k_confidence
