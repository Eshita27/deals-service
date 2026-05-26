from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import logging

logger = logging.getLogger("DealsAPI.Database")

class DatabaseEngine:
    client: AsyncIOMotorClient = None
    db = None

    async def connect_to_mongo(self):
        try:
            logger.info(f"Connecting to MongoDB Instance at {settings.MONGO_URI}...")
            self.client = AsyncIOMotorClient(settings.MONGO_URI)
            self.db = self.client[settings.DATABASE_NAME]
            # Force verification handshake
            await self.client.admin.command('ping')
            logger.info("Successfully established asynchronous handshake with MongoDB!")
        except Exception as e:
            logger.error(f"Critical Database Error: Failed to link to MongoDB: {e}")
            raise e

    async def close_mongo_connection(self):
        if self.client:
            self.client.close()
            logger.info("MongoDB client collection connection pools drained safely.")

db_engine = DatabaseEngine()