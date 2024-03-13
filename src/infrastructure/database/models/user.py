from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Text, func

from infrastructure.database.models.base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .referral import Referral


class User(Base):
    __tablename__ = "user"

    login: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    token: Mapped[str] = mapped_column(
        Text, unique=False, nullable=True, server_default="", default=""
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )

    ref_link: Mapped["Referral"] = relationship("Referral", back_populates="user")
