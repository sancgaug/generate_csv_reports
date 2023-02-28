import csv

from base import Report
from report_formatter.csv_attention_plies_formatter import CSVAttentionPliesFormatter


class CSVUnprocessedPliesFormatter(CSVAttentionPliesFormatter):
    DISPLAY_NAME: str = "Overview of DXF files with warnings (CSV)"

    def __init__(self, report: Report) -> None:
        super().__init__(report)
        self._report = report

    def generate(self, out: str) -> str:
        with open(out + "_unprocessed.csv", "w", newline="") as f:
            writer = csv.writer(f)
            fields = "filename"
            writer.writerow([fields])

            for file in self._report.failed_filenames:
                writer.writerow([file])
        return out + "_unprocessed.csv"
