import sys
from dateutil import tz
from task_script_utils.convert_datetime_to_ts_format import convert_datetime_to_ts_format


def test_no_timezone():
    raw_expect = [
        ("2019-07-17 11:21:00", "2019-07-17T11:21:00.000"),
        ("2020-06-18 13:17:57.54036", "2020-06-18T13:17:57.540"),
    ]
    for raw, expect in raw_expect:
        assert convert_datetime_to_ts_format(raw) == expect


def test_embedded_timezone():
    raw_expect = [
        ("2020-03-06T17:19:45.706000-05:00", "2020-03-06T22:19:45.706Z"),
        ("2020-04-30T20:27:41.000Z", "2020-04-30T20:27:41.000Z"),
    ]
    for raw, expect in raw_expect:
        assert convert_datetime_to_ts_format(raw) == expect


def test_input_timezone():
    raw_timezone_expect = [
        ("2019-07-17 11:21:00", "GMT-5", "2019-07-17T16:21:00.000Z"),
        (
            "2019-07-17 11:21:00",
            tz.tzoffset("GMT", -5 * 60 * 60),  # offset in seconds
            "2019-07-17T16:21:00.000Z",
        ),
        ("2019-07-17 11:21:00", tz.tzutc(), "2019-07-17T11:21:00.000Z"),
        ("2020-04-30T20:27:41.000Z", "GMT+3", "2020-04-30T17:27:41.000Z"),
    ]
    for raw, timezone, expect in raw_timezone_expect:
        assert convert_datetime_to_ts_format(raw, timezone=timezone) == expect


def test_input_timezone_overrides_embedded():
    raw_timezone_expect = [
        ("2020-03-06T17:19:45.706000-05:00", "GMT+5", "2020-03-06T12:19:45.706Z")
    ]
    for raw, raw_timezone, expect in raw_timezone_expect:
        assert convert_datetime_to_ts_format(raw, timezone=raw_timezone) == expect


def test_unreadable_format():
    try:
        convert_datetime_to_ts_format("20200512T235847.070Z")
    except:
        exc_info = sys.exc_info()
        assert exc_info[0] == ValueError


def test_format_strings():
    raw_format_expect = [
        ("20200512T235847.070Z", "YYYYMMDDTHHmmss.SZ", "2020-05-12T23:58:47.070Z"),
    ]
    for raw, format, expect in raw_format_expect:
        assert convert_datetime_to_ts_format(raw, format) == expect


def test_YDM_order():
    raw_format_expect = [
        (
            "2020-03-06T17:19:45.706000-05:00",
            "YYYY-DD-MMTHH:mm:ss.SZZ",
            "2020-06-03T22:19:45.706Z",
        )
    ]
    for raw, format, expect in raw_format_expect:
        assert convert_datetime_to_ts_format(raw, format) == expect


def test_bad_timezone():
    try:
        convert_datetime_to_ts_format(
            "2020-03-06T17:19:45.706000-05:00", timezone="GMT+500"
        )
    except:
        exc_info = sys.exc_info()
        assert exc_info[0] == TypeError

