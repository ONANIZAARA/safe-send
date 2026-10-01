from fastapi import APIRouter, HTTPException, Request
from database import SessionLocal, create_audit_log
from models import User
from auth import hash_password, verify_password, create_token

router = APIRouter()

@router.post("/register")
def register(request: Request, data: dict):
    username = data.get("username", "").strip()
    email    = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not username or not email or not password:
        raise HTTPException(status_code=400, detail="All fields are required")

    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    db = SessionLocal()

    existing_username = db.query(User).filter(User.username == username).first()
    if existing_username:
        db.close()
        raise HTTPException(status_code=400, detail="Username already taken")

    existing_email = db.query(User).filter(User.email == email).first()
    if existing_email:
        db.close()
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        username=username,
        email=email,
        password=hash_password(password)
    )
    db.add(new_user)
    db.commit()

    # SAVE USERNAME BEFORE CLOSING DB
    saved_username = new_user.username 

    ip = request.client.host if request.client else "Unknown"
    create_audit_log(db, saved_username, "USER_REGISTER", f"New account created", ip)

    db.close()

    return {"message": f"Account created successfully. Welcome {saved_username}!"}


@router.post("/login")
def login(request: Request, data: dict):
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        db.close()
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(password, user.password):
        db.close()
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # SAVE USERNAME BEFORE CLOSING DB
    saved_username = user.username
    token = create_token({"sub": saved_username})

    ip = request.client.host if request.client else "Unknown"
    create_audit_log(db, saved_username, "USER_LOGIN", f"User logged in successfully", ip)

    db.close()

    return {
        "token":    token,
        "username": saved_username,
        "message":  f"Welcome back {saved_username}!"
    }

@router.get("/me")
def get_me(data: dict = None):
    return {"message": "Profile endpoint - coming soon"}

@router.get("/all-users")
def all_users():
    db = SessionLocal()
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
