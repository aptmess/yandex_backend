from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.routes.log_route import LogRoute
from app.core.engine import get_session
from app.schemas.error import Error
from app.schemas.shop_item import ShopUnit

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
    Получить информацию об элементе по идентификатору.

    - При получении информации о категории также предоставляется информация о её дочерних элементах.

    - Для пустой категории поле children равно пустому массиву, а для товара равно null

    - Цена категории - это средняя цена всех её товаров, включая товары дочерних категорий.

        - Если категория не содержит товаров цена равна null.

        - При обновлении цены товара, средняя цена категории, которая содержит этот товар, тоже обновляется.

    Output:

    - 200: Информация об элементе.

    - 400: Невалидная схема документа или входные данные не верны. "Validation Failed"

    - 404: Категория/товар не найден. "Item not found"
    """
