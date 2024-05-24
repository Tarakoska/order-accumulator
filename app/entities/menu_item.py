from sqlalchemy import Column, Text, Enum
from uuid import UUID
from . import Base, session
from marshmallow import Schema, fields
import enum
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class MenuItem(Base):
    __tablename__ = 'menu_item'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    menu_id: Mapped[int] = mapped_column(ForeignKey("menu.id"))
    name: Mapped[str]
    link: Mapped[str]
    size: Mapped[str]
    price: Mapped[int]

    orders: Mapped[List["UserBasket"]] = relationship(back_populates="item")
    menu: Mapped["Menu"] = relationship(back_populates="items")

    def __repr__(self):
        return f"MenuItem<{self.id},menu_id={self.menu_id},size={self.size},price={self.price}>"

    def find_all_by_menu(menu_id):
        return session.query(MenuItem).filter_by(menu_id = menu_id).all()


    def add(item):
        session.add(item)
        session.commit()
        session.close()


    @property
    def serialized(self):
        return {
            'id': self.id,
            'name': self.name,
            'size': self.size,
            'price': self.price
        }
