from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from typing import Optional, List
import logging
import markdown
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models.trip import Trip
from models.user import User
from services.bedrock_service import bedrock_service
import bcrypt
from services.auth_service import register, login, get_current_user, get_db, hash_password
from services.kb_service import ask_knowledge_base

from services.trip_service import (
    calculate_daily_budget,
    get_trip_category,
)
from services import conversation_service
from models.conversation import Conversation, Message
from datetime import timedelta

app = FastAPI(
    title="KelanaAI API",
    description="AI-Powered Travel Planning API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

# Suppress noisy Chrome DevTools probe requests from logs
class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return "/.well-known/appspecific/com.chrome.devtools.json" not in record.getMessage()

logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

# Respond to Chrome DevTools probe so it stops sending 404s
@app.get("/.well-known/appspecific/com.chrome.devtools.json", include_in_schema=False)
def chrome_devtools_probe():
    return JSONResponse(content={})

# Override OpenAPI schema agar Swagger UI bisa authorize dengan Bearer token
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in schema.get("paths", {}).values():
        for operation in path.values():
            operation["security"] = [{"BearerAuth": []}]
    app.openapi_schema = schema
    return schema

app.openapi = custom_openapi

# --- Pydantic Schemas ---
class QuestionRequest(BaseModel):
       question: str

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class TripRequest(BaseModel):
    destination: str
    days: int
    budget: float
    travel_style: Optional[str] = "Family"

class TripUpdate(BaseModel):
    budget: float

# --- Conversation Schemas ---
class ConversationCreate(BaseModel):
    title: Optional[str] = None

class ConversationRename(BaseModel):
    title: str

class MessageSend(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    created_at: str

    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: int
    user_id: int
    title: Optional[str] = None
    created_at: str
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True

class TripResponse(BaseModel):
    id: int
    destination: str
    days: int
    budget: float
    category: str
    daily_budget: float
    travel_style: Optional[str] = "Family"
    recommended_transport: Optional[str] = "Bus"  # Opsional agar data dari DB tidak error validation
    ai_recommendation: Optional[str] = None
    user_id: Optional[int] = None

    class Config:
        from_attributes = True

# --- API Endpoints ---

@app.post("/api/v1/auth/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Endpoint untuk mendaftarkan user baru"""
    # Cek apakah email sudah digunakan
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")
    
    # Simpan user dengan password yang di-hash
    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    return {"message": "Registrasi berhasil"}

@app.post("/api/v1/auth/login")
def login_user(user: UserLogin):
    token = login(user.email, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Email atau password salah")
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/v1/auth/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    """Mendapatkan data pengguna yang sedang login"""
    return current_user

@app.get("/")
def home():
    return {
        "message": "Welcome to KelanaAI",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/api/v1/health")
def health_check(db: Session = Depends(get_db)):
    """Diagnostic endpoint to verify Database connectivity"""
    db_status = "OK"
    db_detail = "Database connected successfully"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = "ERROR"
        db_detail = str(e)

    return {
        "status": "online",
        "database": db_status,
        "db_detail": db_detail
    }

@app.post("/api/v1/trips", response_model=TripResponse)    
def create_trip(request: TripRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Create a new trip with AI-powered recommendations
    """
    try:
        daily_budget = calculate_daily_budget(request.budget, request.days)
    except Exception:
        daily_budget = request.budget / request.days if request.days > 0 else 0.0
    
    try:   
        category = get_trip_category(request.budget)
    except Exception:
        category = "Standard"
    
    travel_style = request.travel_style if request.travel_style else category
    
    # Determine transportation based on destination & category
    destination_lower = request.destination.strip().lower()
    if "japan" in destination_lower:
        recommended_transport = "Train"
    elif "bali" in destination_lower:
        recommended_transport = "Bus"
    elif "australia" in destination_lower:
        recommended_transport = "Flight"
    elif category == "Backpacker":
        recommended_transport = "Bus"
    elif category == "Standard":
        recommended_transport = "Train"
    elif category == "Luxury":
        recommended_transport = "Flight"
    else:
        recommended_transport = "Bus"

    # Generate AI recommendation
    try:
        ai_recommendation = bedrock_service.plan_trip_itinerary(
            destination=request.destination,
            days=request.days,
            budget=request.budget,
            travel_style=travel_style
        )
    except Exception as e:
        print(f"Error generating AI recommendation: {e}")
        ai_recommendation = f"AI recommendation will be generated for your {request.days}-day trip to {request.destination} with a budget of ${request.budget}."

    # Save to database
    try:
        trip = Trip(
            destination=request.destination,
            days=request.days,
            budget=request.budget,
            category=category,
            daily_budget=daily_budget,
            travel_style=travel_style,
            ai_recommendation=ai_recommendation,
            user_id=current_user.id
        )
        db.add(trip)
        db.commit()
        db.refresh(trip)
        
        return TripResponse(
            id=trip.id,
            destination=trip.destination,
            days=trip.days,
            budget=trip.budget,
            category=trip.category,
            daily_budget=trip.daily_budget,
            travel_style=getattr(trip, "travel_style", travel_style),
            recommended_transport=recommended_transport,
            ai_recommendation=trip.ai_recommendation,
            user_id=trip.user_id
        )
    except Exception as e:
        db.rollback()
        err_str = str(e)
        if "travel_style" in err_str:
            detail = "Database Error: Kolom 'travel_style' belum ada di tabel PostgreSQL. Silakan jalankan query SQL: ALTER TABLE trips ADD COLUMN IF NOT EXISTS travel_style VARCHAR(100);"
        else:
            detail = f"Failed to save trip: {err_str}"
        raise HTTPException(status_code=500, detail=detail)

@app.get("/api/v1/trip-categories")
def list_trip_categories():
    """Get available trip categories"""
    return ["Backpacker", "Standard", "Luxury"]   

# Homework Session 3 
@app.get("/api/v1/recommendations")
def get_recommendations(destination: Optional[str] = None):
    """
    Get recommended places for a destination
    """
    try:
        default_japan = ["Tokyo Tower", "Shibuya", "Mount Fuji"]
        default_bali = ["Ubud", "Kuta Beach", "Pandawa Beach"]
        default_australia = ["Sydney", "Melbourne", "Queensland"]
        
        if destination and str(destination).strip():
            dest_lower = str(destination).strip().lower()
            
            if "japan" in dest_lower:
                return default_japan
            elif "bali" in dest_lower:
                return default_bali
            elif "australia" in dest_lower:
                return default_australia
        
        return default_japan + default_bali + default_australia
    except Exception:
        return ["Tokyo Tower", "Mount Fuji", "Shibuya", "Ubud", "Kuta Beach", "Pandawa Beach", "Sydney", "Melbourne", "Queensland"]

@app.get("/api/v1/transportations")
def get_transportations():
    """Get available transportation options"""
    return ["Bus", "Train", "Flight"]

# Challenge session 4: Get All Trips (Diberikan response_model agar JSON Serialization sukses)
@app.get("/api/v1/trips", response_model=List[TripResponse])
@app.get("/api/v1/trips/", response_model=List[TripResponse], include_in_schema=False)
def list_trips(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all trips from database"""
    try:
        trips = db.query(Trip).filter(Trip.user_id == current_user.id).order_by(Trip.id.desc()).all()
        return trips
    except Exception as e:
        err_str = str(e)
        if "travel_style" in err_str:
            detail = "Database Error: Kolom 'travel_style' belum ada di tabel PostgreSQL. Silakan jalankan query SQL: ALTER TABLE trips ADD COLUMN IF NOT EXISTS travel_style VARCHAR(100);"
        else:
            detail = f"Failed to fetch trips: {err_str}"
        raise HTTPException(status_code=500, detail=detail)

@app.get("/api/v1/trips/{trip_id}", response_model=TripResponse)
def get_trip(trip_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get a specific trip by ID (Protected)
    """
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    
    if trip is None:
        raise HTTPException(status_code=404, detail=f"Trip with id {trip_id} not found")

    if trip.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Akses ditolak: Ini bukan trip Anda.")
        
    return trip

@app.delete("/api/v1/trips/{trip_id}")
def delete_trip(trip_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Delete a trip by ID (Protected)
    """
    try:
        trip = db.query(Trip).filter(Trip.id == trip_id).first()

        if trip is None:
            raise HTTPException(status_code=404, detail=f"Trip with id {trip_id} not found")
        if trip.user_id != current_user.id:
             raise HTTPException(status_code=403, detail="Akses ditolak: Anda tidak dapat menghapus trip ini.")

        db.delete(trip)
        db.commit()
        return {"message": f"Trip with id {trip_id} successfully deleted"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete trip: {str(e)}")

@app.put("/api/v1/trips/{trip_id}", response_model=TripResponse)
def update_trip(trip_id: int, request: TripUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Update trip budget and recalculate related fields (Protected)
    """
    try:
        trip = db.query(Trip).filter(Trip.id == trip_id).first()

        if trip is None:
            raise HTTPException(status_code=404, detail=f"Trip with id {trip_id} not found")
        if trip.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Akses ditolak: Anda tidak dapat mengubah trip ini.")

        # Update budget
        trip.budget = request.budget

        # Recalculate daily budget
        try:
            trip.daily_budget = calculate_daily_budget(request.budget, trip.days)
        except Exception:
            trip.daily_budget = request.budget / trip.days if trip.days > 0 else 0.0

        # Recalculate category
        try:
            trip.category = get_trip_category(request.budget)
        except Exception:
            trip.category = "Standard"

        db.commit()
        db.refresh(trip)
        return trip
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update trip: {str(e)}")

# Additional endpoint to test AI recommendation directly
@app.post("/api/v1/ai/generate-itinerary")
def generate_itinerary(request: TripRequest):
    """
    Generate AI itinerary without saving to database
    """
    try:
        ai_recommendation = bedrock_service.plan_trip_itinerary(
            destination=request.destination,
            days=request.days,
            budget=request.budget,
            travel_style=request.travel_style or "Family"
        )
        return {
            "destination": request.destination,
            "days": request.days,
            "budget": request.budget,
            "travel_style": request.travel_style or "Family",
            "ai_recommendation": ai_recommendation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate itinerary: {str(e)}")

@app.post("/api/v1/trips/{trip_id}/generate")
def generate_and_save_itinerary(trip_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Generate a rich AI itinerary for an existing trip and save it to the database.
    """
    try:
        trip = db.query(Trip).filter(Trip.id == trip_id).first()
        if trip is None:
            raise HTTPException(status_code=404, detail=f"Trip with id {trip_id} not found")

        if trip.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Akses ditolak: Anda tidak memiliki akses ke trip ini.")

        # Gunakan field travel_style jika tersedia
        travel_style = getattr(trip, 'travel_style', trip.category)

        ai_recommendation = bedrock_service.plan_trip_itinerary(
            destination=trip.destination,
            days=trip.days,
            budget=trip.budget,
            travel_style=travel_style
        )

        trip.ai_recommendation = ai_recommendation
        db.commit()
        db.refresh(trip)

        return {
            "id": trip.id,
            "destination": trip.destination,
            "days": trip.days,
            "budget": trip.budget,
            "category": trip.category,
            "daily_budget": trip.daily_budget,
            "travel_style": travel_style,
            "ai_recommendation": trip.ai_recommendation,
            "user_id": trip.user_id
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to generate itinerary: {str(e)}")

# HTML Render Endpoint (Sudah Ditutup String Triple Quote dan Ditambahkan Return)
@app.get("/api/v1/trips/{trip_id}/itinerary-html", response_class=HTMLResponse)
def get_trip_itinerary_html(trip_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get trip AI recommendation rendered as HTML (Protected)
    """
    try:
        trip = db.query(Trip).filter(Trip.id == trip_id).first()
        
        if trip is None:
            raise HTTPException(status_code=404, detail=f"Trip with id {trip_id} not found")

        if trip.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Akses ditolak: Ini bukan trip Anda.")
        
        if not trip.ai_recommendation:
            raise HTTPException(status_code=404, detail="No AI recommendation available for this trip")
        
        # Convert markdown to HTML
        html_content = markdown.markdown(
            trip.ai_recommendation,
            extensions=['tables', 'fenced_code', 'nl2br']
        )

        # Wrap in HTML template
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{trip.destination} Itinerary - KelanaAI</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8; color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        .container {{
            max-width: 900px; margin: 0 auto; background: white;
            padding: 40px; border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        .header {{
            text-align: center; border-bottom: 3px solid #667eea;
            padding-bottom: 20px; margin-bottom: 30px;
        }}
        .header h1 {{ color: #667eea; font-size: 2.5em; margin-bottom: 10px; }}
        .trip-info {{
            background: #f8f9fa; padding: 20px; border-radius: 10px;
            margin-bottom: 30px; border-left: 5px solid #667eea;
        }}
        .trip-info p {{ margin: 8px 0; font-size: 1.1em; }}
        .trip-info strong {{ color: #667eea; }}
        h1, h2, h3 {{ color: #667eea; margin-top: 25px; margin-bottom: 12px; }}
        ul, ol {{ margin-left: 20px; margin-bottom: 15px; }}
        li {{ margin-bottom: 8px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✈️ {trip.destination} Itinerary</h1>
            <p>Generated by KelanaAI</p>
        </div>
        <div class="trip-info">
            <p><strong>Duration:</strong> {trip.days} Days</p>
            <p><strong>Budget:</strong> USD ${trip.budget:,.2f}</p>
            <p><strong>Category:</strong> {trip.category}</p>
        </div>
        <div class="content">
            {html_content}
        </div>
    </div>
</body>
</html>"""

        return HTMLResponse(content=full_html, status_code=200)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to render HTML: {str(e)}")


@app.post("/api/v1/assistant")
def ask_assistant_endpoint(request: QuestionRequest, current_user: User = Depends(get_current_user)):
    """
    Endpoint RAG: Menerima pertanyaan, mencari di Knowledge Base, dan mengembalikan jawaban.
    Dilindungi dengan JWT (Hanya user login yang bisa bertanya).
    """
    try:
        result = ask_knowledge_base(request.question)
        
        return {
            "question": request.question,
            "answer": result["answer"],
            "sources": result["sources"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to query assistant: " + str(e))


# ─── Conversation Memory Endpoints (Session 10) ───────────────────────────────

def _fmt_msg(msg: Message) -> MessageResponse:
    """Helper: convert Message ORM object ke MessageResponse schema."""
    return MessageResponse(
        id=msg.id,
        conversation_id=msg.conversation_id,
        role=msg.role,
        content=msg.content,
        created_at=msg.created_at.isoformat(),
    )

def _fmt_conv(conv: Conversation, include_messages: bool = False) -> ConversationResponse:
    """Helper: convert Conversation ORM object ke ConversationResponse schema."""
    messages = [_fmt_msg(m) for m in conv.messages] if include_messages else []
    return ConversationResponse(
        id=conv.id,
        user_id=conv.user_id,
        title=conv.title,
        created_at=conv.created_at.isoformat(),
        messages=messages,
    )


@app.post("/api/v1/conversations", status_code=201)
def create_conversation(
    body: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Part 3 — Conversation APIs (CREATE):
    Buat conversation baru dan kembalikan conversation_id.
    """
    conv = conversation_service.create_conversation(db, user_id=current_user.id, title=body.title)
    return {"conversation_id": conv.id, "title": conv.title, "created_at": conv.created_at.isoformat()}


@app.get("/api/v1/conversations")
def list_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Part 3 — Conversation APIs (LIST):
    Daftar semua conversation milik user yang sedang login.
    """
    convs = conversation_service.list_conversations(db, user_id=current_user.id)
    return [_fmt_conv(c) for c in convs]


@app.get("/api/v1/conversations/{conversation_id}")
def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Part 7 — Continue Existing Conversations:
    Ambil conversation beserta semua message-nya.
    """
    conv = conversation_service.get_conversation(db, conversation_id, user_id=current_user.id)
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversation tidak ditemukan")
    return _fmt_conv(conv, include_messages=True)


@app.post("/api/v1/conversations/{conversation_id}/messages", status_code=201)
def send_message(
    conversation_id: int,
    body: MessageSend,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Part 4 — Send Message API:
    Orkestrasi lengkap: simpan user message → load history → build prompt
    → panggil Bedrock → simpan AI response → kembalikan response.
    """
    if not body.content.strip():
        raise HTTPException(status_code=422, detail="Pesan tidak boleh kosong")

    ai_message = conversation_service.send_message(
        db,
        conversation_id=conversation_id,
        user_id=current_user.id,
        user_content=body.content.strip(),
    )

    if ai_message is None:
        raise HTTPException(status_code=404, detail="Conversation tidak ditemukan atau bukan milik Anda")

    return _fmt_msg(ai_message)


@app.patch("/api/v1/conversations/{conversation_id}")
def rename_conversation(
    conversation_id: int,
    body: ConversationRename,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Challenge — Rename Conversation:
    Ganti title conversation dengan nama yang lebih bermakna.
    """
    conv = conversation_service.rename_conversation(
        db,
        conversation_id=conversation_id,
        user_id=current_user.id,
        title=body.title.strip(),
    )
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversation tidak ditemukan")
    return _fmt_conv(conv)


@app.delete("/api/v1/conversations/{conversation_id}", status_code=204)
def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Hapus conversation beserta semua message-nya."""
    conv = conversation_service.get_conversation(db, conversation_id, user_id=current_user.id)
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversation tidak ditemukan")
    db.delete(conv)
    db.commit()
    return None
