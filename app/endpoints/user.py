#Users Endpoints
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.auth import get_current_active_user
from app.core.security import get_pwd_hash
from app.db.database import get_db
from app.models.model import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()

@router.get("/")
def root():
    return {"message": "FastAPI Tutorial with SQLAlchemy!"}


@router.get("/profile",response_model=UserResponse)
def get_profile(current_user:User = Depends(get_current_active_user)):
    return current_user

@router.get("/verify-token")
def verify_token_endpoint(current_user:User = Depends(get_current_active_user)):
    return{
        "valid":True,
        "users":{
            "id":current_user.id,
            "name":current_user.name,
            "email":current_user.email,
            "role":current_user.role
        }
    }


@router.get("/users/", response_model=List[UserResponse])
def get_users(current_user:User = Depends(get_current_active_user),db: Session = Depends(get_db)):
    """Get all users"""
    return db.query(User).all()


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id:int,current_user:User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Get one user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, current_user:User = Depends(get_current_active_user),db: Session = Depends(get_db)):
    """Create a new user"""
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_pwd_hash(user.password)
    db_user = User(
        name = user.name,
        email= user.email,
        role =  user.role,
        hashed_pwd = hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.patch("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate,current_user:User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Update a user"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    
    db_user.name = user.name
    db_user.email = user.email
    db_user.role = user.role


    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/users/{user_id}")
def delete_user(user_id: int,current_user:User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Delete a user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_user.id:
        raise HTTPException(status_code=404,detail="You can not delete yourself!")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}