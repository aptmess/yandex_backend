from datetime import datetime
from typing import Optional, Union
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.routes.log_route import LogRoute
from app.core.engine import get_session
from app.core.models import Shop, ShopHistory
from app.core.utils import row2dict
from app.exceptions import EXCEPTION_404_NOT_FOUND
from app.schemas.error import Error
from app.schemas.response import HTTP_400_RESPONSE, HTTP_404_RESPONSE
from app.schemas.shop_item import ShopUnitType
from app.schemas.statistic import ShopUnitStatisticResponse

router = APIRouter(route_class=LogRoute)


def get_children(root):
    if not root.children:
        pass
    else:
        for child in root.children:
            if child.type == ShopUnitType.OFFER:
                yield child.id
            yield from get_children(child)


@router.get(
    '/node/{id}/statistic',
    response_model=ShopUnitStatisticResponse,
    responses={
        status.HTTP_200_OK: {
            'description': 'Статистика по элементу',
            'model': ShopUnitStatisticResponse,
        },
        status.HTTP_400_BAD_REQUEST: HTTP_400_RESPONSE,
        status.HTTP_404_NOT_FOUND: HTTP_404_RESPONSE,
    },
)
def get_node_id_statistic(
    id: UUID,
    date_start: Optional[datetime] = Query(None, alias='dateStart'),
    date_end: Optional[datetime] = Query(None, alias='dateEnd'),
    session: Session = Depends(get_session),
) -> Union[ShopUnitStatisticResponse, Error]:
    """
    Получение статистики (истории обновлений) по товару/категории за заданный полуинтервал [from, to).

    - Статистика по удаленным элементам недоступна.

    - Цена категории - это средняя цена всех её товаров, включая товары дочерних категорий.

    - Если категория не содержит товаров цена равна null.

    - При обновлении цены товара, средняя цена категории, которая содержит этот товар, тоже обновляется.

    - Можно получить статистику за всё время.

    Output:

    - 200: Статистика по элементу.

    - 400: Некорректный формат запроса или некорректные даты интервала. "Validation Failed"

    - 404: Категория/товар не найден. "Item not found"
    """
    condition = []
    if date_start is not None:
        condition.append(ShopHistory.date >= date_start)
        if date_end is not None:
            condition.append(ShopHistory.date < date_end)
    else:
        if date_end is not None:
            condition.append(ShopHistory.date < date_end)
    type_cat = session.query(Shop.type).filter(Shop.id == id).one_or_none()
    if type_cat is None:
        raise EXCEPTION_404_NOT_FOUND

    elif type_cat.type == ShopUnitType.OFFER:
        t1 = (
            session.query(ShopHistory)
            .filter(ShopHistory.id == id, *condition)
            .subquery('t1')
        )
        items = (
            session.query(t1, Shop.name, Shop.type, Shop.parentId)
            .filter(t1.c.id == Shop.id)
            .order_by(t1.c.date.desc())
            .all()
        )
        if len(items) > 0:
            return {'items': items}
    else:
        shop = session.query(Shop).filter(Shop.id == id).first()
        childrends = tuple(get_children(shop))
        query = (
            session.query(ShopHistory)
            .filter(ShopHistory.id.in_(childrends), *condition)
            .subquery('t1')
        )
        datetimes = (
            session.query(query.c.date)
            .distinct()
            .order_by(query.c.date.asc())
            .all()
        )
        result = []
        if len(datetimes) > 0:
            for x in datetimes:
                windows_params = {
                    'partition_by': [query.c.id],
                    'order_by': query.c.date.desc(),
                }
                tmp = (
                    session.query(
                        query,
                        func.row_number()
                        .over(**windows_params)
                        .label('row_number'),
                    )
                    .filter(query.c.date <= x[0])
                    .subquery('t2')
                )

                res = (
                    session.query(tmp.c.price)
                    .filter(tmp.c.row_number == 1)
                    .all()
                )
                result.append(
                    {
                        **row2dict(shop),
                        **{
                            'date': x[0],
                            'price': sum([x[0] for x in res]) / len(res),
                        },
                    }
                )
        return {'items': result}
