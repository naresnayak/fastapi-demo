from motor.motor_asyncio import AsyncIOMotorClient

# Use 'mongodb' as the hostname because that will be the service name in Docker
MONGODB_URL = "mongodb://mongodb:27017"
client = AsyncIOMotorClient(MONGODB_URL)
db = client.collegedb