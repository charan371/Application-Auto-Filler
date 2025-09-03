# backend/app/main.py
from fastapi import FastAPI, Request, Form, status
from fastapi import Header, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os
import requests
from . import database, models, crud
from . import auth
from fastapi.middleware.cors import CORSMiddleware

def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split(" ")[1]
    payload = auth.decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload["sub"]

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def root():
    return RedirectResponse("/form.html")

@app.get("/form.html", response_class=HTMLResponse)
async def serve_form():
    return FileResponse("../frontend/templates/form.html")

@app.get("/register.html", response_class=HTMLResponse)
async def serve_register():
    return FileResponse("../frontend/templates/register.html")

@app.get("/courses_list.html", response_class=HTMLResponse)
async def serve_courses_list():
    return FileResponse("../frontend/templates/courses_list.html")

@app.get("/login.html", response_class=HTMLResponse)
async def serve_login():
    return FileResponse("../frontend/templates/login.html")

# Registration endpoint
@app.post("/register")
async def register_user(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    if crud.get_user_by_username(db, data["username"]):
        return JSONResponse({"detail": "Username already exists!"}, status_code=400)
    crud.create_user(db, data["fname"], data["lname"], data["username"], data["password"])
    return {"message": "Registered!"}

# Login endpoint (simple, no JWT/session for now)
@app.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    user = crud.get_user_by_username(db, data["username"])
    if user and auth.verify_password(data["password"], user.password):
        # Return JWT token
        token = auth.create_access_token({"sub": user.username})
        return {"access_token": token, "token_type": "bearer", "username": user.username}
    return JSONResponse({"detail": "Invalid username or password"}, status_code=401)

# Webhook endpoint for external agent to autofill
@app.post("/autofill-webhook")
async def autofill_webhook(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    user = crud.get_user_by_username(db, data.get("username"))
    if not user:
        return JSONResponse({"detail": "User not found"}, status_code=404)
    data["user_id"] = user.id
    submission = db.query(models.FormSubmission).filter_by(user_id=user.id).first()
    if not submission:
        crud.create_submission(db, data)
    else:
        for key, value in data.items():
            if hasattr(submission, key):
                setattr(submission, key, value)
        db.commit()
        db.refresh(submission)
    return {"status": "ok"}

# Save progress for multi-step (AJAX, partial update)
@app.post("/save-progress")
async def save_progress(request: Request, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    data = await request.json()
    user = crud.get_user_by_username(db, current_user)
    if not user:
        return JSONResponse({"detail": "User not found"}, status_code=404)
    submission = db.query(models.FormSubmission).filter_by(user_id=user.id).first()
    data["user_id"] = user.id
    data.pop("username", None)  
    if not submission:
        crud.create_submission(db, data)
    else:
        for key, value in data.items():
            if hasattr(submission, key):
                setattr(submission, key, value)
        db.commit()
    return {"status": "progress saved"}

# Form submit endpoint
@app.post("/submit-form")
async def submit_form(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    
    # PATCH: Convert empty string dates to None
    date_fields = ['date_of_birth', 'visa_expiry_date']
    for field in date_fields:
        if field in data and data[field] == "":
            data[field] = None

    user = crud.get_user_by_username(db, data.get("username"))
    if not user:
        return JSONResponse({"detail": "User not found"}, status_code=404)
    submission = db.query(models.FormSubmission).filter_by(user_id=user.id).first()
    data["user_id"] = user.id
    data.pop("username", None)   
    if not submission:
        crud.create_submission(db, data)
    else:
        for key, value in data.items():
            if hasattr(submission, key):
                setattr(submission, key, value)
        # Optionally, set status to "submitted"
        if hasattr(submission, "status"):
            submission.status = "submitted"
        db.commit()
    return {"message": "Application submitted"}


# Prefill for form (autofill fields for current user)
@app.get("/prefill/{username}")
async def prefill(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = crud.get_user_by_username(db, current_user)
    if not user:
        return JSONResponse({"detail": "User not found"}, status_code=404)
    submission = db.query(models.FormSubmission).filter_by(user_id=user.id).first()
    if not submission:
        return JSONResponse({}, status_code=200)
    return {c.name: getattr(submission, c.name) for c in submission.__table__.columns}

