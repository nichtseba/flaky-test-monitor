import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from flaky_monitor.parser import parse_report

FIXTURES = Path(__file__).parent / "fixtures"


def test_passed_testcase():
    xml = b'<testsuite><testcase classname="mod" name="test_a" time="0.5"/></testsuite>'

    results = parse_report(xml)

    assert len(results) == 1
    assert results[0].name == "test_a"
    assert results[0].status == "passed"
    assert results[0].duration == 0.5


def test_failed_testcase_with_message():
    xml = b'''<testsuite>
        <testcase classname="mod" name="test_b" time="0.1">
            <failure message="assert 1 == 2">Traceback...</failure>
        </testcase>
    </testsuite>'''

    results = parse_report(xml)

    assert results[0].status == "failed"
    assert results[0].message == "assert 1 == 2"


def test_error_testcase():
    xml = b'''<testsuite>
        <testcase classname="mod" name="test_c" time="0.2">
            <error message="RuntimeError: boom">Traceback...</error>
        </testcase>
    </testsuite>'''

    results = parse_report(xml)

    assert results[0].status == "error"
    assert results[0].message == "RuntimeError: boom"


def test_skipped_testcase():
    xml = b'''<testsuite>
        <testcase classname="mod" name="test_d" time="0.0">
            <skipped message="not on Windows"/>
        </testcase>
    </testsuite>'''

    results = parse_report(xml)

    assert results[0].status == "skipped"
    assert results[0].message == "not on Windows"


def test_testsuites_root_element():
    xml = b'''<testsuites>
        <testsuite name="first">
            <testcase classname="mod" name="test_e" time="0.1"/>
        </testsuite>
        <testsuite name="second">
            <testcase classname="mod" name="test_f" time="0.1"/>
        </testsuite>
    </testsuites>'''

    results = parse_report(xml)

    assert [r.name for r in results] == ["test_e", "test_f"]


def test_missing_time_defaults_to_zero():
    xml = b'<testsuite><testcase classname="mod" name="test_g"/></testsuite>'

    results = parse_report(xml)

    assert results[0].duration == 0.0


def test_empty_testsuite_returns_empty_list():
    results = parse_report(b'<testsuite/>')

    assert results == []


def test_invalid_xml_raises_parse_error():
    with pytest.raises(ET.ParseError):
        parse_report(b'<testsuite>')


def test_real_pytest_report():
    xml = (FIXTURES / "report_red.xml").read_bytes()

    results = parse_report(xml)

    assert len(results) == 5
    failed = [r.name for r in results if r.status == "failed"]
    assert failed == ["test_flaky_timing"]
