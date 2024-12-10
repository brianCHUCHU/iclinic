from fastapi.responses import HTMLResponse
from fastapi import Request, APIRouter, Depends
from utils.db import get_db
from sqlalchemy.orm import Session
import json
from services.doctor_service import create_or_update_hire
from services.clinicdivision_service import create_clinic_division, enable_clinic_division, disable_clinic_division
from services.schedule_service import create_schedule, enable_schedule, disable_schedule
from schemas.doctor import DoctorAndHireCreate
from schemas.clinicdivision import ClinicDivisionCreate, ClinicDivisionUpdate
from schemas.schedule import ScheduleCreate, ScheduleUpdate
from models import Hire, Period, Clinicdivision

clinic_console_router = APIRouter()

@clinic_console_router.post("/execute/clinic")
async def execute_clinic_command(request: Request, db: Session = Depends(get_db)):
    session = request.session
    user_id = session.get('user_id')
    if not user_id:
        return {"message": "User not logged in. Please log in first."}

    data = await request.json()
    command = data.get("command")

    # sent session state to log
    print(f"Session state: {session}")
    
    current_state = session['state']

    # Welcome state
    if current_state == 'welcome':
        if command == 'manage':
            session['state'] = 'manage'
            return {"message": "Select manage option: doctor, schedule, room, division, period, room_schedule, info\n Note: Recommended construction order: division, doctor, room, period, schedule, room_schedule"}
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
    
    
    # Manage state
    elif current_state == 'manage':
        if command == 'doctor':
            session['state'] = 'doctor'
            return {"message": "To Add/Update doctor, please enter in json form, columns includes \"{docid, docname, divid, startdate(optional), enddate(optional)}\""}
        elif command == 'schedule':
            session['state'] = 'schedule'
            return {"message": "Enter schedule command: add, enable, disable"}
        elif command == 'room':
            session['state'] = 'room'
            return {"message": "add room"}
        elif command == 'division':
            session['state'] = 'division'
            return {"message": "Enter division command: add, enable, disable"}
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
            return {"message": "Please enter in json form, columns includes \"{docid, divid, perid}\""}
        elif command == 'enable':
            session['state'] = 'enable_schedule'
            return {"message": "Please enter in json form, columns includes \"{docid, divid, perid}\""}
        elif command == 'disable':
            session['state'] = 'disable_schedule'
            return {"message": "Please enter in json form, columns includes \"{docid, divid, perid}\""}
        elif command == 'back':
            session['state'] = 'manage'
            return {"message": "back to manage menu"}
        else:
            return {"message": f"Unknown schedule command: {command}"}
    
    elif current_state in ['add_schedule', 'enable_schedule', 'disable_schedule']:
        if command == 'back':
            session['state'] = 'manage'
            return {"message": "back to manage menu"}
        else:
            command = json.loads(command)
            if command.get("docid") and command.get("divid") and command.get("perid"):
                if not db.query(Clinicdivision).filter_by(divid=command['divid'], cid=session['user_id']).first():
                    return {"message": "Division not found"}
                if not db.query(Hire).filter_by(docid=command['docid'], cid=session['user_id']).first():
                    return {"message": "Doctor not found"}
                if not db.query(Period).filter_by(perid=command['perid'], cid=session['user_id']).first():
                    return {"message": "Period not found"}
                
                if current_state == 'add_schedule':
                    result = create_schedule(db=db, schedule_data=ScheduleCreate(**command))
                    try:
                        return {"message": "Schedule added successfully", "schedule": result['schedule']}
                    except:
                        return {"message": "Schedule not added, {}, try again".format(result)}
                elif current_state == 'enable_schedule':
                    result = enable_schedule(db=db, data=ScheduleUpdate(**command))
                    try:
                        return {"message": "Schedule enabled successfully", "schedule": result['schedule']}
                    except:
                        return {"message": "Schedule not enabled, {}, try again".format(result)}
                elif current_state == 'disable_schedule':
                    result = disable_schedule(db=db, data=ScheduleUpdate(**command))
                    try:
                        return {"message": "Schedule disabled successfully", "schedule": result['schedule']}
                    except:
                        return {"message": "Schedule not disabled, {}, try again".format(result)}
                    
            else:
                return {"message": "Please enter in json form, columns includes \"{docid, divid, perid}\""}

    
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
        elif command == 'enable':
            session['state'] = 'enable_division'
            return {"message": "Please enter division id"}
        elif command == 'disable':
            session['state'] = 'disable_division'
            return {"message": "Please enter division id"}
        elif command == 'back':
            session['state'] = 'manage'
            return {"message": "back to manage menu"}
        else:
            return {"message": f"Unknown division command: {command}"}

    elif current_state in ['add_division', 'enable_division', 'disable_division']:
        if command == 'back':
            session['state'] = 'manage'
            return {"message": "back to manage menu"}
        else:
            if current_state == 'add_division':
                result = create_clinic_division(db=db, clinic_division_data=ClinicDivisionCreate(cid=session['user_id'], divid=command))
                try:
                    return {"message": "division created successfully", "division": result['clinic_division']}
                except:
                    return {"message": "Division not created {}, please check if division exists".format(result)}
            elif current_state == 'enable_division':
                result = enable_clinic_division(db=db, clinic_division_data=ClinicDivisionUpdate(cid=session['user_id'], divid=command))
                try:
                    return {"message": "division enabled successfully", "division": result['clinic_division']}
                except:
                    return {"message": "Division not enabled {}, please check if division exists".format(result)}
                
            elif current_state == 'disable_division':
                result = disable_clinic_division(db=db, clinic_division_data=ClinicDivisionUpdate(cid=session['user_id'], divid=command))
                try:
                    return {"message": "division disabled successfully", "division": result['clinic_division']}
                except:
                    return {"message": "Division not disabled {}, please check if division exists".format(result)}
            else:
                return {"message": "Please enter division id"}
            

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
