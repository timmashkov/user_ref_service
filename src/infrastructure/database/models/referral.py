from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Text, func, Date, Boolean, ForeignKey

from infrastructure.database.models.base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .user import User


class Referral(Base):
    __tablename__ = "referral"

    code: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    exp_date: Mapped[Date] = mapped_column(Date, unique=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="ref_link",
        cascade="all, delete-orphan",
        passive_updates=True,
        passive_deletes=True,
        single_parent=True,
    )
