# Auth Endpoints
from datetime import timedelta
from fastapi import Depends, HTTPException,status,APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.config import TOKEN_EXPIRES
from app.core.security import create_access_token, get_pwd_hash, verify_pwd
from app.models.model import User
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserResponse
from app.db.database import get_db


router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
     if db.query(User).filter(User.email == user.email).first():
         raise HTTPException(
               status_code=404,
                 detail="User already created!" )

     hashed_password = get_pwd_hash(user.password)

     db_user =  User(
            name = user.name, 
            email = user.email,
            role = user.role,
            hashed_pwd=hashed_password )
     db.add(db_user) 
     db.commit()
     db.refresh(db_user)
     return db_user

@router.post("/token",response_model=Token)
def login_for_access_token(form_data:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
     user = db.query(User).filter(User.email == form_data.username).first()

     if not user or not verify_pwd(form_data.password,user.hashed_pwd):
          raise HTTPException(
               status_code=404,
               detail="Wrong Info!"
          )
     if not user.is_active:
          raise HTTPException(
               status_code=404,
               detail="Inactive User"
          )
     access_token_expires = timedelta(minutes=TOKEN_EXPIRES)
     access_token =  create_access_token(
          data={"sub":user.email},expires_delta=access_token_expires
     )
     return {"access_token":access_token,"token_type":"bearer"}
