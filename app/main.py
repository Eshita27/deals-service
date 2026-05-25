from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import logging

# Configure logging layout
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DealsAPI")

app = FastAPI(title=settings.APP_NAME)

# Shared asynchronous database client reference
db_client: AsyncIOMotorClient = None

@app.on_event("startup")
async def startup_db_client():
    global db_client
    try:
        logger.info(f"Connecting to MongoDB target: {settings.MONGO_URI}")
        db_client = AsyncIOMotorClient(settings.MONGO_URI)
        # Trigger a quick admin command to force-verify active server connectivity
        await db_client.admin.command('ping')
        logger.info("Successfully established handshake with MongoDB database layer!")
    except Exception as e:
        logger.error(f"Critical Error: Failed to connect to MongoDB: {e}")

@app.on_event("shutdown")
async def shutdown_db_client():
    global db_client
    if db_client:
        db_client.close()
        logger.info("MongoDB client collection pools drained and closed safely.")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "database_connected": db_client is not None
    }