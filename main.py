import os
from datetime import datetime
from tempfile import gettempdir

from base import ReportFormatter
from csv_reports import CSVReportFormatter, CSVAttentionPliesFormatter, CSVUnprocessedPliesFormatter, \
    CSVBoundingBoxFormatter, CSVSinglePhiFormatter, CSVTimeEstFormatter
from data.loader import get_example_file_paths, get_report

CSV_REPORTS_DICT = {"CSVReportFormatter": CSVReportFormatter,
                    "CSVAttentionPliesFormatter": CSVAttentionPliesFormatter,
                    "CSVUnprocessedPliesFormatter": CSVUnprocessedPliesFormatter,
                    "CSVBoundingBoxFormatter": CSVBoundingBoxFormatter,
                    "CSVSinglePhiFormatter": CSVSinglePhiFormatter,
                    "CSVTimeEstFormatter": CSVTimeEstFormatter
                    }


def get_data_file() -> str:
    print("The following data files are available to test with: ")
    file_paths = get_example_file_paths()
    for file_path in file_paths:
        print(file_path)
    while True:
        chosen_file = input("Enter the name of the file to test with: ")
        if chosen_file in file_paths:
            return chosen_file
        else:
            print("Invalid file entered, retry")
            continue


def get_csv_report() -> ReportFormatter:
    print("The following reports are available: ")
    for report_key, report in CSV_REPORTS_DICT.items():
        print(f"{report_key} ({report.DISPLAY_NAME})")
    while True:
        chosen_report = input("Enter the name of the report to test with: ")
        if chosen_report in CSV_REPORTS_DICT.keys():
            return CSV_REPORTS_DICT[chosen_report]
        else:
            print("Invalid report entered, retry")
            continue


def get_report_file_name() -> str:
    report_generation_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_output_dir = os.path.join(gettempdir(), f"reports_{report_generation_datetime}")
    os.mkdir(report_output_dir)
    return os.path.join(report_output_dir, f"report_{report_generation_datetime}")


if __name__ == '__main__':
    while True:
        data_file = get_data_file()
        csv_report = get_csv_report()
        report_file_name_prefix = get_report_file_name()
        report_file_name = csv_report(get_report(data_file)).generate(report_file_name_prefix)
        print(f"Report {report_file_name} generated, Ctrl-C to stop the program")
