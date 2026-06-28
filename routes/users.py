from fastapi import APIRouter, HTTPException
from database import SessionLocal
from models import User
from auth import hash_password, verify_password, create_token

router = APIRouter()


@router.post("/register")
def register(data: dict):
    username = data.get("username", "").strip()
    email    = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not username or not email or not password:
        raise HTTPException(status_code=400, detail="All fields are required")

    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    db = SessionLocal()

    # Check if username already exists
    existing_username = db.query(User).filter(User.username == username).first()
    if existing_username:
        db.close()
        raise HTTPException(status_code=400, detail="Username already taken")

    # Check if email already exists
    existing_email = db.query(User).filter(User.email == email).first()
    if existing_email:
        db.close()
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    new_user = User(
        username=username,
        email=email,
        password=hash_password(password)
    )
    db.add(new_user)
    db.commit()
    db.close()

    return {"message": f"Account created successfully. Welcome {username}!"}


@router.post("/login")
def login(data: dict):
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    db     = SessionLocal()
    user   = db.query(User).filter(User.username == username).first()
    db.close()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_token({"sub": user.username})

    return {
        "token":    token,
        "username": user.username,
        "message":  f"Welcome back {user.username}!"
    }


@router.get("/me")
def get_me(data: dict = None):
    return {"message": "Profile endpoint - coming soon"}


@router.get("/all-users")
def all_users():
    db    = SessionLocal()
    users = db.query(User).all()
    db.close()
    return [
        {
            "id":         u.id,
            "username":   u.username,
            "email":      u.email,
            "created_at": str(u.created_at)
        }
        for u in users
    ]