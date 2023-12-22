from sqlalchemy.orm import Session

from schemas import schemas
from models import models

from aes.aes_generator import generate_aes256_gcm_key
from aes.aes_encrypt import aes_encrypt, aes_decrypt


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password
    random_aes_key = generate_aes256_gcm_key()
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password, aes_key=random_aes_key)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_aes_key(db: Session, user: schemas.User):
    random_aes_key = generate_aes256_gcm_key()
    user.aes_key = random_aes_key
    db.commit()
    db.refresh(user)
    return user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemBase, user_model: models.User):
    aes_dict: dict = aes_encrypt(item.text, user_model.aes_key)
    db_item = models.Item(text=aes_dict['text'], iv=aes_dict['iv'], owner_id=user_model.id)
    # db_item = models.Item(**item.dict(), owner_id=user_model.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def decrypt_user_item(item: schemas.ItemCreate, user_model: models.User):
    decrypted_text = aes_decrypt(item.iv, item.text, user_model.aes_key)
    return decrypted_text
