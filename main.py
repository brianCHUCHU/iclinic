from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
# import middleware for session handling
from starlette.middleware.sessions import SessionMiddleware
from utils.db import test_db_connection
import os
from secrets import token_hex   
# import all routers in routes/
from routes.clinic_routes import clinic_router
from routes.division_routes import division_router 
from routes.room_routes import room_router
from routes.doctor_routes import doctor_router
from routes.patient_routes import patient_router
from routes.treatment_routes import treatment_router
from routes.period_routes import period_router
from routes.schedule_routes import schedule_router
from routes.appointment_routes import appointment_router
from routes.reservation_routes import reservation_router
from routes.membership_routes import membership_router
from routes.roomschedule_routes import roomschedule_router
from routes.clinicdivision_routes import clinicdivision_router
from contextlib import asynccontextmanager
import asyncio
from frontend.base import frontend_router
from frontend.patient_console import patient_console_router
from frontend.clinic_console import clinic_console_router
from fastapi.templating import Jinja2Templates
from pathlib import Path
from pydantic import BaseModel

app = FastAPI()

# Middleware for session handling
# secret_key = os.getenv("SECRET_KEY", token_hex(32))
secret_key = os.getenv("SECRET_KEY", 'default_secret_key')
app.add_middleware(SessionMiddleware, secret_key=secret_key)

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Code for startup
#     test_db_connection()  # Ensure the database connection is successful
#     yield
#     # Code for shutdown (if needed)


# 確保通過 uvicorn 啟動應用
# 例如： uvicorn main:app --reload

# templates = Jinja2Templates(directory=Path(__file__).parent / "frontend/templates")


# Include routes for clinics
app.include_router(clinic_router)
app.include_router(room_router)
app.include_router(doctor_router)
app.include_router(patient_router)
app.include_router(division_router)
app.include_router(treatment_router)
app.include_router(period_router)
app.include_router(schedule_router)
app.include_router(appointment_router)
app.include_router(reservation_router)
app.include_router(membership_router)
app.include_router(roomschedule_router)
app.include_router(clinicdivision_router)
app.include_router(frontend_router)
app.include_router(patient_console_router)
app.include_router(clinic_console_router)
