from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
from schemas import EmployeeCreate
import os
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/employees/")
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    new_employee = models.Employee(name=employee.name, position=employee.position)
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

# ✅ Thêm route này để xem danh sách nhân viên
@app.get("/employees/")
def read_employees(db: Session = Depends(get_db)):
    return db.query(models.Employee).all()

@app.get("/")
def root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
