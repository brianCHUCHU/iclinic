from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi import APIRouter

frontend_router = APIRouter()

@frontend_router.get("/patient_console", response_class=HTMLResponse)
def patient_console():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Patient Console</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            #output { height: 300px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; margin-bottom: 10px; }
            #command { width: 100%; padding: 10px; }
        </style>
    </head>
    <body>
        <h1>Patient Console</h1>
        <div id="output">Welcome to the Patient Console! Type your command below...</div>
        <input id="command" type="text" placeholder="Type your command here and press Enter...">
        <script>
            const output = document.getElementById("output");
            const commandInput = document.getElementById("command");

            commandInput.addEventListener("keypress", async function(event) {
                if (event.key === "Enter") {
                    const command = commandInput.value.trim();
                    if (!command) return;
                    output.innerHTML += `<div>> ${command}</div>`;
                    commandInput.value = "";

                    // 發送命令到後端
                    const response = await fetch("/execute/patient", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ command })
                    });

                    const result = await response.json();
                    output.innerHTML += `<div>${result.message}</div>`;
                    output.scrollTop = output.scrollHeight;
                }
            });
        </script>
    </body>
    </html>
    """)

@frontend_router.get("/clinic_console", response_class=HTMLResponse)
def clinic_console():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Clinic Console</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            #output { height: 300px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; margin-bottom: 10px; }
            #command { width: 100%; padding: 10px; }
        </style>
    </head>
    <body>
        <h1>Clinic Console</h1>
        <div id="output">Welcome to the Clinic Console! Type your command below...</div>
        <input id="command" type="text" placeholder="Type your command here and press Enter...">
        <script>
            const output = document.getElementById("output");
            const commandInput = document.getElementById("command");

            commandInput.addEventListener("keypress", async function(event) {
                if (event.key === "Enter") {
                    const command = commandInput.value.trim();
                    if (!command) return;
                    output.innerHTML += `<div>> ${command}</div>`;
                    commandInput.value = "";

                    // 發送命令到後端
                    const response = await fetch("/execute/clinic", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ command })
                    });

                    const result = await response.json();
                    output.innerHTML += `<div>${result.message}</div>`;
                    output.scrollTop = output.scrollHeight;
                }
            });
        </script>
    </body>
    </html>
    """)


@frontend_router.post("/execute/patient")
async def execute_patient_command(request: Request):
    data = await request.json()
    command = data.get("command")
    
    if command == "get patient info":
        return {"message": "Patient Info: {'name': 'John Doe', 'age': 30, 'history': 'No significant history.'}"}
    elif command == "exit":
        return {"message": "Patient console exiting is not allowed in the web version."}
    else:
        return {"message": f"Unknown patient command: {command}"}

@frontend_router.post("/execute/clinic")
async def execute_clinic_command(request: Request):
    data = await request.json()
    command = data.get("command")
    
    if command == "get clinic info":
        return {"message": "Clinic Info: {'name': 'Sample Clinic', 'location': 'City Center'}"}
    elif command == "exit":
        return {"message": "Clinic console exiting is not allowed in the web version."}
    else:
        return {"message": f"Unknown clinic command: {command}"}

@frontend_router.get("/", response_class=HTMLResponse)
def get_identity_selection_page():
    """返回身份選擇頁面"""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>iClinic Console - Select Identity</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            .button { padding: 10px 20px; margin: 10px; cursor: pointer; font-size: 16px; }
        </style>
    </head>
    <body>
        <h1>Select Identity</h1>
        <div>
            <button class="button" onclick="window.location.href='/login/patient'">Patient</button>
            <button class="button" onclick="window.location.href='/login/clinic'">Clinic</button>
        </div>
    </body>
    </html>
    """)

@frontend_router.get("/login/patient", response_class=HTMLResponse)
async def login_patient_page():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Patient Login</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            .input { padding: 10px; margin: 10px; font-size: 16px; }
            .button { padding: 10px 20px; margin: 10px; cursor: pointer; font-size: 16px; }
        </style>
    </head>
    <body>
        <h1>Patient Login</h1>
        <form id="patient-login-form">
            <input class="input" id="pid" type="text" placeholder="Enter your Patient ID" required>
            <input class="input" id="acctpw" type="password" placeholder="Enter your password" required>
            <button type="button" class="button" onclick="loginPatient()">Login</button>
        </form>
        <script>
            async function loginPatient() {
                const pid = document.getElementById('pid').value;
                const acctpw = document.getElementById('acctpw').value;

                const response = await fetch('/memberships/authenticate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ pid, acctpw })
                });

                if (response.ok) {
                    window.location.href = "/patient_console";
                } else {
                    alert("Invalid credentials!");
                }
            }
        </script>
    </body>
    </html>
    """)

@frontend_router.get("/login/clinic", response_class=HTMLResponse)
async def login_clinic_page():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Clinic Login</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            .input { padding: 10px; margin: 10px; font-size: 16px; }
            .button { padding: 10px 20px; margin: 10px; cursor: pointer; font-size: 16px; }
        </style>
    </head>
    <body>
        <h1>Clinic Login</h1>
        <form id="clinic-login-form">
            <input class="input" id="acct_name" type="text" placeholder="Enter your Clinic Account Name" required>
            <input class="input" id="password" type="password" placeholder="Enter your password" required>
            <button type="button" class="button" onclick="loginClinic()">Login</button>
        </form>
        <script>
            async function loginClinic() {
                const acct_name = document.getElementById('acct_name').value;
                const password = document.getElementById('password').value;

                const response = await fetch('/clinics/authenticate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ acct_name, password })
                });

                if (response.ok) {
                    window.location.href = "/clinic_console";
                } else {
                    alert("Invalid credentials!");
                }
            }
        </script>
    </body>
    </html>
    """)