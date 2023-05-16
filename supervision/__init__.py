__version__ = "0.8.0"

from supervision.dataset.core import BaseDataset, DetectionDataset
from supervision.detection.annotate import BoxAnnotator, MaskAnnotator
from supervision.detection.core import Detections
from supervision.detection.line_counter import LineZone, LineZoneAnnotator
from supervision.detection.tools.polygon_zone import PolygonZone, PolygonZoneAnnotator
from supervision.detection.utils import (
    box_iou_batch,
    filter_polygons_by_area,
    mask_to_polygons,
    mask_to_xyxy,
    non_max_suppression,
    polygon_to_mask,
    polygon_to_xyxy,
)
from supervision.draw.color import Color, ColorPalette
from supervision.draw.utils import draw_filled_rectangle, draw_polygon, draw_text
from supervision.file import list_files_with_extensions
from supervision.geometry.core import Point, Position, Rect
from supervision.geometry.utils import get_polygon_center
from supervision.notebook.utils import plot_image, plot_images_grid
from supervision.video import (
    VideoInfo,
    VideoSink,
    get_video_frames_generator,
    process_video,
)
