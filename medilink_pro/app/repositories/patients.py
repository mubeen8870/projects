from datetime import datetime
from bson import ObjectId
from ..db import get_db

class PatientsRepository:
    def __init__(self, db, store=None):
        self.collection = db["patients"]
        self.store = store

    async def create(self, data: dict):
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()
        result = await self.collection.insert_one(data)
        data["id"] = str(result.inserted_id)
        return data

    async def list(self, skip: int = 0, limit: int = 50):
        cursor = self.collection.find().skip(skip).limit(limit)
        docs = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            docs.append(doc)
        return docs

    async def get(self, patient_id: str):
        doc = await self.collection.find_one({"_id": ObjectId(patient_id)})
        if not doc:
            return None
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        return doc

    async def update(self, patient_id: str, data: dict):
        data["updated_at"] = datetime.utcnow()
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(patient_id)},
            {"$set": data},
            return_document=True,
        )
        if not result:
            return None
        result["id"] = str(result["_id"])
        del result["_id"]
        return result

    async def delete(self, patient_id: str):
        await self.collection.delete_one({"_id": ObjectId(patient_id)})
        return True
