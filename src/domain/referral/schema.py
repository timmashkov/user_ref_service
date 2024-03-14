from datetime import date
from uuid import UUID

from pydantic import BaseModel, field_validator


class GetReferralById(BaseModel):
    id: UUID


class ReferralUpd(BaseModel):
    code: str
    exp_date: date


class ReferralIn(ReferralUpd):
    user_id: UUID


class ReferralOut(GetReferralById, ReferralIn):
    created_at: date
    last_time: float

    @field_validator("last_time")
    def show_time(cls, data):
        return int(float(data)) // 3600
