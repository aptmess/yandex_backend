import datetime
from typing import List

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from app.schemas.shop_item import ShopUnitType

Base: DeclarativeMeta = declarative_base()


class ShopUnit(Base):
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
    parent_id = sa.Column(
        psql.UUID(as_uuid=True),
        sa.ForeignKey('shop_unit.id'),
        index=True,
        default=None,
        nullable=True,
    )

    price = sa.Column(sa.Integer, nullable=True)

    children: List['ShopUnit'] = so.relationship(
        'ShopUnit',
        backref=so.backref('parent', remote_side='ShopUnit.id'),
        uselist=True,
        cascade='all, delete',
    )


#
#
# class Node(Base):
#     __tablename__ = 'node'
#
#     id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
#     parent_id = sa.Column(sa.Integer, nullable=True)
#     updated_at = sa.Column(
#         sa.DateTime, server_default=sa.func.now(), server_onupdate=sa.func.now()
#     )
#
#     __mapper_args__ = {'eager_defaults': True}
#
#     cluster = so.relationship('Cluster')
#
#
# class Cluster(Base):
#     __tablename__ = 'cluster'
#
#     cluster_id = sa.Column(sa.Integer, primary_key=True)
#     description = sa.Column(sa.String, nullable=False)
#     id = sa.Column(sa.Integer, nullable=False)
#
#     category = so.relationship('Category')
#
#     __table_args__ = (
#         sa.ForeignKeyConstraint(('id',), ['node.id'], name='Node__id_fk'),
#     )
#
#
# class Category(Base):
#     """
#     Table for trees
#     """
#
#     __tablename__ = 'category'
#
#     category_id = sa.Column(sa.Integer)
#
#     cluster_id = sa.Column(sa.Integer, nullable=False)
#
#     description = sa.Column(sa.String, nullable=True)
#
#     __table_args__ = (
#         sa.PrimaryKeyConstraint(
#             category_id,
#             cluster_id,
#         ),
#         sa.ForeignKeyConstraint(
#             ('cluster_id',),
#             ['cluster.cluster_id'],
#             name='Cluster__cluster_id_fk',
#         ),
#         sa.Index(
#             'Category__cluster_id_index',
#             cluster_id,
#         ),
#     )
#
#
# class Gender(Base):
#     __tablename__ = 'gender'
#
#     gender_id = sa.Column(sa.CHAR(1), primary_key=True)
#     gender_info = sa.Column(sa.String(length=20), unique=True, nullable=False)
#
#     gender = so.relationship('User')
#
#
# class AgeGroup(Base):
#     __tablename__ = 'age_group'
#
#     age_group_id = sa.Column(sa.CHAR(1), primary_key=True)
#     age_group_info = sa.Column(
#         sa.String(length=20), unique=True, nullable=False
#     )
#
#     age_group = so.relationship('User')
#
#
# class UserRFM(Base):
#     __tablename__ = 'user_rfm'
#
#     user_id = sa.Column(sa.Integer)
#     recency_value = sa.Column(sa.SmallInteger)
#     frequency_value = sa.Column(sa.Float(precision=5))
#     monetary_value = sa.Column(sa.Float(precision=5))
#     updated_at = sa.Column(
#         sa.DateTime, server_default=sa.func.now(), server_onupdate=sa.func.now()
#     )
#
#     __mapper_args__ = {'eager_defaults': True}
#
#     __table_args__ = (
#         sa.PrimaryKeyConstraint(
#             user_id,
#             updated_at,
#         ),
#         # sa.Index(
#         #     'UserRFM__user_id_index',
#         #     user_id,
#         #     updated_at.desc(),
#         # ),
#     )
#
#
# class User(Base):
#
#     __tablename__ = 'user'
#
#     user_id = sa.Column(sa.Integer)
#     gender_id = sa.Column(
#         sa.CHAR(1),
#     )
#     age_group_id = sa.Column(
#         sa.CHAR(1),
#     )
#     updated_at = sa.Column(
#         sa.DateTime, server_default=sa.func.now(), server_onupdate=sa.func.now()
#     )
#
#     __mapper_args__ = {'eager_defaults': True}
#     __table_args__ = (
#         sa.PrimaryKeyConstraint(
#             user_id,
#             updated_at,
#         ),
#         sa.ForeignKeyConstraint(
#             ('gender_id',), ['gender.gender_id'], name='Gender__gender_id_fk'
#         ),
#         sa.ForeignKeyConstraint(
#             ('age_group_id',),
#             ['age_group.age_group_id'],
#             name='AgeGroup__age_group_id_fk',
#         ),
#         # sa.Index(
#         #     'User__user_id_index',
#         #     user_id,
#         #     # updated_at.desc(),
#         # ),
#         # sa.Index(
#         #     'User__(user_id, updated_at_desc)_index',
#         #     user_id,
#         #     updated_at.desc(),
#         # ),
#     )
#
#
# class UserInterest(Base):
#     __tablename__ = 'user_interest'
#
#     # id = sa.Column(
#     #     sa.BigInteger,
#     #     autoincrement=True,
#     #     primary_key=True
#     # )
#     #
#     user_id = sa.Column(sa.Integer)
#     cluster_id = sa.Column(
#         sa.Integer,
#     )
#     updated_at = sa.Column(
#         sa.DateTime,
#         server_default=sa.func.now(),
#         server_onupdate=sa.func.now(),
#     )
#     cluster_value = sa.Column(sa.Float(precision=5))
#
#     __mapper_args__ = {'eager_defaults': True}
#
#     __table_args__ = (
#         sa.PrimaryKeyConstraint(user_id, cluster_id, updated_at),
#         sa.ForeignKeyConstraint(
#             ('cluster_id',),
#             ['cluster.cluster_id'],
#             name='Cluster__cluster_id_fk',
#         ),
#         # sa.Index(
#         #     'UserInterest__(user_id, updated_at_desc)_index',
#         #     user_id,
#         #     updated_at.desc(),
#         # ),
#     )
