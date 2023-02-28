import csv

from base import Report
from report_formatter.csv_report_formatter import CSVReportFormatter


class CSVTimeEstFormatter(CSVReportFormatter):
    DISPLAY_NAME: str = "Time Estimate (CSV)"

    def __init__(self, report: Report) -> None:
        super().__init__(report)
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
