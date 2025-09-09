import json, os, asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..config import settings
from ..utils.json_store import JsonStore

def _now():
    return datetime.utcnow()

def _stringify_id(doc: dict) -> dict:
    if doc is None:
        return doc
    if "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc

class BaseRepository:
    def __init__(self, db: AsyncIOMotorDatabase, collection: str, json_store: JsonStore):
        self.col = db[collection]
        self.json_store = json_store
        self.json_key = collection

    async def create(self, data: dict) -> dict:
        data["created_at"] = _now()
        data["updated_at"] = _now()
        res = await self.col.insert_one(data.copy())
        doc = await self.col.find_one({"_id": res.inserted_id})
        # Mirror to JSON
        await self.json_store.upsert(self.json_key, str(res.inserted_id), _stringify_id(doc.copy()))
        return _stringify_id(doc)

    async def get(self, id: str) -> Optional[dict]:
        doc = await self.col.find_one({"_id": ObjectId(id)})
        return _stringify_id(doc)

    async def list(self, skip: int = 0, limit: int = 50) -> List[dict]:
        cursor = self.col.find({}).skip(skip).limit(limit).sort("created_at", -1)
        items = [_stringify_id(d) async for d in cursor]
        return items

    async def update(self, id: str, data: dict) -> Optional[dict]:
        data["updated_at"] = _now()
        await self.col.update_one({"_id": ObjectId(id)}, {"$set": data})
        doc = await self.col.find_one({"_id": ObjectId(id)})
        if doc:
            await self.json_store.upsert(self.json_key, id, _stringify_id(doc.copy()))
        return _stringify_id(doc) if doc else None

    async def delete(self, id: str) -> bool:
        await self.col.delete_one({"_id": ObjectId(id)})
        await self.json_store.delete(self.json_key, id)
        return True
