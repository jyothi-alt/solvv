# solvv_api/routers/feedback.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from solvv_api.core.database import get_db
from solvv_api.core.scheduler import scheduler
from solvv_api.models.feedback import FeedbackForm
from solvv_api.models.course import Course
from solvv_api.services.reports import send_admin_feedback_report

router = APIRouter(prefix="/feedback", tags=["Feedback"])

class FeedbackSendPayload:
    # if you want pydantic, define a schema; keeping minimal here
    pass

@router.post("/forms/{course_id}/send")
async def send_feedback_form(course_id: int, admin_email: str, title: str, db: AsyncSession = Depends(get_db)):
    course = (await db.execute(select(Course).where(Course.id == course_id))).scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    form = FeedbackForm(course_id=course_id, title=title, admin_email=admin_email, sent_at=datetime.utcnow())
    db.add(form)
    await db.commit()
    await db.refresh(form)

    # schedule report job after 5 days
    run_at = datetime.utcnow() + timedelta(days=5)
    scheduler.add_job(
        send_admin_feedback_report,
        "date",
        run_date=run_at,
        args=[db, form.id],
        id=f"feedback_report_{form.id}",
        replace_existing=True,
    )
    return {"message": "Feedback sent and report scheduled", "form_id": form.id, "report_at": run_at.isoformat()}
