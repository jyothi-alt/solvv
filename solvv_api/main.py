from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Routers
from solvv_api.routers import enrollment, feedback, client

# Models
from solvv_api.models.participant import ParticipantModel
from solvv_api.models.enrollment import EnrollmentModel
from solvv_api.models.feedback import FeedbackForm, FeedbackResponse
from solvv_api.models.client import ClientModel

# Database & scheduler
from solvv_api.core.database import Base, engine
from solvv_api.core.scheduler import start_scheduler

# Email service
from solvv_api.services.emails import send_thank_you_email

# Exception handlers
from solvv_api.exceptions.handlers import (
    client_not_found_handler,
    client_already_exists_handler,
    invalid_client_type_handler,
    database_connection_handler
)
from solvv_api.exceptions.custom_exceptions import (
    ClientNotFoundException,
    ClientAlreadyExistsException,
    InvalidClientTypeException,
    DatabaseConnectionException
)

# Initialize app
app = FastAPI(title="Solvv API", version="1.0")
templates = Jinja2Templates(directory="templates")

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(enrollment, prefix="/enrollments", tags=["Enrollments"])
app.include_router(feedback, prefix="/feedback", tags=["Feedback"])
app.include_router(client, prefix="/clients", tags=["Clients"])

# Exception handlers
app.add_exception_handler(ClientNotFoundException, client_not_found_handler)
app.add_exception_handler(ClientAlreadyExistsException, client_already_exists_handler)
app.add_exception_handler(InvalidClientTypeException, invalid_client_type_handler)
app.add_exception_handler(DatabaseConnectionException, database_connection_handler)

# Startup tasks
@app.on_event("startup")
async def on_startup():
    start_scheduler()

# Routes
@app.get("/")
def root():
    return {"message": "API is running!"}

@app.get("/thank-you", response_class=HTMLResponse)
async def thank_you(request: Request):
    return templates.TemplateResponse("thank_you.html", {"request": request})

@app.post("/send-email/")
async def send_email(background_tasks: BackgroundTasks, email: str, name: str, course: str):
    link = f"https://example.com/courses/{course.replace(' ', '-').lower()}"
    await send_thank_you_email(background_tasks, email, name, course, link)
    return {"status": "Email sent"}
