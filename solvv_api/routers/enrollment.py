# solvv_api/routers/enrollments.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from solvv_api.core.database import get_db
from solvv_api.models.enrollment import EnrollmentModel

from solvv_api.services.emails import send_thank_you_email
from solvv_api.models import EnrollmentModel, ParticipantModel


router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

@router.get("/enrollments")
def read_enrollments():
    return {"message": "Enrollment list"}

@router.post("/{enrollment_id}/complete")
async def mark_completed(enrollment_id: int, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(Enrollment).where(Enrollment.id == enrollment_id))
    enrollment = q.scalar_one_or_none()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    if enrollment.completed:
        return {"message": "Already completed"}

    enrollment.completed = True
    enrollment.completed_at = datetime.utcnow()
    await db.commit()
    await db.refresh(enrollment)

    await send_thank_you_email(db, enrollment)
    return {"message": "Marked complete and email sent"}
