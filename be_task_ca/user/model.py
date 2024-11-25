from dataclasses import dataclass
from typing import List
import uuid

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from be_task_ca.database import Base
from be_task_ca.item.model import Item


@dataclass
class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4(),
        index=True,
    )
    email: Mapped[str] = mapped_column(unique=True, index=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    hashed_password: Mapped[str]
    shipping_address: Mapped[str] = mapped_column(default=None)
    cart_items: Mapped[List["CartItem"]] = relationship()


@dataclass
class CartItem(Base):
    __tablename__ = "cart_items"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(f"{User.__tablename__}.id"), primary_key=True, index=True
    )
    item_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(f"{Item.__tablename__}.id"), primary_key=True
    )
    quantity: Mapped[int]
