from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator

from app.schemas.shop_item import ShopUnitType
from app.core.utils import convert_datetime_to_iso, check_isoformat_data


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
        ...,
        description='Время последнего обновления элемента.',
        example='2022-05-28T21:12:01.000Z'
    )

    @validator('date')
    def check_date_iso_8601(cls, v):
        return check_isoformat_data(v)

    class Config:
        json_encoders = {datetime: convert_datetime_to_iso}


class ShopUnitStatisticResponse(BaseModel):
    items: Optional[List[ShopUnitStatisticUnit]] = Field(
        None, description='История в произвольном порядке.'
    )

    class Config:
        json_encoders = {datetime: convert_datetime_to_iso}
