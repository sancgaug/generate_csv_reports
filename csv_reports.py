import csv
from hashlib import md5

from shapely.geometry import Polygon

from base import Report, ReportFormatter, PickResult, picks_first_valid, picks_primary_failure_reason, compactness


class CSVReportFormatter(ReportFormatter):
    DISPLAY_NAME: str = "Detailed Data Output (CSV)"

    def __init__(self, report: Report) -> None:
        self._report = report

    def ply_id(self, pick: PickResult) -> str:
        return md5(pick.plyshape.geom.wkb).hexdigest()

    def encode_active_cups(self, pick: PickResult) -> bytes:
        separator = "*"
        data = separator.join(pick.active_valves)
        return data

    def generate(self, out: str) -> str:
        with open(out + ".csv", "w", newline="") as f:
            writer = csv.writer(f)
            fields = (
                "file",
                "ply",
                "cell",
                "ee",
                "area",
                "perimeter",
                "compactness",
                "num_holes",
                "holes_perimeter",
                "holes_area",
                "material",
                "ply_phi",
                "valid",
                "reason",
                "zone",
                "weight",
                "ee_x",
                "ee_y",
                "ee_phi",
                "num_cups",
                "active_cups",
            )

            writer.writerow(fields)
            for pick in self._report.picks:
                parent_file = pick.plyshape.parent_file
                ply_id = pick.plyshape.label
                geom: Polygon = pick.plyshape.geom
                area = geom.area
                perimeter = geom.length
                compactness_value = compactness(geom)

                # Holes
                polygons = [Polygon(h.coords) for h in geom.interiors]
                num_holes = len(polygons)
                holes_perimeter = sum(h.length for h in polygons)
                holes_area = sum([h.area for h in polygons])

                writer.writerow(
                    [
                        parent_file,
                        ply_id,
                        pick.cell_label,
                        pick.end_effector_label,
                        area,
                        perimeter,
                        compactness_value,
                        num_holes,
                        holes_perimeter,
                        holes_area,
                        pick.plyshape.material_label,
                        pick.plyshape_orientation,
                        pick.valid,
                        pick.reason,
                        pick.zone_index,
                        pick.weight,
                        pick.end_effector_translation_x,
                        pick.end_effector_translation_y,
                        pick.end_effector_orientation,
                        len(pick.active_valves),
                        self.encode_active_cups(pick),
                    ]
                )
        return out + ".csv"


class CSVAttentionPliesFormatter(ReportFormatter):
    DISPLAY_NAME: str = "Plies Requiring Attention Overview (CSV)"

    def __init__(self, report: Report) -> None:
        self._report = report

    def generate(self, out: str) -> str:
        with open(out + "_attention.csv", "w", newline="") as f:
            writer = csv.writer(f)
            fields = ("file", "ply", "cell", "ee", "success_rate")

            writer.writerow(fields)
            ply_results = sorted(
                self._report.ply_results, key=lambda p: p.success_rate, reverse=True
            )

            for ply in ply_results:
                if ply.success_rate < 1:
                    writer.writerow(
                        [
                            ply.picks[0].plyshape.parent_file,
                            ply.picks[0].plyshape.label,
                            ply.picks[0].cell_label,
                            ply.picks[0].end_effector_label,
                            round(100 * ply.success_rate),
                        ]
                    )
        return out + "_attention.csv"


class CSVUnprocessedPliesFormatter(CSVAttentionPliesFormatter):
    DISPLAY_NAME: str = "Overview of DXF files with warnings (CSV)"

    def __init__(self, report: Report) -> None:
        self._report = report

    def generate(self, out: str) -> str:
        with open(out + "_unprocessed.csv", "w", newline="") as f:
            writer = csv.writer(f)
            fields = "filename"
            writer.writerow([fields])

            for file in self._report.failed_filenames:
                writer.writerow([file])
        return out + "_unprocessed.csv"


class CSVBoundingBoxFormatter(CSVReportFormatter):
    DISPLAY_NAME: str = "Detailed Data Output w Bounding Box (CSV)"

    def __init__(self, report: Report) -> None:
        self._report = report

    def generate(self, out: str) -> str:
        with open(out + "bb.csv", "w", newline="") as f:
            writer = csv.writer(f)
            fields = (
                "file",
                "ply",
                "cell",
                "ee",
                "area",
                "perimeter",
                "compactness",
                "num_holes",
                "holes_perimeter",
                "holes_area",
                "material",
                "ply_phi",
                "valid",
                "reason",
                "zone",
                "weight",
                "ee_x",
                "ee_y",
                "ee_phi",
                "num_cups",
                "max_x",
                "max_y",
                "active_cups",
            )

            writer.writerow(fields)
            for pick in self._report.picks:
                parent_file = pick.plyshape.parent_file
                ply_id = pick.plyshape.label
                geom: Polygon = pick.plyshape.geom
                area = geom.area
                perimeter = geom.length
                compactness_value = compactness(geom)

                # Holes
                polygons = [Polygon(h.coords) for h in geom.interiors]
                num_holes = len(polygons)
                holes_perimeter = sum(h.length for h in polygons)
                holes_area = sum([h.area for h in polygons])

                writer.writerow(
                    [
                        parent_file,
                        ply_id,
                        pick.cell_label,
                        pick.end_effector_label,
                        area,
                        perimeter,
                        compactness_value,
                        num_holes,
                        holes_perimeter,
                        holes_area,
                        pick.plyshape.material_label,
                        pick.plyshape_orientation,
                        pick.valid,
                        pick.reason,
                        pick.zone_index,
                        pick.weight,
                        pick.end_effector_translation_x,
                        pick.end_effector_translation_y,
                        pick.end_effector_orientation,
                        len(pick.active_valves),
                        round(pick.plyshape.bounding_box_axes[0]),
                        round(pick.plyshape.bounding_box_axes[1]),
                        self.encode_active_cups(pick),
                    ]
                )
        return out + "bb.csv"


class CSVSinglePhiFormatter(CSVReportFormatter):
    DISPLAY_NAME: str = "Simple Data Output w Bounding Box (CSV)"

    def generate(self, out: str) -> str:
        with open(out + "simple_bb.csv", "w", newline="") as f:
            writer = csv.writer(f)
            fields = (
                "file",
                "ply",
                "cell",
                "ee",
                "area",
                "perimeter",
                "compactness",
                "num_holes",
                "holes_perimeter",
                "holes_area",
                "material",
                "ply_phi",
                "valid",
                "reason",
                "zone",
                "weight",
                "ee_x",
                "ee_y",
                "ee_phi",
                "num_cups",
                "max_x",
                "max_y",
                "active_cups",
            )

            writer.writerow(fields)

            for ply in self._report.ply_results:
                pick = picks_first_valid(ply.picks)
                primary_failure_reason = picks_primary_failure_reason(ply.picks)
                ply_id = pick.plyshape.label
                parent_file = pick.plyshape.parent_file
                geom: Polygon = pick.plyshape.geom
                area = geom.area
                perimeter = geom.length
                compactness_value = compactness(geom)

                # Holes
                polygons = [Polygon(h.coords) for h in geom.interiors]
                num_holes = len(polygons)
                holes_perimeter = sum(h.length for h in polygons)
                holes_area = sum([h.area for h in polygons])

                writer.writerow(
                    [
                        parent_file,
                        ply_id,
                        pick.cell_label,
                        pick.end_effector_label,
                        area,
                        perimeter,
                        compactness_value,
                        num_holes,
                        holes_perimeter,
                        holes_area,
                        pick.plyshape.material_label,
                        pick.plyshape_orientation,
                        pick.valid,
                        primary_failure_reason,
                        pick.zone_index,
                        pick.weight,
                        pick.end_effector_translation_x,
                        pick.end_effector_translation_y,
                        pick.end_effector_orientation,
                        len(pick.active_valves),
                        round(pick.plyshape.bounding_box_axes[0]),
                        round(pick.plyshape.bounding_box_axes[1]),
                        self.encode_active_cups(pick),
                    ]
                )
        return out + "simple_bb.csv"


class CSVTimeEstFormatter(CSVReportFormatter):
    DISPLAY_NAME: str = "Time Estimate (CSV)"

    def __init__(self, report: Report) -> None:
        self._report = report

    def generate(self, out: str) -> str:
        with open(out + "time_est.csv", "w", newline="") as f:
            writer = csv.writer(f)
            fields = ("process", "time", "cell", "ee", "material", "time_est_config")

            writer.writerow(fields)
            pick = self._report.picks[0]
            timing = self._report.time_estimate
            for process, time in timing.items():
                writer.writerow(
                    [
                        process,
                        time,
                        pick.cell_label,
                        pick.end_effector_label,
                        pick.plyshape.material_label,
                        self._report.tec_config_label,
                    ]
                )
        return out + "time_est.csv"
