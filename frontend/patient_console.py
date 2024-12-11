from fastapi.responses import HTMLResponse
from fastapi import Request, APIRouter, Depends
from utils.db import get_db
from sqlalchemy.orm import Session
from services.appointment_service import *
import requests
from models import Appointment, Schedule, Period
import json
import datetime


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
                    "message": f"Here are your {command} records. If you want to cancel, please enter in json format, columns includes \"sid, date\"",
                    "records": [
                        {**record, "date": record["date"].strftime('%Y-%m-%d'), "applytime": record["applytime"].isoformat()}
                        for record in records
                    ],
                }
                session['state'] = 'cancel'
                return response_data
        
        elif command == "create":
            session['state'] = 'create'
            return {"message": "Enter in json format, enter {sid, date} to create an appointment."}

        elif command == "exit":
            session.clear()
            return {"message": "Goodbye!"}
        else:
            return {"message": f"Unknown command: {command}"}
    elif command == "exit":
        session.clear()
        return {"message": "Goodbye!"}
    elif session['state'] == 'record':
        if command == "back":
            session['state'] = 'welcome'
            return {"message": "Back to main menu."}
        else:
            return {"message": f"Command `{command}` not valid in the current state."}
    elif session['state'] == 'cancel':
        if command == "back":
            session['state'] = 'welcome'
            return {"message": "Back to main menu."}
        else:
            try:
                command = json.loads(command)
            except json.JSONDecodeError:
                return {"message": "Invalid JSON format. Please provide valid input."}
            
            try:
                command['date'] = datetime.datetime.strptime(command['date'], '%Y-%m-%d')
            except ValueError:
                return {"message": "Invalid date format. Please use 'YYYY-MM-DD'."}

            try:
                appointment = db.query(Appointment).filter(
                    Appointment.sid == command['sid'],
                    Appointment.date == command['date'],
                    Appointment.pid == session['user_id']
                ).first()
                if not appointment:
                    return {"message": "No such appointment found. Please try again with a valid appointment ID."}
                appointment.status = "C"
                db.commit()
                db.refresh(appointment)
                return {"message": "Appointment cancelled successfully."}
            except:
                db.rollback()
                return {"message": "Please enter in json form, columns includes \"{sid, date}\""}
            return {"message": "Cancelled"}

    elif session['state'] == 'create':
        if command == "back":
            session['state'] = 'welcome'
            return {"message": "Back to main menu."}

        # 解析 command
        try:
            command = json.loads(command)
        except json.JSONDecodeError:
            return {"message": "Invalid JSON format. Please provide valid input."}

        # 查询 Schedule
        schedule = db.query(Schedule).filter(Schedule.sid == command['sid']).first()
        if not schedule:
            return {"message": "No such schedule found. Please try again with a valid schedule ID."}

        # 查询 Period
        period = db.query(Period).filter(Period.perid == schedule.perid).first()
        if not period:
            return {"message": "No such period found. Please check the schedule details."}

        # 解析日期并匹配
        try:
            command['date'] = datetime.datetime.strptime(command['date'], '%Y-%m-%d')
        except ValueError:
            return {"message": "Invalid date format. Please use 'YYYY-MM-DD'."}

        if (period.weekday - 1) != command['date'].weekday():
            return {"message": "The date does not match the schedule's weekday."}

        # 准备数据
        input_data = {
            "pid": session['user_id'],
            "sid": command['sid'],
            "date": command['date'],
            "status": "P",
            "attendance": 0,
            "applytime": datetime.datetime.now()
        }

        # 数据库事务
        try:
            appointments = db.query(Appointment).filter(
                Appointment.date == input_data['date'],
                Appointment.sid == input_data['sid']
            ).with_for_update().all()
            input_data['order'] = len(appointments) + 1

            new_appointment = Appointment(**input_data)
            db.add(new_appointment)
            db.commit()
            db.refresh(new_appointment)
            return {"message": "Appointment created successfully.", "appointment": new_appointment}
        except SQLAlchemyError as e:
            db.rollback()
            return {"message": f"Database error: {str(e)}"}
        except Exception as e:
            return {"message": f"Unexpected error: {str(e)}"}

    else:
        return {"message": f"Command `{command}` not valid in the current state."}



    
