from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CampaignModel(BaseModel):
    title: str = Field(..., example="Black Friday Flash Discount")
    description: str = Field(..., example="Sitewide category level discount codes")
    # Changed type from int to float to safely handle fractional percentages
    discount_percentage: float = Field(..., ge=1.0, le=100.0, example=25.5)
    target_tier: str = Field(..., example="VIP")  # VIP, Retail, B2B wholesale
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CampaignUpdateModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    # Changed type from Optional[int] to Optional[float] here as well
    discount_percentage: Optional[float] = None
    target_tier: Optional[str] = None
    is_active: Optional[bool] = None