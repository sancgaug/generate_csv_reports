import csv

from shapely.geometry import Polygon

from base import compactness, Report
from report_formatter.csv_report_formatter import CSVReportFormatter


class CSVBoundingBoxFormatter(CSVReportFormatter):
    DISPLAY_NAME: str = "Detailed Data Output w Bounding Box (CSV)"

    def __init__(self, report: Report) -> None:
        super().__init__(report)
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
