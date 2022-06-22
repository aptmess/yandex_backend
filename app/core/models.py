import datetime
from typing import List

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from app.schemas.shop_item import ShopUnitType

Base: DeclarativeMeta = declarative_base()


class Shop(Base):
    __tablename__ = 'shop_unit'

    id = sa.Column(
        psql.UUID(as_uuid=True), primary_key=True, index=True, nullable=False
    )
    name = sa.Column(sa.String, nullable=False)
    date = sa.Column(
        sa.DateTime(timezone=datetime.timezone.utc), nullable=False
    )
    type = sa.Column(
        sa.Enum(ShopUnitType, name='type_enum', create_type=False),
        nullable=False,
    )
    parentId = sa.Column(
        psql.UUID(as_uuid=True),
        sa.ForeignKey('shop_unit.id'),
        index=True,
        default=None,
        nullable=True,
    )

    price = sa.Column(
        sa.Integer, sa.CheckConstraint('price >= 0'), nullable=True
    )

    children: List['Shop'] = so.relationship(
        'Shop',
        backref=so.backref('parent', remote_side='Shop.id'),
        uselist=True,
        cascade='all, delete',
    )

    def __init__(self, id, name, date, type, parentId=None, price=None):
        self.id = id
        self.name = name
        self.date = date
        self.type = type
        self.parentId = parentId
        self.price = price
