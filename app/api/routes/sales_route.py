from datetime import datetime, timedelta
from typing import Union

from fastapi import APIRouter, Depends, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.routes.log_route import LogRoute
from app.core.engine import get_session
from app.core.models import Shop, ShopHistory
from app.schemas.error import Error
from app.schemas.response import HTTP_400_RESPONSE
from app.schemas.shop_item import ShopUnitType
from app.schemas.statistic import ShopUnitStatisticResponse

router = APIRouter(route_class=LogRoute)


@router.get(
    '/sales',
    response_model=ShopUnitStatisticResponse,
    responses={
        status.HTTP_200_OK: {
            'description': 'Список товаров, цена которых была обновлена',
            'model': ShopUnitStatisticResponse,
        },
        status.HTTP_400_BAD_REQUEST: HTTP_400_RESPONSE,
    },
)
def get_sales(
    date: datetime, session: Session = Depends(get_session)
) -> Union[ShopUnitStatisticResponse, Error]:
    """
    Получение списка **товаров**, цена которых была обновлена за последние 24 часа включительно [now() - 24h, now()] от времени переданном в запросе.

    - Обновление цены не означает её изменение.

    - Обновления цен удаленных товаров недоступны.

    - При обновлении цены товара, средняя цена категории, которая содержит этот товар, тоже обновляется.

    Output:

    - 200: Список товаров, цена которых была обновлена.

    - 400: Невалидная схема документа или входные данные не верны. Validation Failed
    """
    windows_params = {
        'partition_by': [ShopHistory.id],
        'order_by': ShopHistory.date.desc(),
    }
    subquery = session.query(
        ShopHistory.id,
        ShopHistory.date,
        ShopHistory.price,
        func.row_number().over(**windows_params).label('row_number'),
    ).subquery('t')
    sub2 = (
        session.query(subquery.c.id, subquery.c.date, subquery.c.price)
        .filter(subquery.c.row_number == 1)
        .subquery('t1')
    )
    items = (
        session.query(
            sub2.c.id, sub2.c.date, sub2.c.price, Shop.type, Shop.name
        )
        .filter(
            Shop.id == sub2.c.id,
            Shop.type == ShopUnitType.OFFER,
            sub2.c.date <= date,
            sub2.c.date >= date - timedelta(hours=24),
        )
        .all()
    )
    return ShopUnitStatisticResponse(**{'items': items})
