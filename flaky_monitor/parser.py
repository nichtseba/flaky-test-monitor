import xml.etree.ElementTree as ET
from dataclasses import dataclass


@dataclass
class TestResult:
    classname: str
    name: str
    status: str            # "passed", "failed", "error" oder "skipped"
    duration: float        # Sekunden
    message: str | None    # Fehlermeldung, nur bei failed/error/skipped


def parse_report(xml_bytes: bytes) -> list[TestResult]:
    # TODO: XML einlesen, über alle <testcase> laufen, Status bestimmen
    ...
