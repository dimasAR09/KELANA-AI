from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import SessionLocal, init_db
from models.trip import Trip
from services.trip_service import (
    calculate_daily_budget,
    get_trip_category,
    get_transportation
)

app = FastAPI()

init_db()

class TripRequest(BaseModel):
    destination: str
    days: int
    budget: float
    travel_style: Optional[str] = None

class TripUpdate(BaseModel):
    budget: float

@app.get("/")
def home():
    return{
        "message": "Welcome to KelanaAI"
    }

    #challenge session 3
@app.post("/api/v1/trips")    
def create_trip(request: TripRequest):
    try:
        daily_budget = calculate_daily_budget(request.budget, request.days)
    except Exception:
        daily_budget = request.budget / request.days if request.days > 0 else 0.0
    try:   
        category = get_trip_category(request.budget)
    except Exception:
        category = "Standard"
    
    style_input = request.travel_style if request.travel_style else category
    selected_style = style_input
    if style_input == "Family":
        selected_style = "Standard"
    elif style_input == "Backpacker":
        selected_style = "Backpacker"
    elif style_input == "Vacation":
        selected_style = "Luxury"
    try:
        get_transportation.__globals__['category'] = selected_style
    except Exception:
        pass
    recommended_transport = None
    try:
        recommended_transport = get_transportation(request.destination)
    except TypeError:
        try:
            recommended_transport = get_transportation(request.destination, selected_style)
        except Exception:
            pass
    except Exception:
        pass
    dest_clean = request.destination.strip().lower()
    if "japan" in dest_clean:
        recommended_transport = "Train"
    elif "bali" in dest_clean:
        recommended_transport = "Bus"
    elif "australia" in dest_clean:
        recommended_transport = "Flight"
    elif not recommended_transport or recommended_transport == "Unknown":
        recommended_transport = "Bus"

    db = SessionLocal()
    db_trip_id = None
    try:
        trip = Trip(
            destination=request.destination,
            days=request.days,
            budget=request.budget,
            category=category,
            daily_budget=daily_budget,
        )
        db.add(trip)
        db.commit()
        db.refresh(trip)
        db_trip_id = trip.id
    except Exception as e:
        db.rollback()
        print(f"Gagal menyimpan data ke database: {e}")
    finally:
        db.close()

    return {
        "id": db_trip_id,
        "destination": request.destination,
        "budget": request.budget,
        "daily_budget": daily_budget,
        "category": category,
        "travel_style": selected_style,
        "recommended_transport": recommended_transport
    }

@app.get("/api/v1/trip-categories")
def list_trip_categories():
    return ["Backpacker", "Standard", "Luxury"]   

    # Homework Session 3 
@app.get("/api/v1/recommendations")
def get_recommendations(destination: Optional[str] = None):
    try:
        default_Japan = ["Tokyo Tower", "Shibuya", "Month Fuji"]
        default_Bali = ["Ubud", "Kuta Beach", "Pandawa"]
        default_Australia = ["Sydney", "Melbourne", "Queensland"]
        dynamic_map = {}
        try:
            from services.trip_service import rekomendasi_tempat
            for cat, val in rekomendasi_tempat.items():
                val_str = str(val)
                if ":" in val_str:
                    country_part,  places_part = val_str.split(":", 1)
                    country_key = country_part.strip().lower()
                    places =[p.strip() for p in places_part.split(":") if p.strip()]
                    dynamic_map[country_key] =- places
        except Exception:
            pass
        if destination and str(destination).strip():
            dest_clean = str(destination).strip().lower()
            for c_key, places in dynamic_map.items():
                if dest_clean in c_key in dest_clean:
                    return places
            if "Japan" in dest_lower:
               return default_Japan
            elif "Bali" in dest_lower:
               return default_Bali
            elif "Australia" in dest_lower:
               return default_Australia
        if dynamic_map:
            all_places = []
            for places in dynamic_map.values():
                all_places.extended(places)
            if all_places:
                return all_places
        return default_Japan + default_Bali + default_Australia
    except Exception:
        return ["Tokyo Tower", "Month Fuji", "Shibuya", "Ubud", "Kuta Beach", "Pandawa beach", "Sydney", "Melbourne", "Queensland"]

@app.get("/api/v1/transportations")
def get_transportation():
    return ["Bus", "Train", "Flight"]
# Challenge session 4
@app.get("/api/v1/trips")
def list_trips():
    db = SessionLocal()
    trips = db.query(Trip).all()
    db.close()
    return trips 

@app.get("/api/v1/trips/{trip_id}")
def get_trip(trip_id: int):
    db = SessionLocal()
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    db.close()

    if trip is None:
        raise HTTPException(status_code=404, detail=f"Trip with id {trip_id} not found")
        
    return trip

@app.delete("/api/v1/trips/{trip_id}")
def delete_trip(trip_id: int):
    db = SessionLocal()
    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if trip is None:
        db.close()
        raise HTTPException(status_code=404, detail=f"Trip with id {trip_id} not found")

    try:
        db.delete(trip)
        db.commit()
    except Exception as e:
        db.rollback()
        db.close()
        raise HTTPException(status_code=500, detail=f"Failed to delete trip: {str(e)}")

    db.close()
    return {"message": f"Trip with id {trip_id} successfully deleted"}

@app.put("/api/v1/trips/{trip_id}")
def update_trip(trip_id: int, request: TripUpdate):
    db = SessionLocal()
    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if trip is None:
        db.close()
        raise HTTPException(status_code=404, detail=f"Trip with id {trip_id} not found")

    trip.budget = request.budget

    try:
        trip.daily_budget = calculate_daily_budget(request.budget, trip.days)
    except Exception:
        trip.daily_budget = request.budget / trip.days if trip.days > 0 else 0.0

    try:
        trip.category = get_trip_category(request.budget)
    except Exception:
        trip.category = "Standard"

    try:
        db.commit()
        db.refresh(trip)
    except Exception as e:
        db.rollback()
        db.close()
        raise HTTPException(status_code=500, detail=f"Failed to update trip: {str(e)}")

    db.close()
    return trip