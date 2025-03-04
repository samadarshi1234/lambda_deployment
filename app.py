from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from mangum import Mangum
from database import get_employee_collection
import uvicorn

# Initialize FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Get MongoDB collection
collection = get_employee_collection()

							
@app.get("/")
def home(request: Request):
    employees = list(collection.find({}, {"_id": 1, "name": 1, "age": 1, "department": 1}))
    for emp in employees:
        emp["id"] = str(emp.pop("_id"))
    return templates.TemplateResponse("index.html", {"request": request, "employees": employees})

				   
@app.get("/add")
def add_page(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})

									 
@app.post("/add")
def add_employee(name: str = Form(...), age: int = Form(...), department: str = Form(...)):
    employee = {"name": name, "age": age, "department": department}
    collection.insert_one(employee)
    return RedirectResponse(url="/", status_code=303)

				 
@app.get("/delete/{employee_id}")
def delete_employee(employee_id: str):
    collection.delete_one({"_id": ObjectId(employee_id)})
    return RedirectResponse(url="/", status_code=303)

# AWS Lambda handler
handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)