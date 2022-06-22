from datetime import datetime
from typing import Union

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.routes.log_route import LogRoute
from app.core.engine import get_session
from app.schemas.output_schemas import Error, ShopUnitStatisticResponse

router = APIRouter(route_class=LogRoute)


@router.get(
    '/sales',
    response_model=ShopUnitStatisticResponse,
    responses={'400': {'model': Error}},
)
def get_sales(
    date: datetime, session: Session = Depends(get_session)
) -> Union[ShopUnitStatisticResponse, Error]:
    """
    tags:
        - Дополнительные задачи
    Получение списка **товаров**, цена которых была обновлена за последние 24
        часа включительно [now() - 24h, now()] от времени переданном в запросе.
    Обновление цены не означает её изменение.
    Обновления цен удаленных товаров недоступны.
    При обновлении цены товара, средняя цена категории,
        которая содержит этот товар, тоже обновляется.
    :param session:
    :param date:
    :return:
        "200":
            description: Список товаров, цена которых была обновлена.
        "400":
            description: Невалидная схема документа или входные данные не верны.
    """
