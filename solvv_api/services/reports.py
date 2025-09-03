# solvv_api/services/reports.py
import io
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi_mail import MessageSchema
from solvv_api.core.mail import fast_mail
from solvv_api.models.feedback import FeedbackForm, FeedbackResponse
from solvv_api.models.course import Course

async def build_feedback_report_xlsx(db: AsyncSession, form_id: int) -> bytes:
    # gather responses
    responses = (await db.execute(
        select(FeedbackResponse).where(FeedbackResponse.form_id == form_id)
    )).scalars().all()

    # flatten to rows (adjust to your response schema)
    rows = []
    for r in responses:
        rows.append({
            "response_id": r.id,
            "participant_id": r.participant_id,
            "submitted_at": r.submitted_at,
            "response_json": r.response_json,
        })
    df = pd.DataFrame(rows or [{"response_id": None, "participant_id": None, "submitted_at": None, "response_json": None}])

    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Feedback")
    buf.seek(0)
    return buf.read()

async def send_admin_feedback_report(db: AsyncSession, form_id: int):
    form = (await db.execute(select(FeedbackForm).where(FeedbackForm.id == form_id))).scalar_one_or_none()
    if not form:
        return

    course = (await db.execute(select(Course).where(Course.id == form.course_id))).scalar_one_or_none()

    # counts
    total_participants = (await db.execute(
        select(func.count()).select_from(FeedbackResponse).where(FeedbackResponse.form_id == form_id)
    )).scalar()

    # You may track "who received form" elsewhere; if not, pass the total from enrollment
    # Here we assume total participants == enrollments for that course:
    # (Adjust query to your schema)
    from solvv_api.models.enrollment import Enrollment
    sent_to = (await db.execute(
        select(func.count()).select_from(Enrollment).where(Enrollment.course_id == form.course_id)
    )).scalar()

    xlsx_bytes = await build_feedback_report_xlsx(db, form_id)

    msg = MessageSchema(
        subject=f"Feedback Report: {form.title}",
        recipients=[form.admin_email],
        body=(
            f"Feedback title: {form.title}\n"
            f"Course: {course.name if course else form.course_id}\n"
            f"Responses: {total_participants} / {sent_to}\n"
        ),
        attachments=[{
            "file": xlsx_bytes,
            "filename": f"feedback_report_{form_id}.xlsx",
            "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        }],
        subtype="plain"
    )
    await fast_mail.send_message(msg)
