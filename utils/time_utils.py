from dateutil.parser import parse


def parse_date(date_str):
    parsed_date = parse(date_str)
    return parsed_date
