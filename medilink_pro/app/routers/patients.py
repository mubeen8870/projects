from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.db import get_db
import json
import os

router = APIRouter(
    prefix="/api/patients",
    tags=["patients"]
)

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data.json")


# ---------------------------
# Helper function for JSON save
# ---------------------------
def save_to_json(new_patient):
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
        else:
            data = {"patients": []}

        data["patients"].append(new_patient)

        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving to JSON: {e}")


# ---------------------------
# CREATE Patient
# ---------------------------
@router.post("/")
async def create_patient(patient: dict):
    db = get_db()
    result = await db["patients"].insert_one(patient)

    patient["_id"] = str(result.inserted_id)
    save_to_json(patient)

    return patient


# ---------------------------
# READ All Patients
# ---------------------------
@router.get("/")
async def get_patients():
    db = get_db()
    patients = []
    async for patient in db["patients"].find():
        patient["_id"] = str(patient["_id"])
        patients.append(patient)
    return patients


# ---------------------------
# READ One Patient
# ---------------------------
@router.get("/{patient_id}")
async def get_patient(patient_id: str):
    db = get_db()
    patient = await db["patients"].find_one({"_id": ObjectId(patient_id)})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    patient["_id"] = str(patient["_id"])
    return patient


# ---------------------------
# UPDATE Patient
# ---------------------------
@router.put("/{patient_id}")
async def update_patient(patient_id: str, update_data: dict):
    db = get_db()
    result = await db["patients"].update_one(
        {"_id": ObjectId(patient_id)},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found")

    updated_patient = await db["patients"].find_one({"_id": ObjectId(patient_id)})
    updated_patient["_id"] = str(updated_patient["_id"])
    return updated_patient


# ---------------------------
# DELETE Patient
# ---------------------------
@router.delete("/{patient_id}")
async def delete_patient(patient_id: str):
    db = get_db()
    result = await db["patients"].delete_one({"_id": ObjectId(patient_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {"message": "Patient deleted successfully"}
