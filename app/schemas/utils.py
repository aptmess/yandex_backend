from datetime import datetime


def check_isoformat_data(date: str):
    try:
        datetime.fromisoformat(date.replace('Z', '+00:00'))
    except ValueError as ex:
        raise ex
    return True
