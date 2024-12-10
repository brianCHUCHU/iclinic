from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi import APIRouter

clinic_console_router = APIRouter()

@clinic_console_router.post("/execute/clinic")
async def execute_clinic_command(request: Request):
    data = await request.json()
    command = data.get("command")
    
    if command == "get clinic info":
        return {"message": "Clinic Info: {'name': 'Sample Clinic', 'location': 'City Center'}"}
    elif command == "exit":
        return {"message": "Clinic console exiting is not allowed in the web version."}
    else:
        return {"message": f"Unknown clinic command: {command}"}