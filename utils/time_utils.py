from dateutil.parser import parse


def parse_date_year(date_str):
    parsed_year = parse(date_str).year
    return parsed_year
