import csv

from base import Report
from report_formatter.report_formatter import ReportFormatter


class CSVAttentionPliesFormatter(ReportFormatter):
    DISPLAY_NAME: str = "Plies Requiring Attention Overview (CSV)"

    def __init__(self, report: Report) -> None:
        super().__init__(report)
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
