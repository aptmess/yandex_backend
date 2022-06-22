from __future__ import annotations

from datetime import datetime

from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


from app.schemas.shop_item_schemas import ShopUnitType


class ShopUnitStatisticUnit(BaseModel):
    id: UUID = Field(
        ...,
        description='Уникальный идентфикатор',
        example='3fa85f64-5717-4562-b3fc-2c963f66a333',
    )
    name: str = Field(..., description='Имя элемента')
    parentId: Optional[UUID] = Field(
        None,
        description='UUID родительской категории',
        example='3fa85f64-5717-4562-b3fc-2c963f66a333',
    )
    type: ShopUnitType
    price: Optional[int] = Field(
        None,
        description='Целое число, для категории - это средняя цена всех дочерних'
        ' товаров(включая товары подкатегорий). Если цена является '
        'не целым числом, округляется в меньшую сторону до целого '
        'числа. Если категория не содержит товаров цена равна null.',
    )
    date: datetime = Field(
        ..., description='Время последнего обновления элемента.'
    )


class ShopUnitStatisticResponse(BaseModel):
    items: Optional[List[ShopUnitStatisticUnit]] = Field(
        None, description='История в произвольном порядке.'
    )
