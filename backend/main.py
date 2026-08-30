from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import markdown
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models.trip import Trip
from models.user import User
from services.bedrock_service import bedrock_service
import bcrypt
from services.auth_service import register, login, get_current_user, get_db, hash_password

from services.trip_service import (
    calculate_daily_budget,
    get_trip_category,
)
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

# --- Pydantic Schemas ---

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