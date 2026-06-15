from sqlalchemy.orm import Session

from backend import models, schemas


def get_patient(db: Session, patient_id: int) -> models.Patient | None:
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()


def get_patients(db: Session, skip: int = 0, limit: int = 100) -> list[models.Patient]:
    return (
        db.query(models.Patient)
        .order_by(models.Patient.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_patient(
    db: Session, patient: schemas.PatientCreate, remarks: str
) -> models.Patient:
    db_patient = models.Patient(**patient.model_dump(), remarks=remarks)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def update_patient(
    db: Session,
    patient_id: int,
    patient: schemas.PatientUpdate,
    remarks: str,
) -> models.Patient | None:
    db_patient = get_patient(db, patient_id)
    if not db_patient:
        return None

    for field, value in patient.model_dump().items():
        setattr(db_patient, field, value)
    db_patient.remarks = remarks

    db.commit()
    db.refresh(db_patient)
    return db_patient


def delete_patient(db: Session, patient_id: int) -> bool:
    db_patient = get_patient(db, patient_id)
    if not db_patient:
        return False

    db.delete(db_patient)
    db.commit()
    return True
