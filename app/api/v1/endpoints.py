from fastapi import APIRouter, HTTPException, status
from app.models.campaign import CampaignModel, CampaignUpdateModel
from app.core.database import db_engine
from bson import ObjectId
from datetime import datetime

router = APIRouter()

# Helper tool to convert MongoDB data structures to clean JSON formats
def campaign_helper(campaign) -> dict:
    return {
        "id": str(campaign["_id"]),
        "title": campaign["title"],
        "description": campaign["description"],
        "discount_percentage": campaign["discount_percentage"],
        "target_tier": campaign["target_tier"],
        "is_active": campaign["is_active"],
        "created_at": campaign["created_at"].isoformat() if isinstance(campaign["created_at"], datetime) else campaign["created_at"]
    }

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_marketing_campaign(campaign: CampaignModel):
    new_campaign_dict = campaign.model_dump()
    result = await db_engine.db["campaigns"].insert_one(new_campaign_dict)
    created_campaign = await db_engine.db["campaigns"].find_one({"_id": result.inserted_id})
    return {"message": "Campaign successfully built", "data": campaign_helper(created_campaign)}

@router.get("/")
async def get_all_active_campaigns():
    campaigns = []
    cursor = db_engine.db["campaigns"].find()
    async for document in cursor:
        campaigns.append(campaign_helper(document))
    return {"count": len(campaigns), "campaigns": campaigns}

@router.get("/{campaign_id}")
async def get_campaign_by_id(campaign_id: str):
    if not ObjectId.is_valid(campaign_id):
        raise HTTPException(status_code=400, detail="Invalid MongoDB Hexadecimal identifier layout.")
    
    campaign = await db_engine.db["campaigns"].find_one({"_id": ObjectId(campaign_id)})
    if campaign:
        return campaign_helper(campaign)
    raise HTTPException(status_code=404, detail="Campaign entity target not located.")

@router.put("/{campaign_id}")
async def update_campaign(campaign_id: str, payload: CampaignUpdateModel):
    if not ObjectId.is_valid(campaign_id):
        raise HTTPException(status_code=400, detail="Invalid hex formatting.")
        
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    
    if len(update_data) >= 1:
        update_result = await db_engine.db["campaigns"].update_one(
            {"_id": ObjectId(campaign_id)}, {"$set": update_data}
        )
        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail="No documentation changes processing modifications executed.")

    existing_campaign = await db_engine.db["campaigns"].find_one({"_id": ObjectId(campaign_id)})
    if existing_campaign:
        return campaign_helper(existing_campaign)
    raise HTTPException(status_code=404, detail="Campaign target not located.")

@router.delete("/{campaign_id}", status_code=status.HTTP_200_OK)
async def permanently_purge_campaign(campaign_id: str):
    if not ObjectId.is_valid(campaign_id):
        raise HTTPException(status_code=400, detail="Invalid hex syntax tracking formats.")
        
    delete_result = await db_engine.db["campaigns"].delete_one({"_id": ObjectId(campaign_id)})
    if delete_result.deleted_count == 1:
        return {"message": f"Successfully dropped campaign item identifier: {campaign_id}"}
    raise HTTPException(status_code=404, detail="Campaign entry entity missing.")