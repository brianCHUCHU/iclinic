from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi import APIRouter

patient_console_router = APIRouter()

@patient_console_router.post("/execute/patient")
async def execute_patient_command(request: Request):
    data = await request.json()
    command = data.get("command")
    command = command.lower()
    if command == "schedule":
        return {"message": "Enter \"\""}
    elif command == "record":
        return {"message": "Patient console exiting is not allowed in the web version."}
    else:
        return {"message": f"Unknown patient command: {command}"}