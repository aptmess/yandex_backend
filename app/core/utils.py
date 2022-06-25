from datetime import datetime
from math import floor
from typing import Any, Dict, Tuple

from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session


def convert_datetime_to_iso(dt: datetime) -> str:
    return dt.isoformat(
        timespec='milliseconds',
    ).replace('+00:00', 'Z')


def row2dict(r: DeclarativeMeta) -> Dict[str, Any]:
    return {c.name: getattr(r, c.name) for c in r.__table__.columns}


def recursive_nodes(
    root: DeclarativeMeta, session: Session, model: DeclarativeMeta
) -> Tuple[Dict[str, Any], datetime, int, int]:
    data = row2dict(root)
    db = (
        session.query(model.date, model.price)
        .filter(model.id == root.id)
        .order_by(model.date.desc())
        .first()
    )
    updated_date, price = db['date'], db['price']
    data['date'] = updated_date
    data['price'] = price
    if not root.children:
        return data, updated_date, price, 1

    data['children'] = []
    value, count = 0, 0
    for child in root.children:
        d, updated_date, price, current_count = recursive_nodes(
            child, session, model
        )
        value += price
        count += current_count
        data['children'].append(d)
        if data['date'] <= updated_date:
            data['date'] = updated_date
    data['price'] = int(floor(value / count))
    return data, updated_date, value, count


def check_isoformat_data(date: datetime) -> datetime:
    try:
        datetime.fromisoformat(str(date).replace('Z', '+00:00'))
    except ValueError as ex:
        raise ex
    return date


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
