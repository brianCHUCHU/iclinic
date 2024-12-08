from fastapi import FastAPI
from utils.db import test_db_connection
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

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code for startup
    test_db_connection()  # Ensure the database connection is successful
    yield
    # Code for shutdown (if needed)

@app.get("/")
def read_root():
    return {"Hello": "FastAPI"}

# 確保通過 uvicorn 啟動應用
# 例如： uvicorn main:app --reload


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