from pydantic import BaseModel, EmailStr
from typing import Optional, List


class NotificationRequest(BaseModel):
    user_id: int
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    telegram_id: Optional[str] = None
    message: str
    channels_priority: List[str] = ["telegram", "email", "sms"]
