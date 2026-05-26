from fastapi import FastAPI
from app.core.config import settings
from app.core.database import db_engine
from app.api.v1.endpoints import router as campaign_router

app = FastAPI(title=settings.APP_NAME)

@app.on_event("startup")
async def startup_event():
    # Establishes the real connection to Mongo
    await db_engine.connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    # Safely disconnects on stop
    await db_engine.close_mongo_connection()

# Include the newly configured operational endpoint routing matrices
app.include_router(campaign_router, prefix="/api/v1/campaigns", tags=["Marketing Campaigns"])

@app.get("/health")
async def system_health():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "vault_secret_check": settings.GLOBAL_OVERRIDE_SECRET != "",
        "database_connected": db_engine.client is not None
    }