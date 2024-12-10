from fastapi.responses import HTMLResponse
from fastapi import Request, APIRouter, Depends
from utils.db import get_db
from sqlalchemy.orm import Session

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
                reservations = view_past_reservations(db=db, pid=user_id)
            elif command == "pending":
                appointments = view_future_appointments(db=db, pid=user_id)
                reservations = view_future_reservations(db=db, pid=user_id)

            # 合并 appointments 和 reservations
            combined_records = [
                {**appt.to_dict(), "type": "appointment"} for appt in appointments
            ] + [
                {**res.to_dict(), "type": "reservation"} for res in reservations
            ]

            return {
                "message": f"Here are your {command} records.",
                "records": combined_records,
            }
        elif command == "schedule":
            session['state'] = 'schedule'
            return {"message": "Here is your schedule."}
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
    else:
        return {"message": f"Command `{command}` not valid in the current state."}

    
