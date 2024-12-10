from fastapi.responses import HTMLResponse
from fastapi import Request, APIRouter, Depends
from utils.db import get_db
from sqlalchemy.orm import Session
from services.appointment_service import *
import requests
from datetime import datetime
from sqlalchemy import func


patient_console_router = APIRouter()

@patient_console_router.post("/execute/patient")
async def execute_patient_command(request: Request, db: Session = Depends(get_db)):
    session = request.session
    user_id = session.get('user_id')
    if not user_id:
        return {"message": "User not logged in. Please log in first."}

    data = await request.json()
    command = data.get("command", "")

    if session['state'] == 'welcome':
        if command in ["record", "pending"]:
            session['state'] = command

            if command == "record":
                appointments = view_past_appointments(db=db, pid=user_id)
            elif command == "pending":
                appointments = view_future_appointments(db=db, pid=user_id)
            elif command == "create":
                return {"message": "Enter the SID for the new appointment."}

            records = [appt.to_dict() for appt in appointments]
            return {"message": f"Here are your {command} records.", "records": records}

        elif command == "create":
            session['state'] = 'create'
            return {"message": "Enter the details of the appointment in the following format:\n" "'pid,sid,date,order,applytime,status,attendance'"}

        elif command == "exit":
            session.clear()
            return {"message": "Goodbye!"}
        else:
            return {"message": f"Unknown command: {command}"}
    elif session['state'] == 'record':
        if command == "back":
            session['state'] = 'welcome'
            return {"message": "Back to main menu."}
        else:
            return {"message": f"Command `{command}` not valid in the current state."}
    elif session['state'] == 'pending':
        if command == "cancel":
            return {"message": "Cancelled"}
        elif command == "back":
            session['state'] = 'welcome'
            return {"message": "Back to main menu."}
        else:
            return {"message": f"Command `{command}` not valid in the current state."}
    #elif session['state'] == 'create':
        

    else:
        session['state'] = 'welcome'
        return {"message": f"Command `{command}` not valid in the current state."}


@patient_console_router.post("/execute/patient")
async def execute_patient_command(request: Request, db: Session = Depends(get_db)):
    session = request.session
    user_id = session.get('user_id')

    if not user_id:
        return {"message": "User not logged in. Please log in first."}

    data = await request.json()
    command = data.get("command", "")

    if command == "create":
        sid = data.get("sid")
        date = data.get("date")
        order = db.query(func.max(Appointment.order)).scalar() or 0
        try:
            appointment_data = {
                "pid": user_id,
                "sid": sid,
                "date": date,
                "order": int(order),
                "applytime": datetime.now().isoformat()

            }
            result = create_appointment(db=db, appointment_data=appointment_data)
            return {"message": f"Appointment created successfully: {result}"}
        except Exception as e:
            return {"message": f"Failed to create appointment: {str(e)}"}

    elif command == "record":
        appointments = view_past_appointments(db=db, pid=user_id)
        records = [appointment.to_dict() for appointment in appointments]
        return {"message": "Here are your past appointments.", "records": records}

    elif command == "pending":
        appointments = view_future_appointments(db=db, pid=user_id)
        records = [appointment.to_dict() for appointment in appointments]
        return {"message": "Here are your pending appointments.", "records": records}

    return {"message": f"Unknown command: {command}"}


    
