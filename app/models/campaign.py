from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class CampaignModel(BaseModel):
    title: str = Field(..., example="Black Friday Flash Discount")
    description: str = Field(..., example="Sitewide category level discount codes")
    discount_percentage: int = Field(..., ge=1, le=100, example=25)
    target_tier: str = Field(..., example="VIP")  # VIP, Retail, B2B wholesale
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CampaignUpdateModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    discount_percentage: Optional[int] = None
    target_tier: Optional[str] = None
    is_active: Optional[bool] = None