from datetime import date

from pydantic import BaseModel, Field, field_validator


class PredictionRequest(BaseModel):
    date_of_birth: date
    glucose: float = Field(..., ge=0, le=1000)
    haemoglobin: float = Field(..., ge=0, le=30)
    cholesterol: float = Field(..., ge=0, le=1000)

    @field_validator("date_of_birth")
    @classmethod
    def dob_not_in_future(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("Date of birth cannot be in the future.")
        return value


class PredictionResponse(BaseModel):
    remarks: str
    risk_level: str
    confidence: float
