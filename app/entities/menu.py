from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, JSON, func, Sequence, Boolean, select, or_, and_
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.sql import extract
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from datetime import date as d
import enum
from typing import List
from . import Base, session
from uuid import UUID
from .vendor import Vendor
import datetime
import logging

class Frequency(enum.Enum):
    FIX = 'fix'
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    YEARLY = 'yearly'

    def __str__(self):
        return self.value



class Menu(Base):
    __tablename__ = 'menu'


    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    active: Mapped[bool] = mapped_column(Boolean(), default=False)
    date: Mapped[d] = mapped_column(insert_default=func.current_date())
    vendor_id: Mapped[UUID] = mapped_column(ForeignKey("vendor.id"))
    freq_id: Mapped[Frequency] = mapped_column(default=Frequency.FIX)

    items: Mapped[List["MenuItem"]] = relationship(back_populates="menu", order_by="MenuItem.index")

    def __repr__(self):
        return f"Menu<{self.id},name={self.name},date={self.date},vendor_id={self.vendor_id}>"

    def find_vendor_menu(vendor_id, date, menu_freq):
        stmt = select(Menu).where(
            Menu.vendor_id == vendor_id,
            Menu.date == date,
            menu.freq_id == menu_freq
        )
        return session.execute(stmt).scalars().first()

    def find_vendor_all_menu(vendor_id, date):
        stmt = select(Menu).where(
            or_(
                and_(
                    Menu.vendor_id == vendor_id,
                    Menu.date == date
                ),
                and_(
                    Menu.vendor_id == vendor_id,
                    Menu.freq_id == Frequency.FIX
                ),
                and_(
                    Menu.vendor_id == vendor_id,
                    extract("week",Menu.date) == datetime.datetime.strptime(date, "%Y-%m-%d").isocalendar()[1],
                    Menu.freq_id == Frequency.WEEKLY
                ),
                and_(
                    Menu.vendor_id == vendor_id,
                    extract("month",Menu.date) == datetime.datetime.strptime(date, "%Y-%m-%d").month,
                    Menu.freq_id == Frequency.MONTHLY
                ),
                and_(
                    Menu.vendor_id == vendor_id,
                    extract("year",Menu.date) == datetime.datetime.strptime(date, "%Y-%m-%d").year,
                    Menu.freq_id == Frequency.YEARLY
                )
            )
        )

        return session.execute(stmt).scalars().all()

    def find_by_date(date=d.today().strftime('%Y-%m-%d')):
        stmt = select(Menu).where(Menu.me_date == date)
        return session.execute(stmt).scalars().first()

    def find_by_id(menu_id):
        stmt = select(Menu).where(
            Menu.id == menu_id
        )

        return session.execute(stmt).scalars().first()

    def find_all_by_vendor(vendor_id):
        stmt = select(Menu).where(
            Menu.vendor_id == vendor_id
        ).order_by(Menu.date.desc())
        return session.execute(stmt).scalars().all()

    def add(menu):
        session.add(menu)
        session.commit()


    def update(self, name, date):
        self.name = name
        self.date = date
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def fill_menu(vendor_id, date_to_fill, raw_item_list):
        menu = Menu.find_vendor_menu(vendor_id, date_to_fill)
        if menu is None:
            logging.error("Menu to fill not found!")
            return
        # TODO: Handlig items that got out of stock
        for raw_menu_item in raw_item_list:
            found = False
            for item in menu.items:
                if item.name == raw_menu_item['name']:
                    found = True
                    break
            if found:
                continue

            session.add(
                MenuItem(
                    menu_id=menu.id,
                    name=raw_menu_item['name'],
                    link=raw_menu_item['link'],
                    size=raw_menu_item['size'],
                    price=raw_menu_item['price']
                )
            )

    def create_menu(name, vendor, date, freq):
        menu = Menu.find_vendor_menu(vendor,date)
        # TODO: Need to check that date corresponed to the frequency. This currently only works for daily types
        if menu is not None:
            return
        session.add(Menu(name=name, vendor_id=vendor, date=date, freq_id=freq))
        session.commit()

    @property
    def serialized(self):
        from app.vendor_factory import VendorFactory
        return {
            'id': self.id,
            'name': self.name,
            'date': str(self.date),
            'vendor_id': str(self.vendor_id),
            'freq': str(self.freq_id),
            'items': [item.serialized for item in self.items]
        }
