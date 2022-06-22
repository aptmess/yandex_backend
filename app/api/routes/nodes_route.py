from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.routes.log_route import LogRoute
from app.core.engine import get_session
from app.schemas.output_schemas import (
    Error,
    ShopUnit,
)

router = APIRouter(route_class=LogRoute)


@router.get(
    '/nodes/{id}',
    response_model=ShopUnit,
    responses={'400': {'model': Error}, '404': {'model': Error}},
)
def get_nodes_id(
    id: UUID, session: Session = Depends(get_session)
) -> Union[ShopUnit, Error]:
    """
    tags:
        - Базовые задачи
    Получить информацию об элементе по идентификатору.
    При получении информации о категории также предоставляется
        информация о её дочерних элементах.

    - для пустой категории поле children равно пустому массиву,
        а для товара равно null
    - цена категории - это средняя цена всех её товаров,
        включая товары дочерних категорий.
        1. Если категория не содержит товаров цена равна null.
        2. При обновлении цены товара, средняя цена категории,
            которая содержит этот товар, тоже обновляется.
    :param session:
    :param id:
    :return:
        "200":
          description: Информация об элементе.
        "400":
          description: Невалидная схема документа или входные данные не верны.
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

