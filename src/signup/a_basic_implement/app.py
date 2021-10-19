import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, constr
from sqlalchemy import Column, String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.db import Base, get_session


class Account(Base):
    """
    CREATE TABLE accounts (
        id varchar(100) primary key,
        password varchar(100) not null
    );
    """

    __tablename__ = "accounts"

    id = Column(String, primary_key=True)
    password = Column(String, nullable=False)


class AccountDTO(BaseModel):
    id: constr(max_length=100)
    password: constr(max_length=100)


app = FastAPI()


@app.post("/accounts")
async def create_account(account: AccountDTO, session: Session = Depends(get_session)):
    session.add(Account(**account.dict()))

    try:
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="id already exists")

    return account.dict()


if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=80, reload=True)
