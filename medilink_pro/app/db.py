from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings
import json
import os

# -----------------------
# MongoDB Connection
# -----------------------
_client: AsyncIOMotorClient | None = None

def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.MONGO_URI, uuidRepresentation="standard")
    return _client

def get_db():
    return get_client()[settings.MONGO_DB]


# -----------------------
# JSON Utilities
# -----------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_FILE = os.path.join(BASE_DIR, "data.json")

def read_json():
    if not os.path.exists(JSON_FILE):
        return []
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def write_json(data):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
