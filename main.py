from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
import os
import uvicorn

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

@app.get("/")
def root():
    return {"message": "Hello, World!"}
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)