from fastapi.responses import HTMLResponse
from fastapi import Request, APIRouter, Depends
from utils.db import get_db
from sqlalchemy.orm import Session
import json
from services.doctor_service import create_or_update_hire
from services.clinicdivision_service import create_clinic_division, enable_clinic_division, disable_clinic_division
from services.schedule_service import create_schedule, enable_schedule, disable_schedule
from services.room_service import create_room
from services.period_service import create_period
from services.roomschedule_service import create_room_schedule
from schemas.doctor import DoctorAndHireCreate
from schemas.clinicdivision import ClinicDivisionCreate, ClinicDivisionUpdate
from schemas.room import RoomCreate
from schemas.period import PeriodCreate
from schemas.schedule import ScheduleCreate, ScheduleUpdate
from schemas.roomschedule import RoomScheduleCreate, RoomScheduleUpdate
from models import Hire, Period, Clinicdivision, Room, Roomschedule
from datetime import datetime

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
            if session['queue_type'] == 'I':
                session['state'] = 'room_queue'
                return {"message": "enter room_id to update queue"}
            else:
                session['state'] = 'div_queue'
                return {"message": "enter division id to update queue"}
            # return {"message": "enter divid or roomid to update queue"}
        elif command == 'query':
            session['state'] = 'query'
            return {"message": "query patient information"}
        elif command == 'exit':
            session.clear()
            return {"message": "Goodbye!"}
        else:
            return {"message": f"Unknown command: {command}"}
    
    elif current_state == 'div_queue':
        if command == 'back':
            session['state'] = 'welcome'
            return {"message": "back to main menu"}
        else:
            try:
                # add for share lock
                result = db.query(Clinicdivision).filter_by(divid=command, cid=session['user_id']).first()
                # update queue number and last update
                result.queuenumber += 1
                result.last_update = datetime.now()
                db.commit()
                db.refresh(result)
                return {"message": "Queue updated successfully", "division": result}
            except:
                return {"message": "Division not found, please check division id"}
            return {"message": f"Unknown appointment command: {command}"}

    elif current_state == 'room_queue':
        if command == 'back':
            session['state'] = 'welcome'
            return {"message": "back to main menu"}
        try:
            result = db.query(Room).filter_by(rid=command, cid=session['user_id']).first()
            # update queue number and last update
            result.queuenumber += 1
            result.last_update = datetime.now()
            db.commit()
            db.refresh(result)
            return {"message": "Queue number updated successfully".format(result.queuenumber), "result": result}
        except Exception as e:
            return {"message": f"Failed to update queue number: {str(e)}"}

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
            return {"message": "Enter room command: add, update_roomname, enable, disable"}
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
            return {"message": "Enter room schedule command: add, enable, disable"}
        elif command == 'period':
            session['state'] = 'period'
            return {"message": "Enter period command: add, enable, disable"}
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
            session['state'] = 'add_room'
            return {"message": "Please provide room name."}
        elif command == 'update_roomname':
            session['state'] = 'update_roomname'
            return {"message": "Please provide room update details in JSON format with fields {rid, rname}."}
        elif command == 'enable':
            session['state'] = 'enable_room'
            return {"message": "Please enter room id."}
        elif command == 'disable':
            session['state'] = 'disable_room'
            return {"message": "Please enter room id."}
        elif command == 'back':
            session['state'] = 'manage'
            return {"message": "Back to manage menu."}
        else:
            return {"message": f"Unknown room command: {command}"}


    # Add room
    elif current_state == 'add_room':
        if command == 'back':
            session['state'] = 'manage'
            return {"message": "back to manage menu"}
        try:
            room_data = RoomCreate(cid=session['user_id'], rname=command, available=True)
            result = create_room(db, room_data)
            return {"message": "Room added successfully.", "result": result}
        except Exception as e:
            return {"message": f"Failed to add room: {str(e)}"}
       
    # Update room
    elif current_state in ['enable_room', 'disable_room']:
        if command == 'back':
            session['state'] = 'manage'
            return {"message": "back to manage menu"}
        try:
            room = db.query(Room).filter_by(rid=command, cid=session['user_id']).first()
            room.available = True if current_state == 'enable_room' else False
            db.commit()
            db.refresh(room)
            return {"message": f"{current_state} successfully.", "result": room}
        except Exception as e:
            return {"message": f"Failed to {current_state} room: {str(e)}"}
            
    elif current_state == 'update_roomname':
        if command == 'back':
            session['state'] = 'manage'
            return {"message": "back to manage menu"}
        command = json.loads(command)
        try:
            room = db.query(Room).filter_by(rid=command['rid'], cid=session['user_id']).first()
            room.rname = command['rname']
            return {"message": "Room updated successfully.", "result": room}
        except Exception as e:
            return {"message": f"Failed to update room: {str(e)}"}


    
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
            session['state'] = 'add_room_schedule'
            return {"message": "Please enter room schedule details in JSON form, fields include {sid, rid}."}
        elif command == 'enable':
            session['state'] = 'enable_room_schedule'
            return {"message": "Please provide schedule id."}
        elif command == 'disable':
            session['state'] = 'disable_room_schedule'
            return {"message": "Please provide schedule id."}
        elif command == 'back':
            session['state'] = 'manage'
            return {"message": "Back to manage menu."}
        else:
            return {"message": f"Unknown room schedule command: {command}"}


    # Add room schedule
    elif current_state == 'add_room_schedule':
        try:
            try:
                command = json.loads(command)
            except:
                return {"message": "Please enter in JSON form, fields include {sid, rid}."}


            # Check for required fields
            if not command.get("sid") or not command.get("rid"):
                return {"message": "Missing required fields: {sid, rid}. Please provide valid data."}


            # Add room schedule logic
            command['cid'] = session['user_id']
            room_schedule = create_room_schedule(db=db, room_schedule_data=RoomScheduleCreate(**command))
            session['state'] = 'room_schedule'
            return {"message": "Room schedule added successfully.", "result": room_schedule}


        except Exception as e:
            return {"message": f"Failed to add room schedule: {str(e)}"}


    # Enable or disable room schedule
    elif current_state in ['enable_room_schedule', 'disable_room_schedule']:
        if command == 'back':
            session['state'] = 'manage'
            return {"message": "Back to manage menu."}


        try:

            # Enable/disable room schedule logic
            sid = command
            schedule = db.query(Roomschedule).filter_by(sid=sid, cid=session['user_id']).first()
            if not schedule:
                return {"message": "Room schedule not found."}
            schedule.available = True if current_state == 'enable_room_schedule' else False
            db.commit()
            db.refresh(schedule)
            session['state'] = 'room_schedule'
            return {"message": f"Room schedule {current_state.split('_')[0]}d successfully.", "result": schedule}


        except Exception as e:
            return {"message": f"Failed to {current_state.split('_')[0]} room schedule: {str(e)}"}
    
    elif current_state == 'period':
        if command == 'add':
            session['state'] = 'add_period'
            return {"message": "Please enter in json form, columns includes \"{weekday, starttime, endtime}\""}
        elif command == 'back':
            session['state'] = 'manage'
            return {"message": "back to manage menu"}
        elif command == 'enable':
            session['state'] = 'enable_period'
            return {"message": "Please enter period id"}
        elif command == 'disable':
            session['state'] = 'disable_period'
            return {"message": "Please enter period id"}

    elif current_state in ['enable_period', 'disable_period']:
        if command == 'back':
            session['state'] = 'manage'
            return {"message": "back to manage menu"}
        else:
            try:
                period = db.query(Period).filter_by(perid=command, cid=session['user_id']).first()
                period.available = True if current_state == 'enable' else False
                db.commit()
                db.refresh(period)
                return {"message": f"{current_state} successfully.", "result": period}
            except Exception as e:
                return {"message": f"Failed to {current_state} period: {str(e)}"}
    elif current_state == 'add_period':
        if command == 'back':
            session['state'] = 'manage'
            return {"message": "back to manage menu"}
        try:
            command = json.loads(command)
            period = PeriodCreate(cid=session['user_id'], weekday=command['weekday'], starttime=command['starttime'], endtime=command['endtime'], available=True)
            period = create_period(db, period)
            return {"message": "Period added successfully.", "result": period}
        except Exception as e:
            return {"message": f"Failed to add period: {str(e)}"}

    elif command == 'exit':
        session.clear()
        return {"message": "Goodbye!"}

    else:
        return {"message": f"Unknown clinic command: {command}"}

