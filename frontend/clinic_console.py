from fastapi.responses import HTMLResponse
from fastapi import Request, APIRouter, Depends
from utils.db import get_db
from sqlalchemy.orm import Session

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
    
    if session['welcome_state']:
        if command == 'manage':
            session['manage_state'] = True
            session['welcome_state'] = False
            session['doctor_state'] = False
            session['schedule_state'] = False
            session['room_state'] = False
            session['division_state'] = False
            session['room_schedule'] = False
            session['info_state'] = False
            return {"message": "start managing"}
        elif command == 'appointment':
            session['appointment_state'] = True
            session['welcome_state'] = False
            return {"message": "enable/disable appointment, update queue number"}
        elif command == 'query':
            session['query_state'] = True
            session['welcome_state'] = False
            return {"message": "query patient information"}
        elif command == 'exit':
            session.clear()
            return {"message": "Goodbye!"}
        else:
            return {"message": f"Unknown command: {command}"}
    elif session['appointment_state']:
        if command == 'enable':
            return {"message": "enable schedule"}
        elif command == 'disable':
            return {"message": "disable schedule"}
        elif command == 'update':
            return {"message": "update schedule"}
        elif command == 'back':
            session['welcome_state'] = True
            session['appointment_state'] = False
            return {"message": "back to main menu"}
        else:
            return {"message": f"Unknown appointment command: {command}"}
    elif session['manage_state']:
        if command == 'doctor':
            session['doctor_state'] = True
            return {"message": "add doctor"}
        elif command == 'schedule':
            session['schedule_state'] = True
            return {"message": "add schedule"}
        elif command == 'room':
            session['room_state'] = True
            return {"message": "add room"}
        elif command == 'division':
            session['division_state'] = True
            return {"message": "add division"}
        elif command == 'info':
            session['info_state'] = True
            return {"message": "update clinic information"}
        elif command == 'back':
            session['welcome_state'] = True
            session['manage_state'] = False
            return {"message": "back to main menu"}
        elif command == 'room_schedule':
            session['room_schedule'] = True
            session['manage_state'] = False
            return {"message": "room schedule"}
        else:
            return {"message": f"Unknown manage command: {command}"}
    elif session['doctor_state']:
        if command == 'add':
            return {"message": "add doctor"}
        elif command == 'remove':
            return {"message": "remove doctor"}
        elif command == 'back':
            session['manage_state'] = True
            session['doctor_state'] = False
            return {"message": "back to manage menu"}
        else:
            return {"message": f"Unknown doctor command: {command}"}
    elif session['schedule_state']:
        if command == 'add':
            return {"message": "add schedule"}
        elif command == 'remove':
            return {"message": "remove schedule"}
        elif command == 'back':
            session['manage_state'] = True
            session['schedule_state'] = False
            return {"message": "back to manage menu"}
        else:
            return {"message": f"Unknown schedule command: {command}"}
    elif session['room_state']:
        if command == 'add':
            return {"message": "add room"}
        elif command == 'remove':
            return {"message": "remove room"}
        elif command == 'back':
            session['manage_state'] = True
            session['room_state'] = False
            return {"message": "back to manage menu"}
        else:
            return {"message": f"Unknown room command: {command}"}
    elif session['division_state']:
        if command == 'add':
            return {"message": "add division"}
        elif command == 'remove':
            return {"message": "remove division"}
        elif command == 'back':
            session['manage_state'] = True
            session['division_state'] = False
            return {"message": "back to manage menu"}
        else:
            return {"message": f"Unknown division command: {command}"}
    elif session['info_state']:
        if command == 'update':
            return {"message": "update clinic information"}
        elif command == 'back':
            session['manage_state'] = True
            session['info_state'] = False
            return {"message": "back to manage menu"}
    elif session['room_schedule']:
        if command == 'add':
            return {"message": "add room schedule"}
        elif command == 'remove':
            return {"message": "remove room schedule"}
        elif command == 'back':
            session['manage_state'] = True
            session['room_schedule'] = False
            return {"message": "back to manage menu"}
    else:
        return {"message": f"Unknown clinic command: {command}"}