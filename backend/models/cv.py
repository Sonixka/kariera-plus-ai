from datetime import datetime

from pydantic import BaseModel


class CVProfile(BaseModel):
    id: int | None = None
    user_id: int
    filename: str
    text: str
    ai_analysis: str
    created_at: str | None = None