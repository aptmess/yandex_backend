from datetime import datetime
from math import floor


# import re
#
# regex = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
#
#
# match_iso8601 = re.compile(regex).match
#
#
# def check_isoformat_data(str_val):
#     if match_iso8601(str_val) is not None:
#         return str_val
#     else:
#         raise ValueError(f'{str_val} not in iso 8601 format')
#
def row2dict(r):
    return {c.name: getattr(r, c.name) for c in r.__table__.columns}


def recursive_nodes(root):
    data = row2dict(root)
    updated_date = data['date']
    if not root.children:
        return data, updated_date, root.price, 1
    else:
        data['children'] = []
        value, count = 0, 0
        for child in root.children:
            d, updated_date, price, current_count = recursive_nodes(child)
            value += price
            count += current_count
            data['children'].append(d)
            if data['date'] <= updated_date:
                data['date'] = updated_date
        data['price'] = int(floor(value / count))
        return data, updated_date, value, count


def check_isoformat_data(date: str):
    try:
        datetime.fromisoformat(str(date).replace('Z', '+00:00'))
    except ValueError as ex:
        raise ex
    return date
