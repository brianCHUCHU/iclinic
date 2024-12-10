from fastapi.responses import HTMLResponse
from fastapi import Request, APIRouter, Depends
from utils.db import get_db
from sqlalchemy.orm import Session
import json
from services.doctor_service import create_or_update_hire
from services.clinicdivision_service import create_clinic_division
from schemas.doctor import DoctorAndHireCreate
from schemas.clinicdivision import ClinicDivisionCreate

clinic_console_router = APIRouter()

@clinic_console_router.post("/execute/clinic")
async def execute_clinic_command(request: Request, db: Session = Depends(get_db)):
    session = request.session
    user_id = session.get('user_id')
    if not user_id:
        return {"message": "User not logged in. Please log in first."}

    data = await request.json()
    command = data.get("command").lower()

    # sent session state to log
    print(f"Session state: {session}")
    
    current_state = session['state']

    # Welcome state
    if current_state == 'welcome':
        if command == 'manage':
            session['state'] = 'manage'
            return {"message": "Select manage option: doctor, schedule, room, division, period, room_schedule, info"}
        elif command == 'appointment':
            session['state'] = 'appointment'
            return {"message": "enable/disable appointment, update queue number"}
        elif command == 'query':
            session['state'] = 'query'
            return {"message": "query patient information"}
        elif command == 'exit':
            session.clear()
            return {"message": "Goodbye!"}
        else:
            return {"message": f"Unknown command: {command}"}
    
    # Appointment state
    elif current_state == 'appointment':
        if command == 'enable':
            return {"message": "enable schedule"}
        elif command == 'disable':
            return {"message": "disable schedule"}
        elif command == 'update':
            return {"message": "update schedule"}
        elif command == 'back':
            session['state'] = 'welcome'
            return {"message": "back to main menu"}
        else:
            return {"message": f"Unknown appointment command: {command}"}
    
    # Manage state
    elif current_state == 'manage':
        if command == 'doctor':
            session['state'] = 'doctor'
            return {"message": "To Add/Update doctor, please enter in json form, columns includes \"{docid, docname, divid, startdate(optional), enddate(optional)}\""}
        elif command == 'schedule':
            session['state'] = 'schedule'
            return {"message": "add schedule"}
        elif command == 'room':
            session['state'] = 'room'
            return {"message": "add room"}
        elif command == 'division':
            session['state'] = 'division'
            return {"message": "add division"}
        elif command == 'info':
            session['state'] = 'info'
            return {"message": "update clinic information"}
        elif command == 'back':
            session['state'] = 'welcome'
            return {"message": "back to main menu"}
        elif command == 'room_schedule':
            session['state'] = 'room_schedule'
            return {"message": "room schedule"}
        elif command == 'period':
            session['state'] = 'period'
            return {"message": "add period"}
        else:
            return {"message": f"Unknown manage command: {command}"}
    
    # Doctor state
    elif current_state == 'doctor':
        if command == 'back':
            session['state'] = 'manage'
            return {"message": "back to manage menu"}
        else:
            command = data.get("command")
            try:
                command = json.loads(command)
            except:
                return {"message": "Please enter in json form, columns includes \"{docid, docname, divid, startdate(optional), enddate(optional)}\""}
            if command.get("docid") and command.get("docname") and command.get("divid"):
                command['cid'] = session['user_id']
                print(f"Command: {command}")
                result = create_or_update_hire(db=db, data=DoctorAndHireCreate(**command))
                if not result:
                    return {"message": "Doctor not added/updated, {}".format(result.json())}
                return {"message": "doctor added/updated successfully", "doctor": result}
            else:
                return {"message": "Please enter in json form, columns includes \"{docid, docname, divid, startdate(optional), enddate(optional)}\""}
    
    # Schedule state
    elif current_state == 'schedule':
        if command == 'add':
            session['state'] = 'add_schedule'
            return {"message": "add schedule"}
        elif command == 'remove':
            return {"message": "remove schedule"}
        elif command == 'back':
            session['state'] = 'manage'
            return {"message": "back to manage menu"}
        else:
            return {"message": f"Unknown schedule command: {command}"}
    
    # Room state
    elif current_state == 'room':
        if command == 'add':
            return {"message": "add room"}
        elif command == 'remove':
            return {"message": "remove room"}
        elif command == 'back':
            session['state'] = 'manage'
            return {"message": "back to manage menu"}
        else:
            return {"message": f"Unknown room command: {command}"}
    
    # Division state
    elif current_state == 'division':
        if command == 'add':
            session['state'] = 'add_division'
            return {"message": "Please enter division id"}
        elif command == 'remove':
            session['state'] = 'remove_division'
            return {"message": "remove division"}
        elif command == 'back':
            session['state'] = 'manage'
            return {"message": "back to manage menu"}
        else:
            return {"message": f"Unknown division command: {command}"}
    elif current_state == 'add_division':
        if command == 'back':
            session['state'] = 'manage'
            return {"message": "back to manage menu"}
        else:
            result = create_clinic_division(db=db, clinic_division=ClinicDivisionCreate(clinic_id=session['user_id'], division_id=command))
            if not result:
                return {"message": "Division not added, {}".format(result.json())}
            return {"message": "division added successfully", "division": result}
    # Info state
    elif current_state == 'info':
        if command == 'update':
            return {"message": "update clinic information"}
        elif command == 'back':
            session['state'] = 'manage'
            return {"message": "back to manage menu"}

    # Room schedule state
    elif current_state == 'room_schedule':
        if command == 'add':
            return {"message": "add room schedule"}
        elif command == 'remove':
            return {"message": "remove room schedule"}
        elif command == 'back':
            session['state'] = 'manage'
            return {"message": "back to manage menu"}

    else:
        return {"message": f"Unknown clinic command: {command}"}
