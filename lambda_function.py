from fastapi import FastAPI
from mangum import Mangum  # Adapter for AWS Lambda
from database import get_employee_collection  # Import DB connection

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from AWS Lambda!"}

@app.get("/employees")
def get_employees():
    employees = get_employee_collection().find({}, {"_id": 0})  # Exclude `_id`
    return list(employees)

# AWS Lambda handler
handler = Mangum(app)
