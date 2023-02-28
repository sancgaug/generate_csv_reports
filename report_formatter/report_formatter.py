from abc import ABC, abstractmethod

from base import Report


class ReportFormatter(ABC):
    DISPLAY_NAME: str = "Report Format"  # override me!
    DISPLAY_DESCRIPTION: str = "Does Nothing"  # override me!

    def __init__(self, report: Report):
        self.report = report

    @abstractmethod
    def generate(self, out_path_no_extension: str) -> str:
        raise NotImplementedError()
