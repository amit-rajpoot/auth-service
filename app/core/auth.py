#Auth Dependencies
from fastapi import Depends, HTTPException
from app.core.config import oauth2_scheme
from app.core.security import verify_token
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.models.model import User
from fastapi import status

def get_current_user(token:str = Depends(oauth2_scheme),
                     db:Session = Depends(get_db)
):
   token_data = verify_token(token)

   user = db.query(User).filter(User.email == token_data.email).first()
   if user is None:
    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="User does not exisit",
                                headers={"WWW-Authenticate":"Bearer"})
   return user

def get_current_active_user(
      current_user:User = Depends(get_current_user)
):
   if not current_user.is_active:
      raise HTTPException(
         status_code=404,
         detail="Inactive User"
      )
   return current_user