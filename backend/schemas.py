from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class PatientBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120)
    date_of_birth: date
    email: EmailStr
    glucose: float = Field(..., ge=0, le=1000)
    haemoglobin: float = Field(..., ge=0, le=30)
    cholesterol: float = Field(..., ge=0, le=1000)

    @field_validator("date_of_birth")
    @classmethod
    def dob_not_in_future(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("Date of birth cannot be in the future.")
        return value


class PatientCreate(PatientBase):
    pass


class PatientUpdate(PatientBase):
    pass


class PatientResponse(PatientBase):
    id: int
    remarks: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
