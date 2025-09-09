from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.db import get_db
import json
import os

router = APIRouter(
    prefix="/api/medicines",
    tags=["medicines"]
)

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data.json")


# ---------------------------
# Helper function for JSON save
# ---------------------------
def save_to_json(new_medicine):
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
        else:
            data = {"medicines": []}

        if "medicines" not in data:
            data["medicines"] = []

        data["medicines"].append(new_medicine)

        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving to JSON: {e}")


# ---------------------------
# CREATE Medicine
# ---------------------------
@router.post("/")
async def create_medicine(medicine: dict):
    db = get_db()
    result = await db["medicines"].insert_one(medicine)

    medicine["_id"] = str(result.inserted_id)
    save_to_json(medicine)

    return medicine


# ---------------------------
# READ All Medicines
# ---------------------------
@router.get("/")
async def get_medicines():
    db = get_db()
    medicines = []
    async for medicine in db["medicines"].find():
        medicine["_id"] = str(medicine["_id"])
        medicines.append(medicine)
    return medicines


# ---------------------------
# READ One Medicine
# ---------------------------
@router.get("/{medicine_id}")
async def get_medicine(medicine_id: str):
    db = get_db()
    medicine = await db["medicines"].find_one({"_id": ObjectId(medicine_id)})
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    medicine["_id"] = str(medicine["_id"])
    return medicine


# ---------------------------
# UPDATE Medicine
# ---------------------------
@router.put("/{medicine_id}")
async def update_medicine(medicine_id: str, update_data: dict):
    db = get_db()
    result = await db["medicines"].update_one(
        {"_id": ObjectId(medicine_id)},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Medicine not found")

    updated_medicine = await db["medicines"].find_one({"_id": ObjectId(medicine_id)})
    updated_medicine["_id"] = str(updated_medicine["_id"])
    return updated_medicine


# ---------------------------
# DELETE Medicine
# ---------------------------
@router.delete("/{medicine_id}")
async def delete_medicine(medicine_id: str):
    db = get_db()
    result = await db["medicines"].delete_one({"_id": ObjectId(medicine_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Medicine not found")

    return {"message": "Medicine deleted successfully"}
