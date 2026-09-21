from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client, Client
from enum import Enum
import os

load_dotenv()

app = FastAPI()
security = HTTPBearer()

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
        "endpoints": ["/tasks", "/auth/signup", "/auth/login", "/auth/logout", "/protected/profile", "/public/info", "/triage"]
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


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        user_response = supabase.auth.get_user(token)
        return user_response.user, token
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@app.get("/protected/profile")
def protected_profile(auth_data=Depends(verify_token)):
    user, token = auth_data
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at
    }


@app.get("/protected/dashboard")
def protected_dashboard(auth_data=Depends(verify_token)):
    user, token = auth_data
    return {"message": f"Welcome to your dashboard, {user.email}"}


@app.post("/auth/logout", status_code=204)
def logout(auth_data=Depends(verify_token)):
    user, token = auth_data
    supabase.auth.sign_out()
    return


# ---------- TRIAGE (LLM) ROUTE ----------

class TriageRequest(BaseModel):
    text: str


class Category(str, Enum):
    billing = "billing"
    bug = "bug"
    feature = "feature"
    other = "other"


class Urgency(str, Enum):
    low = "low"
    normal = "normal"
    high = "high"


class TriageResponse(BaseModel):
    category: Category
    urgency: Urgency
    confidence: float
    reason: str


@app.post("/triage", response_model=TriageResponse)
def triage(request: TriageRequest):
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Field 'text' is required and cannot be empty")
    if len(request.text) > 2000:
        raise HTTPException(status_code=400, detail="Field 'text' must be 2000 characters or fewer")

    if os.getenv("LLM_STUB") == "1":
        return TriageResponse(
            category=Category.other,
            urgency=Urgency.low,
            confidence=0.5,
            reason="Stub mode — no model called"
        )

    raise HTTPException(status_code=501, detail="Model call not implemented yet")