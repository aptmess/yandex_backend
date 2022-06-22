from datetime import datetime
from typing import Optional, Union
from uuid import UUID

from fastapi import APIRouter, Query

from app.api.routes.log_route import LogRoute
from app.schemas.output_schemas import (
    Error,
    ShopUnitStatisticResponse,
)

router = APIRouter(route_class=LogRoute)


@router.get(
    '/node/{id}/statistic',
    response_model=ShopUnitStatisticResponse,
    responses={'400': {'model': Error}, '404': {'model': Error}},
)
def get_node_id_statistic(
    id: UUID,
    date_start: Optional[datetime] = Query(None, alias='dateStart'),
    date_end: Optional[datetime] = Query(None, alias='dateEnd'),
) -> Union[ShopUnitStatisticResponse, Error]:
    """
    tags:
        - Дополнительные задачи

    Получение статистики (истории обновлений)
        по товару/категории за заданный полуинтервал [from, to).
    Статистика по удаленным элементам недоступна.

        - цена категории - это средняя цена всех её товаров,
              включая товары дочерних категорий.
          Если категория не содержит товаров цена равна null.
          При обновлении цены товара, средняя цена категории,
              которая содержит этот товар, тоже обновляется.
        - можно получить статистику за всё время.

    :param id:
    :param date_start:
    :param date_end:
    :return:
        "200":
          description: Статистика по элементу.
        "400":
          description: Некорректный формат запроса или некорректные даты интервала.
            {
                "code": 400,
                "message": "Validation Failed"
            }
        "404":
          description: Категория/товар не найден.
            {
                "code": 404,
                "message": "Item not found"
            }
    """
