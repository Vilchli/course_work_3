from json import JSONDecodeError

import pytest
import json

from utils.services import load_json, date_format, sort_by_date, get_last_five_successful_operations, mask_card


def test_load_json():
    assert load_json('tests/data_tests/correct.json') == []

    with pytest.raises(JSONDecodeError):
        assert load_json('tests/data_tests/no_correct.json')


def test_date_format():
    test_data = "2019-04-18T11:22:18.800453"
    assert date_format(test_data) == "18.04.2019"


def test_sort_by_date():
    test_data1 = [
        {"date": "2019-04-19T12:02:30.129240"},
        {"date": "2019-11-13T17:38:04.800051"},
        {"date": "2019-06-30T15:11:53.136004"}
    ]

    assert sort_by_date(test_data1) == [
        {"date": "2019-11-13T17:38:04.800051"},
        {"date": "2019-06-30T15:11:53.136004"},
        {"date": "2019-04-19T12:02:30.129240"}
    ]


def test_get_last_five_successful_operations():
    test_data2 = [
        {"state": "CANCELED", "date": "2019-11-13T17:38:04.800051"},
        {"state": "EXECUTED", "date": "2019-06-30T15:11:53.136004"},
        {"state": "EXECUTED", "date": "2019-04-19T12:02:30.129240"},
        {"state": "EXECUTED", "date": "2018-04-16T17:34:19.241289"},
        {"state": "EXECUTED", "date": "2018-02-13T04:43:11.374324"},
        {"state": "EXECUTED", "date": "2018-02-03T07:16:28.366141"}
    ]

    assert get_last_five_successful_operations(test_data2) == [
        {"state": "EXECUTED", "date": "2019-06-30T15:11:53.136004"},
        {"state": "EXECUTED", "date": "2019-04-19T12:02:30.129240"},
        {"state": "EXECUTED", "date": "2018-04-16T17:34:19.241289"},
        {"state": "EXECUTED", "date": "2018-02-13T04:43:11.374324"},
        {"state": "EXECUTED", "date": "2018-02-03T07:16:28.366141"}
    ]


def test_mask_card():

    assert mask_card("Maestro 7552745726849311") == "Maestro 7552 74** **** 9311"
    assert mask_card("Visa Classic 6831982476737658") == "Visa Classic 6831 98** **** 7658"
    assert mask_card("Current account 38976430693692818358") == "Current account **8358"

