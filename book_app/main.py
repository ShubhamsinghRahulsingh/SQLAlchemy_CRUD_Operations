from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/add_new', response_model=schemas.Book)
def add_book(b1: schemas.Book, db: Session = Depends(get_db)):
    bk = models.Books(id=b1.id, title=b1.title, author=b1.author, publisher=b1.publisher)
    db.add(bk)
    db.commit()
    db.refresh(bk)
    return models.Books(**b1.dict())


@app.get('/get_list', response_model=list[schemas.Book])
def get_books(db: Session = Depends(get_db)):
    recs = db.query(models.Books).all()
    return recs


@app.get('/book/{id}', response_model=schemas.Book)
def get_book(id: int, db: Session = Depends(get_db)):
    return db.query(models.Books).filter(models.Books.id == id).first()


@app.put('/update/{id}', response_model=schemas.Book)
def update_book(id:int, book: schemas.Book, db: Session = Depends(get_db)):
    b1 = db.query(models.Books).filter(models.Books.id == id).first()
    b1.id = book.id
    b1.title = book.title
    b1.author = book.author
    b1.publisher = book.publisher
    db.commit()
    return db.query(models.Books).filter(models.Books.id == id).first()


@app.delete('/delete/{id}')
def del_book(id:int, db: Session = Depends(get_db)):
    try:
      db.query(models.Books).filter(models.Books.id == id).delete()
      db.commit()
    except Exception as e:
        raise Exception(e)
    return {"delete status": "success"}
