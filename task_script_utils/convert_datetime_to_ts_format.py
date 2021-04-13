import dateparser
import arrow
import datetime as dt
from dateutil import tz
from typing import Union


def convert_datetime_to_ts_format(
    datetime, datetime_format: str = "", timezone: Union[str, dt.tzinfo] = ""
) -> str:
    """ Convert datetime to TetraScience standard: ISO-8601 in milliseconds in UTC if timezone is available

    Inputs:
        datetime - datetime string
        datetime_format - datetime format string
            (must follow https://arrow.readthedocs.io/en/stable/#format)
        timezone - user-defined timezone. If specified, this overwrites any
            timezone in the input datetime. It can be a string or a timezone
            type accepted by arrow.get. Timezone strings must come from the tz
            timezone database, e.g. "EDT" is not allowed, but is equivalent to
            "America/New York".

    Output:
        Datetime string in ISO-8601 format with millisecond precision.
            If timezone is defined, the output is in UTC, indicated by 'Z'.
            Otherwise, the output will be timezone unaware, indicated by 
            having no 'Z' at the end.

        Examples:
        If timezone is defined: "2019-07-17T14:21:00.000Z"
        If timezone is not defined: "2019-07-17T11:21:00.000"
    """

    if datetime_format:
        parsed_time = arrow.get(datetime, datetime_format)
        parser_name = "arrow"
    else:
        parsed_time = dateparser.parse(datetime)
        parser_name = "dateparser"

    if parsed_time is None:
        raise ValueError(
            f"Could not parse input datetime string {datetime} using {parser_name} and the following input formats: '{datetime_format}'"
        )

    utc_indicator = "Z"
    timezone_to_use = timezone if timezone else parsed_time.tzinfo

    if not timezone_to_use:
        timezone_to_use = tz.gettz("GMT")
        utc_indicator = ""

    datetime_iso_local = arrow.get(
        str(parsed_time),
        tzinfo=timezone_to_use
    )

    ts_datetime = (
        datetime_iso_local.to("GMT")
        .format("YYYY-MM-DDTHH:mm:ss.SSSZ")
        .replace("+0000", utc_indicator)
    )

    return ts_datetime
