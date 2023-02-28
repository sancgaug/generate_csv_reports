from abc import ABC
from collections import Counter
from dataclasses import dataclass, field, fields
from math import pi
from typing import List, Tuple, Dict

from shapely.geometry import Polygon


@dataclass
class PlyShape:
    label: str = None
    parent_file: str = None
    geom: Polygon = None
    material_label: str = None
    bounding_box_axes: Tuple[float, float] = None


@dataclass
class PickResult:
    cell_label: str = None
    end_effector_label: str = None
    plyshape: PlyShape = field(default_factory=PlyShape)
    plyshape_orientation: float = 0.0
    valid: bool = False
    reason: str = "Unknown error"
    end_effector_orientation: float = 0.0
    end_effector_translation_x: float = 0.0
    end_effector_translation_y: float = 0.0
    active_valves: List[str] = field(default_factory=list)
    zone_index: int = 0
    weight: float = 0.0


@dataclass
class PlyResult:
    picks: List[PickResult] = field(default_factory=list)
    success_rate: float = 0.0


@dataclass
class Report:
    picks: List[PickResult] = field(default_factory=list)
    time_estimate: Dict[str, float] = field(default_factory=dict)
    tec_config_label: str = None
    ply_results: List[PlyResult] = field(default_factory=list)
    failed_filenames: List[str] = field(default_factory=list)


def shallow_as_dict(obj):
    return dict((f.name, getattr(obj, f.name)) for f in fields(obj))


class ReportFormatter(ABC):
    DISPLAY_NAME: str = "Report Format"  # override me!
    DISPLAY_DESCRIPTION: str = "Does Nothing"  # override me!

    def __init__(self, report: Report):
        self.report = report

    def generate(self, out_path_no_extension: str) -> str:
        raise NotImplementedError()


def compactness(geom: Polygon) -> float:
    """Polsby-Popper measure of compactness: in range 0-100%"""
    return ((4 * pi * geom.area) / (geom.length**2)) * 100 if geom.length != 0 else 0


def picks_failures(picks: List[PickResult]) -> List[PickResult]:
    """
    Returns a list of invalid picks
    """
    return [pick for pick in picks if not pick.valid]


def picks_primary_failure_reason(picks: List[PickResult]) -> str:
    """
    Returns the primary failure reason of a list of invalid picks.
    Primary failure reason is the most common reason for failure."""
    if len(picks_failures(picks)) == 0:
        return ""

    return Counter(
        [pick.reason.split("-")[-1] for pick in picks if not pick.valid]
    ).most_common(n=1)[0][0]


def picks_first_valid(picks: List[PickResult]) -> PickResult:
    """
    Returns the first valid pick in a list of picks. Return last pick if no valid pick found.
    """
    for pick in picks:
        if pick.valid:
            return pick
    return picks[-1]


