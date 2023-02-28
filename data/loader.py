import json
from os import path
from typing import Dict, List

import importlib_resources
from shapely import wkt
from shapely.geometry import Polygon

from base import Report, PlyShape, PlyResult, PickResult, shallow_as_dict
from data import DATA_MODULE_NAME


class ReportEncoder(json.JSONEncoder):
    _PLY_SHAPE_KEY = "__ply_shape__"
    _PLY_RESULT_KEY = "__ply_result__"
    _PICK_RESULT_KEY = "__pick_result__"
    _POLYGON_KEY = "__polygon__"
    _REPORT_KEY = "__report__"

    def default(self, obj):
        if isinstance(obj, Report):
            return {self._REPORT_KEY: shallow_as_dict(obj)}
        if isinstance(obj, PlyShape):
            return {self._PLY_SHAPE_KEY: shallow_as_dict(obj)}
        if isinstance(obj, PlyResult):
            return {self._PLY_RESULT_KEY: shallow_as_dict(obj)}
        if isinstance(obj, PickResult):
            return {self._PICK_RESULT_KEY: shallow_as_dict(obj)}
        if isinstance(obj, Polygon):
            return {self._POLYGON_KEY: wkt.dumps(obj)}
        return json.JSONEncoder.default(self, obj)

    @staticmethod
    def decode_special(dct: Dict):
        if ReportEncoder._REPORT_KEY in dct:
            return Report(**dct[ReportEncoder._REPORT_KEY])
        if ReportEncoder._POLYGON_KEY in dct:
            return wkt.loads(dct[ReportEncoder._POLYGON_KEY])
        if ReportEncoder._PLY_SHAPE_KEY in dct:
            return PlyShape(**dct[ReportEncoder._PLY_SHAPE_KEY])
        if ReportEncoder._PLY_RESULT_KEY in dct:
            return PlyResult(**dct[ReportEncoder._PLY_RESULT_KEY])
        if ReportEncoder._PICK_RESULT_KEY in dct:
            return PickResult(**dct[ReportEncoder._PICK_RESULT_KEY])
        return dct


def get_report(file_name: str) -> Report:
    with importlib_resources.files(DATA_MODULE_NAME).joinpath(file_name).open("r") as f:
        return json.load(f, object_hook=ReportEncoder.decode_special)


def dump_report(report: Report, file_name: str):
    with importlib_resources.files(DATA_MODULE_NAME).joinpath(file_name).open("w") as f:
        json.dump(report, f, cls=ReportEncoder)


def get_example_file_paths() -> List[str]:
    result = []
    for item in importlib_resources.files(DATA_MODULE_NAME).iterdir():
        if item.is_file():
            (_, ext) = path.splitext(item.name)
            if ext == ".json":
                result.append(item.name)
    return result
