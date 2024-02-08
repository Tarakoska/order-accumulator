from sqlalchemy import Column, Text, Enum
from uuid import UUID
from . import Base
from marshmallow import Schema, fields
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class UserSetting(Base):
    __tablename__ = 'user_setting'

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), primary_key=True)
    setting_id: Mapped[int] = mapped_column(ForeignKey("setting.id"), primary_key=True)

    def __repr__():
        return "Menu"

    @property
    def serialized(self):
        return {
            'user_id': self.id,
            'setting_id': self.menu_id
        }
#
# class UserSettingSchema(Schema):
#     user_id = fields.Integer()
#     setting_id = fields.Integer()