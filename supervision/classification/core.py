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

    def get_top_k(self, k: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Retrieve the top k class IDs and confidences, ordered in descending order by confidence.

        Args:
            k (int): The number of top class IDs and confidences to retrieve.

        Returns:
            Tuple[np.ndarray, np.ndarray]: A tuple containing the top k class IDs and confidences.

        Example:
            ```python
            >>> import supervision as sv

            >>> cd = sv.ClassificationDataset(...)

            >>> cd.annotations["image.png"].get_top_k(1)

            (array([1]), array([0.9]))
        """
        if self.confidence is None:
            raise ValueError("confidence is None")

        order = np.argsort(self.confidence.copy())[::-1]
        top_k_order = order[:k]
        top_k_class_id = self.class_id[top_k_order]
        top_k_confidence = self.confidence[top_k_order]

        return top_k_class_id, top_k_confidence
