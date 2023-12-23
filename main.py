import os
import json
import subprocess

from fastapi import FastAPI, Depends, Request, HTTPException, Response
from fastapi.responses import HTMLResponse, StreamingResponse

from sqlalchemy.orm import Session

from aes import aes_encrypt
from database import SessionLocal, engine
from crud import crud
from schemas import schemas
from models import models

"""
APP NAME
"""
app = FastAPI()

"""
BLACKLIST
"""
BLACKLIST = []

"""
DATABASE
"""
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int or str, password: str, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     if db_user.hashed_password != password:
#         raise HTTPException(status_code=400, detail="Invalid password")
#     return db_user


@app.post("/login/", response_model=schemas.User)
def read_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.hashed_password != user.password:
        raise HTTPException(status_code=400, detail="Invalid password")
    return db_user


@app.post("/update_aes_key/", response_model=schemas.User)
def update_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.hashed_password != user.password:
        raise HTTPException(status_code=400, detail="Invalid password")
    db_user = crud.update_user_aes_key(db, user=db_user)
    return db_user


@app.post("/encrypt/", response_model=schemas.ItemCreate)
def encrypt_item(user_email: str, item: schemas.ItemBase, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user_email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_item = crud.create_user_item(db=db, item=item, user_model=db_user)
    return db_item


@app.post("/decrypt/")
def decrypt_item(user_email: str, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user_email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_item = crud.decrypt_user_item(item=item, user_model=db_user)
    response = Response(content=db_item, media_type="text/plain", status_code=200)
    return response


@app.delete("/drop_user/")
def drop_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user = crud.drop_user(db, user=db_user)
    response = Response(content=f"User {db_user.email} deleted", media_type="text/plain", status_code=200)
    return response


@app.delete("/drop_all_user_items/")
def drop_all_user_items(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user = crud.drop_all_user_items(db, user=db_user)
    return db_user


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#         user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)
#
#
# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items


if __name__ == '__main__':
    import uvicorn

    # uvicorn.run(app, host='0.0.0.0', port=8989, ssl_keyfile="privkey.pem", ssl_certfile="cert.pem", reload=True)
    uvicorn.run(app, host='0.0.0.0', port=8989)
