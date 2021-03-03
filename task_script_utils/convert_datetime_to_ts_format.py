import dateparser, arrow, datetime
from dateutil import tz


def convert_datetime_to_ts_format(
    datetime, datetime_format: str = "", timezone: str = ""
):
    """ Convert datetime to TetraScience standard: ISO-8601 in milliseconds in UTC if timezone is available
    
        Inputs:
            datetime - raw datetime
            datetime_format - raw datetime format (must follow https://arrow.readthedocs.io/en/stable/#format)
            timezone - user-defined timezone. If the user specify an timezone, it will overwrite the timezone extracted from the raw datetime. It can be either string (i.e. "GMT-5") or a timezone type recognized by the arrow.get function.
            

        Output:
            Datetime string in ISO-8601 with millisecond precision. If timezone is defined, it will be in UTC indicated by 'Z'.
                
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
            f"Could not parse input datetime string {datetime} using {parser_name} and the following input formats: {datetime_format}"
        )

    timezone_to_use = parsed_time.tzinfo

    if timezone:
        try:
            timezone_to_use = tz.gettz(timezone)
        except:
            print(
                "The provided timezone can't be parsed by dateutil tz, going to use the plain value"
            )
            timezone_to_use = timezone

    datetime_iso_local = ""
    utc_indicator = ""

    if timezone_to_use:
        datetime_iso_local = arrow.get(str(parsed_time), tzinfo=timezone_to_use)
        utc_indicator = "Z"

    else:
        datetime_iso_local = arrow.get(str(parsed_time), tzinfo=tz.gettz("GMT"))

    ts_datetime = (
        datetime_iso_local.to("GMT")
        .format("YYYY-MM-DDTHH:mm:ss.SSSZ")
        .replace("+0000", utc_indicator)
    )

    return ts_datetime
