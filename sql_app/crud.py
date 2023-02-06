from sqlalchemy.orm import Session

from . import model, schemas


def add_emp(emp: schemas.Emp):
    hashed_password = emp.hashed_password+"secretpassword"
    db_emp = model.Employees(id=emp.id, FirstName=emp.FirstName, LastName=emp.LastName,
                             Address=emp.Address, City=emp.City, State=emp.State,
                             ZIP=emp.ZIP, hashed_password=hashed_password)
    return db_emp


def read_emp(db: Session, id: int):
    db_emp = db.query(model.Employees).filter(model.Employees.id == id).first()
    return db_emp


def update_emp(emp: schemas.Emp, db: Session, id: int):
    db_emp = db.query(model.Employees).filter(model.Employees.id == id).first()
    db_emp.id = emp.id
    db_emp.FirstName = emp.FirstName
    db_emp.LastName = emp.LastName
    db_emp.Address = emp.Address
    db_emp.City = emp.City
    db_emp.State = emp.State
    db_emp.ZIP = emp.ZIP
    db_emp.hashed_password = emp.hashed_password
    return db_emp




