from sqlalchemy.orm import Session
from app.models.user import User
from app.models.userRole import UserRole
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password


def get_user_by_username(*, db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(*, db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_superuser(*, db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        role=UserRole.ADMIN,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(*, db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session):
    return db.query(User).all()


def authenticate_user(*, db: Session, username: str, password: str):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def get_user_by_email(*, db: Session, email: str):
    return db.query(User).filter(User.email == email).first()