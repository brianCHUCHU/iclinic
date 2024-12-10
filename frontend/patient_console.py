from fastapi.responses import HTMLResponse
from fastapi import Request, APIRouter, Depends
from utils.db import get_db
from sqlalchemy.orm import Session
from services.appointment_service import *
import json

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
                records = [  {**appt.to_dict(), "type": "appointment"} for appt in appointments]

                response_data = {
                    "message": f"Here are your {command} records.",
                    "records": [
                        {**record, "date": record["date"].strftime('%Y-%m-%d'), "applytime": record["applytime"].isoformat()}
                        for record in records
                    ],
                }
                return response_data

            elif command == "pending":
                appointments = view_future_appointments(db=db, pid=user_id)

                records = [  {**appt.to_dict(), "type": "appointment"} for appt in appointments]

                response_data = {
                    "message": f"Here are your {command} records.",
                    "records": [
                        {**record, "date": record["date"].strftime('%Y-%m-%d'), "applytime": record["applytime"].isoformat()}
                        for record in records
                    ],
                }
                return response_data
        
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
            command = data.get("command")
            try:
                command = json.loads(command)
            except:
                return {"message": "Please enter in json form, columns includes \"{sid, sid, date}\""}
            return {"message": "Cancelled"}
        elif command == "back":
            session['state'] = 'welcome'
            return {"message": "Back to main menu."}
        else:
            return {"message": f"Command `{command}` not valid in the current state."}
    # elif session['state'] == 'create':
        

    else:
        return {"message": f"Command `{command}` not valid in the current state."}



    
