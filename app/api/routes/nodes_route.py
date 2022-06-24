from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.routes.log_route import LogRoute
from app.core.engine import get_session
from app.core.models import Shop, ShopHistory
from app.core.utils import recursive_nodes, row2dict
from app.exceptions import EXCEPTION_404_NOT_FOUND
from app.schemas.error import Error
from app.schemas.response import HTTP_400_RESPONSE, HTTP_404_RESPONSE
from app.schemas.shop_item import ShopUnit, ShopUnitType

router = APIRouter(route_class=LogRoute)


@router.get(
    '/nodes/{id}',
    response_model=ShopUnit,
    responses={
        status.HTTP_200_OK: {
            'description': 'Информация об элементе',
            'model': ShopUnit,
        },
        status.HTTP_400_BAD_REQUEST: HTTP_400_RESPONSE,
        status.HTTP_404_NOT_FOUND: HTTP_404_RESPONSE,
    },
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

    shop = session.query(Shop).filter_by(id=id).one_or_none()
    if shop is None:
        raise EXCEPTION_404_NOT_FOUND
    if shop.type == ShopUnitType.CATEGORY:
        return recursive_nodes(shop, session, ShopHistory)[0]
    else:
        return row2dict(shop)
