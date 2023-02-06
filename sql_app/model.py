from sqlalchemy import Column, Integer, String

from .database import Base


# Create SQLAlchemy Models with attributes/columns
class Employees(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True, nullable=False)
    FirstName = Column(String(50), unique=True)
    LastName = Column(String(50))
    Address = Column(String(100))
    City = Column(String(50))
    State = Column(String(30))
    ZIP = Column(Integer, nullable=False)
    hashed_password = Column(String)
