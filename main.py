from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client, Client
import os

load_dotenv()

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("Server running and connected to Supabase")


class AuthRequest(BaseModel):
    email: str
    password: str


@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "2.0",
        "endpoints": ["/tasks", "/auth/signup", "/auth/login", "/auth/logout", "/protected/profile", "/public/info"]
    }


@app.get("/health")
def health():
    return {"status": "ok"}


# ---------- AUTH ROUTES ----------

@app.post("/auth/signup", status_code=201)
def signup(auth: AuthRequest):
    if not auth.email or not auth.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    try:
        result = supabase.auth.sign_up({
            "email": auth.email,
            "password": auth.password
        })
        return {"user": result.user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/auth/login")
def login(auth: AuthRequest):
    if not auth.email or not auth.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    try:
        result = supabase.auth.sign_in_with_password({
            "email": auth.email,
            "password": auth.password
        })
        return {
            "access_token": result.session.access_token,
            "refresh_token": result.session.refresh_token
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid login credentials")

@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}


@app.get("/protected/profile")
def protected_profile(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Access token required")
    token = authorization.split(" ")[1]
    return {"message": "token received", "token_preview": token[:20] + "..."}