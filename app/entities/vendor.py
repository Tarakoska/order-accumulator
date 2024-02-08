from enum import Enum as pyenum
from . import Base, session
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from uuid import UUID
from typing import List

class VendorType(pyenum):
    PLUGIN = 'plugin'
    BASIC = 'basic'

    def __str__(self):
        return self.value

class Vendor(Base):
    __tablename__ = 'vendor'

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True, nullable=False)
    name: Mapped[str]
    type: Mapped[VendorType] = mapped_column(default=VendorType.BASIC)

    orders: Mapped[List["Order"]] = relationship(back_populates="vendor")

    def __repr__(self):
        return f"Vendor<id={self.id},name={self.name},type={str(self.type)}>"

    def find_all():
        return session.query(Vendor).all()

    @property
    def serialized(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'type': str(self.type)
        }

# class VendorSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = Vendor
#         load_instance = True