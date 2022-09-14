from dateutil import parser


def to_filename(iso8601_string: str):
    timestamp = parser.parse(iso8601_string)
    return timestamp.strftime("%Y%m%dT%H%M%S+%Z")
