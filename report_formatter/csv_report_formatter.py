import csv
from hashlib import md5

from shapely.geometry import Polygon

from base import compactness, PickResult, Report
from report_formatter.report_formatter import ReportFormatter


class CSVReportFormatter(ReportFormatter):
    DISPLAY_NAME: str = "Detailed Data Output (CSV)"

    def __init__(self, report: Report) -> None:
        super().__init__(report)
        self._report = report

    @staticmethod
    def ply_id(pick: PickResult) -> str:
        return md5(pick.plyshape.geom.wkb).hexdigest()

    @staticmethod
    def encode_active_cups(pick: PickResult) -> str:
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
