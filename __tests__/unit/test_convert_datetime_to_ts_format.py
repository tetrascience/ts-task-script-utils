import pytest
from dateutil import tz
from task_script_utils.convert_datetime_to_ts_format import convert_datetime_to_ts_format


@pytest.mark.parametrize(
    "raw,expect",
    [
        ("2019-07-17 11:21:00", "2019-07-17T11:21:00.000"),
        ("2020-06-18 13:17:57.54036", "2020-06-18T13:17:57.540"),
    ]
)
def test_no_timezone(raw, expect):
    assert convert_datetime_to_ts_format(raw) == expect


@pytest.mark.parametrize(
    "raw,expect",
    [
        ("2020-03-06T17:19:45.706000-05:00", "2020-03-06T22:19:45.706Z"),
        ("2020-04-30T20:27:41.000Z", "2020-04-30T20:27:41.000Z"),
        ("2020-04-30T10:27:41.000 EDT", "2020-04-30T14:27:41.000Z"),
    ]
)
def test_embedded_timezone(raw, expect):
    assert convert_datetime_to_ts_format(raw) == expect


@pytest.mark.parametrize(
    "raw,timezone,expect",
    [
        ("2019-07-17 11:21:00", "GMT-5", "2019-07-17T16:21:00.000Z"),
        (
            "2019-07-17 11:21:00",
            tz.tzoffset("GMT", -5 * 60 * 60),  # offset in seconds
            "2019-07-17T16:21:00.000Z",
        ),
        ("2019-07-17 11:21:00", tz.tzutc(), "2019-07-17T11:21:00.000Z"),
        ("2020-04-30T20:27:41.000Z", "GMT+3", "2020-04-30T17:27:41.000Z"),
        ("2020-04-30T10:27:41.000", "America/New York", "2020-04-30T14:27:41.000Z"),
        ("2019-07-17 11:21:00", "", "2019-07-17T11:21:00.000"),
        ("2019-07-17 11:21:00", None, "2019-07-17T11:21:00.000"),
    ]
)
def test_input_timezone(raw, timezone, expect):
    assert convert_datetime_to_ts_format(raw, timezone=timezone) == expect


@pytest.mark.parametrize(
    "raw,timezone,expect",
    [
        ("2020-03-06T17:19:45.706000-05:00", "GMT+4", "2020-03-06T13:19:45.706Z")
    ]
)
def test_input_timezone_overrides_embedded(raw, timezone, expect):
    assert convert_datetime_to_ts_format(raw, timezone=timezone) == expect


@pytest.mark.parametrize(
    "raw,error_type",
    [
        ("20200512T235847.070Z", ValueError),
        ("11111 GMT", ValueError),
    ]
)
def test_unparsable_datetime(raw, error_type):
    pytest.raises(
        error_type,
        convert_datetime_to_ts_format,
        raw
    )


@pytest.mark.parametrize(
    "raw,format,expect",
    [
        ("20200512T235847.070Z", "YYYYMMDDTHHmmss.SZ", "2020-05-12T23:58:47.070Z"),
        ("2020-04-30T10:27:41.012 EST", "YYYY-MM-DDTHH:mm:ss.S ZZZ", "2020-04-30T15:27:41.012Z"),
    ]
)
def test_format_strings(raw, format, expect):
    assert convert_datetime_to_ts_format(raw, format) == expect

@pytest.mark.parametrize(
    "raw,format,timezone,expect",
    [
        ("20200512T235847.070", "YYYYMMDDTHHmmss.S", "GMT-3", "2020-05-13T02:58:47.070Z"),
        ("2020-04-30T10:27:41.012", "YYYY-MM-DDTHH:mm:ss.S", "EST", "2020-04-30T15:27:41.012Z"),
    ]
)
def test_format_and_timezone(raw, format, timezone, expect):
    assert convert_datetime_to_ts_format(
        raw,
        datetime_format=format,
        timezone=timezone
    ) == expect


@pytest.mark.parametrize(
    "raw,format,expect",
    [
        (
            "2020-03-06T17:19:45.706000-05:00",
            "YYYY-DD-MMTHH:mm:ss.SZZ",
            "2020-06-03T22:19:45.706Z",
        ),
    ]
)
def test_YDM_order(raw, format, expect):
    assert convert_datetime_to_ts_format(raw, format) == expect


@pytest.mark.parametrize(
    "raw,format,timezone,error_type",
    [
        ("2020-03-06T17:19:45.706000-05:00", "", "GMT+500", ValueError),
        ("2020-03-06T17:19:45.706000-05:00", "", "inval", ValueError),
        ("2020-03-06T17:19:45.706", "", "EDT", ValueError), # EDT is not in the tz database
        ("2020-04-30T10:27:41.012", "YYYY-MM-DDTHH:mm:ss.S", "EDT", ValueError),
        ("2020-03-06T17:19:45.706000-05:00", "", 5, TypeError),
    ]
)
def test_bad_timezone(raw, format, timezone, error_type):
    pytest.raises(
        error_type,
        convert_datetime_to_ts_format,
        raw,
        datetime_format=format,
        timezone=timezone
    )
