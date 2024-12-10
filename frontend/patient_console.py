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
    command = data.get("command", "").lower()

    if session['welcome_state']:
        if command in ["record", "pending"]:
            session['welcome_state'] = False

            if command == "record":
                session['record_state'] = True
                appointments = view_past_appointments(db=db, pid=user_id)
                reservations = view_past_reservations(db=db, pid=user_id)
            elif command == "pending":
                session['pending_state'] = True
                appointments = view_future_appointments(db=db, pid=user_id)
                reservations = view_future_reservations(db=db, pid=user_id)

            # 合并 appointments 和 reservations
            combined_records = [
                {**appt.model_dump(), "type": "appointment"} for appt in appointments
            ] + [
                {**res.model_dump(), "type": "reservation"} for res in reservations
            ]

            return {
                "message": f"Here are your {command} records.",
                "records": combined_records,
            }
        elif command == "schedule":
            return {"message": "Here is your schedule."}
        elif command == "exit":
            session.clear()
            return {"message": "Goodbye!"}
        else:
            return {"message": f"Unknown command: {command}"}
    elif session['record_state']:
        if command == "back":
            session['welcome_state'] = True
            session['record_state'] = False
            return {"message": "Back to main menu."}
        else:
            return {"message": f"Command `{command}` not valid in the current state."}
    elif session['pending_state']:
        if command == "cancel":
            return {"message": "Cancelled"}
        elif command == "back":
            session['welcome_state'] = True
            session['pending_state'] = False
            return {"message": "Back to main menu."}
        else:
            return {"message": f"Command `{command}` not valid in the current state."}
    else:
        return {"message": f"Command `{command}` not valid in the current state."}

    
