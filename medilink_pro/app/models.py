from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class MongoModel(BaseModel):
    id: Optional[str] = Field(None, description="Stringified ObjectId")

    class Config:
        from_attributes = True   # instead of orm_mode in Pydantic v2

class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    age: int
    phone: str
    notes: Optional[str] = None

class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    phone: Optional[str] = None
    notes: Optional[str] = None

class Patient(MongoModel, PatientCreate):
    created_at: datetime
    updated_at: datetime
