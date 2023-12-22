from pydantic import BaseModel


class ItemBase(BaseModel):
    text: str


class ItemCreate(ItemBase):
    iv: str


class Item(ItemCreate):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []
    aes_key: str

    class Config:
        orm_mode = True
