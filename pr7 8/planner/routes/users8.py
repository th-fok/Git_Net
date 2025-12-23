from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database.connection8 import get_session
from models.users8 import User, UserCreate, UserSignIn

user_router = APIRouter(
    tags=["User"]
)

# Регистрация пользователя
@user_router.post("/signup")
async def sign_new_user(user_data: UserCreate, session: Session = Depends(get_session)) -> dict:
    # Проверяем, существует ли пользователь с таким email
    statement = select(User).where(User.email == user_data.email)
    existing_user = session.exec(statement).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    
    # Создаем нового пользователя
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        password=user_data.password  # В реальном приложении хэшируйте пароль!
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return {
        "message": "User successfully registered!",
        "user_id": new_user.id
    }

# Вход пользователя
@user_router.post("/signin")
async def sign_user_in(user_credentials: UserSignIn, session: Session = Depends(get_session)) -> dict:
    # Ищем пользователя по email
    statement = select(User).where(User.email == user_credentials.email)
    user = session.exec(statement).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email does not exist"
        )
    
    # Проверяем пароль (в реальном приложении используйте хэширование!)
    if user.password != user_credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )
    
    return {
        "message": "User signed in successfully",
        "user_id": user.id
    }

# Получение всех пользователей (для админа)
@user_router.get("/", response_model=list[User])
async def get_all_users(session: Session = Depends(get_session)) -> list[User]:
    statement = select(User)
    users = session.exec(statement).all()
    return users