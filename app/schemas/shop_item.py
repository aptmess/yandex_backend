from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator

from app.core.utils import check_isoformat_data


def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    return dt.isoformat(
        timespec='milliseconds',
    ).replace('+00:00', 'Z')


class ShopUnitType(Enum):
    OFFER = 'OFFER'
    CATEGORY = 'CATEGORY'


class ShopUnit(BaseModel):
    id: UUID = Field(
        ...,
        description='Уникальный идентфикатор',
        example='3fa85f64-5717-4562-b3fc-2c963f66a333',
    )
    name: str = Field(..., description='Имя категории')
    date: datetime = Field(
        ...,
        description='Время последнего обновления элемента.',
        example='2022-05-28T21:12:01.000Z',
    )
    parentId: Optional[UUID] = Field(
        None,
        description='UUID родительской категории',
        example='3fa85f64-5717-4562-b3fc-2c963f66a333',
    )
    type: ShopUnitType
    price: Optional[int] = Field(
        None,
        description='Целое число, для категории - это средняя цена всех дочерних'
        ' товаров(включая товары подкатегорий). '
        'Если цена является не целым числом, '
        'округляется в меньшую сторону до целого числа. '
        'Если категория не содержит товаров цена равна null.',
    )
    children: Optional[List[ShopUnit]] = Field(
        None,
        description='Список всех дочерних товаров\\категорий. '
        'Для товаров поле равно null.',
    )

    @validator('date')
    def check_date_iso_8601(cls, v):
        return check_isoformat_data(v)

    class Config:
        json_encoders = {datetime: convert_datetime_to_iso_8601_with_z_suffix}


class ShopUnitImport(BaseModel):
    id: UUID = Field(
        ...,
        description='Уникальный идентфикатор',
        example='3fa85f64-5717-4562-b3fc-2c963f66a333',
    )
    name: str = Field(..., description='Имя элемента.')
    parentId: Optional[UUID] = Field(
        None,
        description='UUID родительской категории',
        example='3fa85f64-5717-4562-b3fc-2c963f66a333',
    )
    type: ShopUnitType
    price: Optional[int] = Field(
        None,
        description='Целое число, для категорий поле должно содержать null.',
    )


class ShopUnitImportRequest(BaseModel):
    items: Optional[List[ShopUnitImport]] = Field(
        None, description='Импортируемые элементы'
    )
    updateDate: Optional[datetime] = Field(
        None,
        description='Время обновления добавляемых товаров/категорий.',
        example='2022-05-28T21:12:01.000Z',
    )

    @validator('updateDate')
    def check_date_iso_8601(cls, v):
        return check_isoformat_data(v)
