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
            #records { border: 1px solid #ccc; padding: 10px; margin-top: 10px; display: none; }
            #command { width: 100%; padding: 10px; }
            .record-item { cursor: pointer; margin: 5px 0; padding: 5px; border: 1px solid #ddd; }
            .record-item:hover { background-color: #f0f0f0; }
            #back-btn { margin-top: 10px; display: none; }
        </style>
    </head>
    <body>
        <h1>Patient Console</h1>
        <div id="output">
            Welcome to the Patient Console!<br>
            Enter to Select Function:<br><br>
            Type "create" to Create an Appointment<br>
            Type "pending" to View/Cancel/Update Your Scheduled Appointments<br>
            Type "record" to View Your Past Appointments
        </div>
        <div id="records"></div>
        <button id="back-btn">Back to Console</button>
        <input id="command" type="text" placeholder="Type your command here and press Enter...">
        <script>
            const output = document.getElementById("output");
            const recordsDiv = document.getElementById("records");
            const commandInput = document.getElementById("command");
            const backBtn = document.getElementById("back-btn");

            let state = "welcome"; // 用戶當前狀態

            commandInput.addEventListener("keypress", async function (event) {
                if (event.key === "Enter") {
                    const command = commandInput.value.trim();
                    if (!command) return;
                    output.innerHTML += `<div>> ${command}</div>`;
                    commandInput.value = "";

                    if (state === "create") {
                        // 收集用戶輸入的 appointment 資料
                        const sid = command;
                        const date = prompt("Enter the appointment date (YYYY-MM-DD):");

                        // 發送創建請求
                        const response = await fetch("/execute/patient", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ command: "create", sid, date, order }),
                        });
                        const result = await response.json();
                        output.innerHTML += `<div>${result.message}</div>`;
                        state = "welcome"; // 重置狀態
                    } else {
                        // 發送一般指令到後端
                        const response = await fetch("/execute/patient", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ command }),
                        });

                        const result = await response.json();
                        output.innerHTML += `<div>${result.message}</div>`;
                        output.scrollTop = output.scrollHeight;

                        // 如果進入創建模式
                        if (command === "create") {
                            state = "create";
                            output.innerHTML += `<div>Please enter the SID for the new appointment:</div>`;
                        }

                        // 顯示記錄
                        if (result.records) {
                            recordsDiv.style.display = "block";
                            recordsDiv.innerHTML = "<h3>Your Records:</h3>";
                            result.records.forEach((record) => {
                                const recordDiv = document.createElement("div");
                                let recordDetails = Object.entries(record)
                                    .map(([key, value]) => `${key}: ${value}`)
                                    .join("<br>");
                                recordDiv.innerHTML = `${recordDetails}<hr>`;
                                recordsDiv.appendChild(recordDiv);  
                            });
                        }
                    }
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
        <div id="output">
            Welcome to the Clinic Console!<br>
            Enter to Select Function:<br><br>
            Type "manage" to Manage your Doctors/Rooms/Schedules/Divisions/Periods/Info<br>
            Type "appointment" to Enable/Disable Your Appointments/Reservations System / Update Appointment Queue Number / Create Physical Appointment<br>
            Type "query" to Query Information
        </div>
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


@frontend_router.get("/", response_class=HTMLResponse)
async def login_or_create_page():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login or Create Account</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            .input { padding: 10px; margin: 10px; font-size: 16px; }
            .button { padding: 10px 20px; margin: 10px; cursor: pointer; font-size: 16px; }
            .hidden { display: none; }
        </style>
    </head>
    <body>
        <h1>Login or Create Account</h1>
        <div>
            <label>
                <input type="radio" name="userType" value="patient" checked onclick="toggleUserType()"> Patient
            </label>
            <label>
                <input type="radio" name="userType" value="clinic" onclick="toggleUserType()"> Clinic
            </label>
        </div>
        <div>
            <label>
                <input type="radio" name="authMode" value="login" checked onclick="toggleAuthMode()"> Login
            </label>
            <label>
                <input type="radio" name="authMode" value="create" onclick="toggleAuthMode()"> Create Account
            </label>
        </div>
        
        <!-- Login Form -->
        <form id="login-form">
            <div id="login-patient-fields">
                <input class="input" id="login-pid" type="text" placeholder="Enter your Patient ID" required>
                <input class="input" id="login-acct_pw" type="password" placeholder="Enter your password" required>
            </div>
            <div id="login-clinic-fields" class="hidden">
                <input class="input" id="login-acct_name" type="text" placeholder="Enter your Clinic Account Name" required>
                <input class="input" id="login-password" type="password" placeholder="Enter your password" required>
            </div>
            <button type="button" class="button" onclick="login()">Login</button>
        </form>
        
        <!-- Create Account Form -->
        <form id="create-form" class="hidden">
            <div id="create-patient-fields">
                <input class="input" id="create-pid" type="text" placeholder="Enter your Patient ID" required>
                <input class="input" id="create-pname" type="text" placeholder="Enter your Name" required>
                <input class="input" id="create-birthdate" type="date" required>
                <select class="input" id="create-gender">
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                </select>
                <input class="input" id="create-email" type="email" placeholder="Enter your Email" required>
                <input class="input" id="create-acct_pw" type="password" placeholder="Create a password" required>
                <input class="input hidden" id="create-status" type="text" value="M" readonly>
            </div>
            <div id="create-clinic-fields" class="hidden">
                <input class="input" id="create-cname" type="text" placeholder="Enter your Clinic Name" required>
                <input class="input" id="create-acct_name" type="text" placeholder="Create an Account Name" required>
                <input class="input" id="create-acct_pw" type="password" placeholder="Create a password" required>
                <input class="input" id="create-fees" type="number" placeholder="Enter Appointment Fees" required>
                <select class="input" id="create-queue_type">
                    <option value="S">Shared Queue Number System for All Doctors/Rooms</option>
                    <option value="I">Individual Queue Number System for Different Doctor/Room</option>
                </select>
                <input class="input" id="create-address" type="text" placeholder="Enter Address (Exclude City and District)" required>

                <input class="input" id="create-city" type="text" placeholder="Enter City" required>
                <input class="input" id="create-district" type="text" placeholder="Enter District" required>
            </div>
            <button type="button" class="button" onclick="createAccount()">Create Account</button>
        </form>
        
        <script>
    function toggleUserType() {
        const userType = document.querySelector('input[name="userType"]:checked').value;
        // Toggle visibility of user type fields
        document.getElementById("login-patient-fields").classList.toggle("hidden", userType !== "patient");
        document.getElementById("login-clinic-fields").classList.toggle("hidden", userType !== "clinic");
        document.getElementById("create-patient-fields").classList.toggle("hidden", userType !== "patient");
        document.getElementById("create-clinic-fields").classList.toggle("hidden", userType !== "clinic");
    }

    function toggleAuthMode() {
        const authMode = document.querySelector('input[name="authMode"]:checked').value;
        // Toggle visibility of forms based on authentication mode
        document.getElementById("login-form").classList.toggle("hidden", authMode !== "login");
        document.getElementById("create-form").classList.toggle("hidden", authMode !== "create");
    }

    // Ensure both toggle functions are called on page load to set the initial visibility state
    window.onload = function() {
        toggleUserType();
        toggleAuthMode();
    };

    async function login() {
        const userType = document.querySelector('input[name="userType"]:checked').value;
        if (userType === "patient") {
            const pid = document.getElementById('login-pid').value;
            const acct_pw = document.getElementById('login-acct_pw').value;
            const response = await fetch('/memberships/authenticate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pid, acct_pw })
            });
            if (response.ok) {
                window.location.href = "/patient_console";
            } else {
                alert("Invalid Patient credentials!");
            }
        } else {
            const acct_name = document.getElementById('login-acct_name').value;
            const password = document.getElementById('login-password').value;
            const response = await fetch('/clinics/authenticate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ acct_name, password })
            });
            if (response.ok) {
                window.location.href = "/clinic_console";
            } else {
                alert("Invalid Clinic credentials!");
            }
        }
    }

    async function createAccount() {
        const userType = document.querySelector('input[name="userType"]:checked').value;
        if (userType === "patient") {
            const genderElement = document.getElementById('create-gender');
            const genderValue = genderElement.value === "male" ? "M" : "F";
            const data = {
                pid: document.getElementById('create-pid').value,
                pname: document.getElementById('create-pname').value,
                birthdate: document.getElementById('create-birthdate').value,
                gender: genderValue,
                email: document.getElementById('create-email').value,
                acct_pw: document.getElementById('create-acct_pw').value,
                status: 'M'
            };

            const response = await fetch('/memberships', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            if (response.ok) {
                alert("Patient account created successfully!");
            } else {
                const errorData = await response.json();
                alert(`Failed to create ${userType} account. Error: ${errorData.detail || 'Unknown error.'}`);
            }
        } else {
            const data = {
                cname: document.getElementById('create-cname').value,
                acct_name: document.getElementById('create-acct_name').value,
                acct_pw: document.getElementById('create-acct_pw').value,
                fee: document.getElementById('create-fees').value,
                queue_type: document.getElementById('create-queue_type').value,
                address: document.getElementById('create-address').value,
                city: document.getElementById('create-city').value,
                district: document.getElementById('create-district').value,
                available: true
            };

            const response = await fetch('/clinics', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                alert("Clinic account created successfully!");
            } else {
                const errorData = await response.json();
                alert(`Failed to create ${userType} account. Error: ${errorData.detail || 'Unknown error.'}`);
            }
        }
    }
</script>
    </body>
    </html>
    """)
