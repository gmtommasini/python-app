from datetime import datetime


def is_valid_date(date_str: str) -> bool:
    """
    Checks if input string is a date in the YYYY-MM-DD format
    """
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False
