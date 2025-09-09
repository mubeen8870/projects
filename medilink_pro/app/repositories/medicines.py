import json
from bson import ObjectId

class MedicinesRepository:
    def __init__(self, db, json_store):
        self.collection = db["medicines"]
        self.json_store = json_store

    # ---------- Helper to write JSON ----------
    def _save_to_json(self, data):
        try:
            with open(self.json_store, "r") as f:
                all_data = json.load(f)
        except FileNotFoundError:
            all_data = []

        all_data.append(data)

        with open(self.json_store, "w") as f:
            json.dump(all_data, f, indent=4)

    # ---------- Create ----------
    def create_medicine(self, medicine: dict):
        result = self.collection.insert_one(medicine)
        medicine["_id"] = str(result.inserted_id)
        self._save_to_json(medicine)
        return medicine

    # ---------- Read ----------
    def get_medicines(self):
        return [
            {**doc, "_id": str(doc["_id"])}
            for doc in self.collection.find()
        ]

    def get_medicine(self, medicine_id: str):
        doc = self.collection.find_one({"_id": ObjectId(medicine_id)})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    # ---------- Update ----------
    def update_medicine(self, medicine_id: str, updates: dict):
        self.collection.update_one(
            {"_id": ObjectId(medicine_id)},
            {"$set": updates}
        )
        return self.get_medicine(medicine_id)

    # ---------- Delete ----------
    def delete_medicine(self, medicine_id: str):
        self.collection.delete_one({"_id": ObjectId(medicine_id)})
        # optional: also remove from JSON
        return True
