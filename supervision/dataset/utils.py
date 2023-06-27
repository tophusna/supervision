import os
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple, TypeVar

import cv2
import numpy as np

from supervision.detection.core import Detections
from supervision.detection.utils import (
    approximate_polygon,
    filter_polygons_by_area,
    mask_to_polygons,
)

T = TypeVar("T")


def approximate_mask_with_polygons(
    mask: np.ndarray,
    min_image_area_percentage: float = 0.0,
    max_image_area_percentage: float = 1.0,
    approximation_percentage: float = 0.75,
) -> List[np.ndarray]:
    height, width = mask.shape
    image_area = height * width
    minimum_detection_area = min_image_area_percentage * image_area
    maximum_detection_area = max_image_area_percentage * image_area

    polygons = mask_to_polygons(mask=mask)
    if len(polygons) == 1:
        polygons = filter_polygons_by_area(
            polygons=polygons, min_area=None, max_area=maximum_detection_area
        )
    else:
        polygons = filter_polygons_by_area(
            polygons=polygons,
            min_area=minimum_detection_area,
            max_area=maximum_detection_area,
        )
    return [
        approximate_polygon(polygon=polygon, percentage=approximation_percentage)
        for polygon in polygons
    ]


def generate_unique_class_map(class_lists: List[str]) -> List[str]:
    class_lists = [x.lower() for x in class_lists]
    class_lists_set = set(class_lists)
    return list(class_lists_set)


def remapped_detections(
    old_class_list: List[str], new_class_list: List[str], detections: Detections
) -> Detections:
    class_ids = detections.class_id
    for class_id, old_class_name in enumerate(old_class_list):
        new_id = new_class_list.index(old_class_name)
        class_ids[class_ids == class_id] = new_id
    detections.class_id = class_ids
    return detections


def save_dataset_images(
    images_directory_path: str, images: Dict[str, np.ndarray]
) -> None:
    Path(images_directory_path).mkdir(parents=True, exist_ok=True)

    for image_name, image in images.items():
        target_image_path = os.path.join(images_directory_path, image_name)
        cv2.imwrite(target_image_path, image)


def train_test_split(
    data: List[T],
    train_ratio: float = 0.8,
    random_state: Optional[int] = None,
    shuffle: bool = True,
) -> Tuple[List[T], List[T]]:
    """
    Splits the data into two parts using the provided train_ratio.

    Args:
        data (List[T]): The data to split.
        train_ratio (float): The ratio of the training set to the entire dataset.
        random_state (Optional[int]): The seed for the random number generator.
        shuffle (bool): Whether to shuffle the data before splitting.

    Returns:
        Tuple[List[T], List[T]]: The split data.
    """
    if random_state is not None:
        random.seed(random_state)

    if shuffle:
        random.shuffle(data)

    split_index = int(len(data) * train_ratio)
    return data[:split_index], data[split_index:]
