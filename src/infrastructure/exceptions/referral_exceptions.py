from infrastructure.exceptions.base import BaseAPIException

from fastapi import status


class ReferralNotFound(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Referral not found"


class ReferralAlreadyExist(BaseAPIException):
    status_code = status.HTTP_403_FORBIDDEN
    message = "Referral already exist"
