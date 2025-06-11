from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models

# Khởi tạo bảng trong CSDL
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency: lấy session database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/employees/")
def create_employee(name: str, position: str, db: Session = Depends(get_db)):
    employee = models.Employee(name=name, position=position)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

@app.get("/employees/")
def read_employees(db: Session = Depends(get_db)):
    return db.query(models.Employee).all()
