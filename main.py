from fastapi import FastAPI, Header, HTTPException, Request
from typing import Optional
from datetime import datetime
import os
from fastapi.responses import FileResponse

app = FastAPI(title="Aboutxtreme HRMS Mini API")

API_KEY = "demo-key-123"

# -------------------------
# Sample Employees
# -------------------------
EMPLOYEES = {
    "E1001": {
        "employeeId": "E1001",
        "name": "Ayesha Khan",
        "department": "Finance",
        "designation": "Senior Accountant",
        "location": "Karachi",
        "managerId": "E2001",
        "role": "Employee"
    },
    "E2001": {
        "employeeId": "E2001",
        "name": "Sara Malik",
        "department": "HR",
        "designation": "HR Manager",
        "location": "Islamabad",
        "managerId": None,
        "role": "Manager"
    },
    "E3001": {
        "employeeId": "E3001",
        "name": "Hassan Raza",
        "department": "HR",
        "designation": "HR Officer",
        "location": "Lahore",
        "managerId": "E2001",
        "role": "HR"
    }
}

# -------------------------
# Helper
# -------------------------
def check_key(x_api_key: Optional[str]):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# -------------------------
# Health
# -------------------------
@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow()}

# -------------------------
# Employee Profile
# -------------------------
@app.get("/employees/{employeeId}")
def employee_profile(employeeId: str, x_api_key: Optional[str] = Header(None)):
    check_key(x_api_key)
    return EMPLOYEES.get(employeeId, {"message": "Employee not found"})

# -------------------------
# Leave Balance
# -------------------------
@app.get("/leave/balance")
def leave_balance(employeeId: str, x_api_key: Optional[str] = Header(None)):
    check_key(x_api_key)
    return {
        "employeeId": employeeId,
        "annual": 12,
        "sick": 6,
        "casual": 4
    }

# -------------------------
# Attendance Summary
# -------------------------
@app.get("/attendance/summary")
def attendance(employeeId: str, month: str, x_api_key: Optional[str] = Header(None)):
    check_key(x_api_key)
    return {
        "employeeId": employeeId,
        "month": month,
        "workingDays": 23,
        "present": 21,
        "absent": 1,
        "late": 1
    }

# -------------------------
# Fuel Allowance
# -------------------------
@app.get("/allowances/fuel")
def fuel_allowance(employeeId: str, x_api_key: Optional[str] = Header(None)):
    check_key(x_api_key)
    return {
        "employeeId": employeeId,
        "eligible": employeeId == "E1001",
        "monthlyLimit": 15000 if employeeId == "E1001" else 0,
        "currency": "PKR"
    }

# -------------------------
# Payroll – Latest Payslip (FULL URL)
# -------------------------
@app.get("/payroll/payslips/latest")
def latest_payslip(employeeId: str, request: Request, x_api_key: Optional[str] = Header(None)):
    check_key(x_api_key)

    file_name = f"{employeeId}_2026_03.pdf"

    proto = request.headers.get("x-forwarded-proto") or request.url.scheme
    host = request.headers.get("x-forwarded-host") or request.headers.get("host")
    base_url = f"{proto}://{host}"

    return {
        "employeeId": employeeId,
        "month": "2026-03",
        "netSalary": 185000 if employeeId == "E1001" else 152000,
        "currency": "PKR",
        "pdfUrl": f"{base_url}/files/payslips/{file_name}"
    }

# -------------------------
# Payslip File Download
# -------------------------
@app.get("/files/payslips/{fileName}")
def download_payslip(fileName: str, x_api_key: Optional[str] = Header(None)):
    check_key(x_api_key)

    file_path = os.path.join("static", "payslips", fileName)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Payslip not found")

    return FileResponse(file_path, media_type="application/pdf", filename=fileName)