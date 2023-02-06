from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, model, schemas
from .database import SessionLocal

description = """
            performing CRUD operations in Database
            Create: Add data in database
            Retrieve: Getting data from database
            Update: Update data in database
            Delete: Delete data from the database
            """

app = FastAPI(title="CRUD_Operations", description=description)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Adding data to the database
@app.post("/add_employee", response_model=schemas.Employee, tags=["Add_Rows"],
          summary="Add employee Details in Database")
def add_employees(emp: schemas.Emp, db: Session = Depends(get_db)):
    details = crud.add_emp(emp)
    db.add(details)
    db.commit()
    db.refresh(details)
    return model.Employees(**emp.dict())


# Retrieving Employees details from database
@app.get('/get_employees', response_model=list[schemas.Employee], tags=["Retrieve Rows"],
         summary="Getting Details of Employees")
def get_employees(db: Session = Depends(get_db)):
    recs = db.query(model.Employees).all()
    return recs


# Retrieving Particular Employee details from database using id
@app.get('/get_employee/{id}', response_model=schemas.Employee, tags=["Retrieve Particular Row"],
         summary="Getting Details of Particular Employee")
def get_employee(id: int, db: Session = Depends(get_db)):
    db_emp = crud.read_emp(db, id=id)
    return db_emp


# Updating Particular Employee details in database using id
@app.put('/update_employee/{id}', response_model=schemas.Employee, tags=["Update Row"],
         summary="Updating Details of a Particular Employee")
def update_books(id: int, emp: schemas.Emp, db: Session = Depends(get_db)):
    db_emp = crud.update_emp(emp, db, id=id)
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db.query(model.Employees).filter(model.Employees.id == id).first()


# Delete Particular Employee Details from database using id
@app.delete("/delete_employee/{id}", tags=["Delete Row"],
            summary="Deleting Particular Employee Details")
def delete_employee(id: int, db: Session = Depends(get_db)):
    try:
        db.query(model.Employees).filter(model.Employees.id == id).delete()
        db.commit()
    except Exception as e:
        raise Exception(e)
    return {"delete status": "success"}
