import csv

from shapely.geometry import Polygon

from base import picks_first_valid, picks_primary_failure_reason, compactness
from report_formatter.csv_report_formatter import CSVReportFormatter


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
