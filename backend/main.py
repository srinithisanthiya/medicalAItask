from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from backend import crud, schemas
from backend.database import Base, engine, get_db
from backend.ml_client import MLAPIError, fetch_health_prediction

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MIRA Health Prediction",
    description="Medical Intelligence health prediction application",
    version="1.0.0",
)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
async def serve_frontend():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/patients", response_model=list[schemas.PatientResponse])
def list_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_patients(db, skip=skip, limit=limit)


@app.get("/api/patients/{patient_id}", response_model=schemas.PatientResponse)
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient record not found.")
    return patient


@app.post("/api/patients", response_model=schemas.PatientResponse, status_code=201)
async def create_patient(
    patient: schemas.PatientCreate, db: Session = Depends(get_db)
):
    try:
        remarks = await fetch_health_prediction(
            date_of_birth=patient.date_of_birth,
            glucose=patient.glucose,
            haemoglobin=patient.haemoglobin,
            cholesterol=patient.cholesterol,
        )
    except MLAPIError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return crud.create_patient(db, patient, remarks)


@app.put("/api/patients/{patient_id}", response_model=schemas.PatientResponse)
async def update_patient(
    patient_id: int,
    patient: schemas.PatientUpdate,
    db: Session = Depends(get_db),
):
    try:
        remarks = await fetch_health_prediction(
            date_of_birth=patient.date_of_birth,
            glucose=patient.glucose,
            haemoglobin=patient.haemoglobin,
            cholesterol=patient.cholesterol,

        )
    except MLAPIError as exc:  
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    updated = crud.update_patient(db, patient_id, patient, remarks)
    if not updated:
        raise HTTPException(status_code=404, detail="Patient record not found.")
    return updated


@app.delete("/api/patients/{patient_id}", status_code=204)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_patient(db, patient_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Patient record not found.")
