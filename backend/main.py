from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import markdown
from database import SessionLocal, init_db
from models.trip import Trip
from services.bedrock_service import bedrock_service
from services.trip_service import (
    calculate_daily_budget,
    get_trip_category,
)

app = FastAPI(
    title="KelanaAI API",
    description="AI-Powered Travel Planning API",
    version="1.0.0"
)

init_db()

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
    travel_style: str
    recommended_transport: str
    ai_recommendation: Optional[str] = None

    class Config:
        from_attributes = True

@app.get("/")
def home():
    return {
        "message": "Welcome to KelanaAI",
        "version": "1.0.0",
        "docs": "/docs"
    }

# Challenge session 3
@app.post("/api/v1/trips", response_model=TripResponse)    
def create_trip(request: TripRequest):
    """
    Create a new trip with AI-powered recommendations
    
    - **destination**: Travel destination (e.g., Japan, Bali, Australia)
    - **days**: Number of days for the trip
    - **budget**: Total budget in USD
    - **travel_style**: Style of travel (Family, Backpacker, Luxury)
    """
    try:
        # Calculate daily budget
        daily_budget = calculate_daily_budget(request.budget, request.days)
    except Exception:
        daily_budget = request.budget / request.days if request.days > 0 else 0.0
    
    try:   
        category = get_trip_category(request.budget)
    except Exception:
        category = "Standard"
    
    # Determine travel style
    travel_style = request.travel_style if request.travel_style else category
    
    # Determine transportation based on destination
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
    db = SessionLocal()
    try:
        trip = Trip(
            destination=request.destination,
            days=request.days,
            budget=request.budget,
            category=category,
            daily_budget=daily_budget,
            ai_recommendation=ai_recommendation
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
            travel_style=travel_style,
            recommended_transport=recommended_transport,
            ai_recommendation=trip.ai_recommendation
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save trip: {str(e)}")
    finally:
        db.close()

@app.get("/api/v1/trip-categories")
def list_trip_categories():
    """Get available trip categories"""
    return ["Backpacker", "Standard", "Luxury"]   

# Homework Session 3 
@app.get("/api/v1/recommendations")
def get_recommendations(destination: Optional[str] = None):
    """
    Get recommended places for a destination
    
    - **destination**: Optional destination name (Japan, Bali, Australia)
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
        
        # Return all if no specific destination
        return default_japan + default_bali + default_australia
    except Exception:
        return ["Tokyo Tower", "Mount Fuji", "Shibuya", "Ubud", "Kuta Beach", "Pandawa Beach", "Sydney", "Melbourne", "Queensland"]

@app.get("/api/v1/transportations")
def get_transportations():
    """Get available transportation options"""
    return ["Bus", "Train", "Flight"]

# Challenge session 4
@app.get("/api/v1/trips")
def list_trips():
    """Get all trips from database"""
    db = SessionLocal()
    try:
        trips = db.query(Trip).all()
        return trips
    finally:
        db.close() 

@app.get("/api/v1/trips/{trip_id}")
def get_trip(trip_id: int):
    """
    Get a specific trip by ID
    
    - **trip_id**: ID of the trip to retrieve
    """
    db = SessionLocal()
    try:
        trip = db.query(Trip).filter(Trip.id == trip_id).first()
        
        if trip is None:
            raise HTTPException(status_code=404, detail=f"Trip with id {trip_id} not found")
            
        return trip
    finally:
        db.close()

@app.delete("/api/v1/trips/{trip_id}")
def delete_trip(trip_id: int):
    """
    Delete a trip by ID
    
    - **trip_id**: ID of the trip to delete
    """
    db = SessionLocal()
    try:
        trip = db.query(Trip).filter(Trip.id == trip_id).first()

        if trip is None:
            raise HTTPException(status_code=404, detail=f"Trip with id {trip_id} not found")

        db.delete(trip)
        db.commit()
        return {"message": f"Trip with id {trip_id} successfully deleted"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete trip: {str(e)}")
    finally:
        db.close()

@app.put("/api/v1/trips/{trip_id}")
def update_trip(trip_id: int, request: TripUpdate):
    """
    Update trip budget and recalculate related fields
    
    - **trip_id**: ID of the trip to update
    - **budget**: New budget amount in USD
    """
    db = SessionLocal()
    try:
        trip = db.query(Trip).filter(Trip.id == trip_id).first()

        if trip is None:
            raise HTTPException(status_code=404, detail=f"Trip with id {trip_id} not found")

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
    finally:
        db.close()

# Additional endpoint to test AI recommendation directly
@app.post("/api/v1/ai/generate-itinerary")
def generate_itinerary(request: TripRequest):
    """
    Generate AI itinerary without saving to database
    
    - **destination**: Travel destination
    - **days**: Number of days
    - **budget**: Total budget in USD
    - **travel_style**: Style of travel
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
def generate_and_save_itinerary(trip_id: int):
    """
    Generate a rich AI itinerary for an existing trip and save it to the database.

    Uses the improved prompt with structured daily plans:
    - **Morning:** 3 specific activities with costs and durations
    - **Afternoon:** cultural sites + authentic local experiences
    - **Evening:** named dinner spots + nightlife recommendations

    - **trip_id**: ID of the existing trip
    """
    db = SessionLocal()
    try:
        # Fetch the existing trip
        trip = db.query(Trip).filter(Trip.id == trip_id).first()
        if trip is None:
            raise HTTPException(status_code=404, detail=f"Trip with id {trip_id} not found")

        # Generate enriched AI recommendation using the richer prompt
        ai_recommendation = bedrock_service.plan_trip_itinerary(
            destination=trip.destination,
            days=trip.days,
            budget=trip.budget,
            travel_style=trip.category
        )

        # Persist the result into the ai_recommendation column
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
            "ai_recommendation": trip.ai_recommendation
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to generate itinerary: {str(e)}")
    finally:
        db.close()

@app.get("/api/v1/trips/{trip_id}/itinerary-html", response_class=HTMLResponse)
def get_trip_itinerary_html(trip_id: int):
    """
    Get trip AI recommendation rendered as beautiful HTML
    
    - **trip_id**: ID of the trip to view
    """
    db = SessionLocal()
    try:
        trip = db.query(Trip).filter(Trip.id == trip_id).first()
        
        if trip is None:
            raise HTTPException(status_code=404, detail=f"Trip with id {trip_id} not found")
        
        if not trip.ai_recommendation:
            raise HTTPException(status_code=404, detail="No AI recommendation available for this trip")
        
        # Convert markdown to HTML
        html_content = markdown.markdown(
            trip.ai_recommendation,
            extensions=['tables', 'fenced_code', 'nl2br']
        )
        
        # Wrap in beautiful HTML template
        full_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{trip.destination} Itinerary - KelanaAI</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #667eea;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .trip-info {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            border-left: 5px solid #667eea;
        }}
        .trip-info p {{
            margin: 8px 0;
            font-size: 1.1em;
        }}
        .trip-info strong {{
            color: #667eea;
        }}
        h1 {{
            color: #667eea;
            margin-top: 30px;
            margin-bottom: 15px;
            font-size: 2.2em;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #764ba2;
            margin-top: 25px;
            margin-bottom: 12px;
            font-size: 1.8em;
        }}
        h3 {{
            color: #667eea;
            margin-top: 20px;
            margin-bottom: 10px;
            font-size: 1.4em;
        }}
        h4 {{
            color: #555;
            margin-top: 15px;
            margin-bottom: 8px;
            font-size: 1.2em;
        }}
        ul, ol {{
            margin-left: 25px;
            margin-bottom: 15px;
        }}
        li {{
            margin-bottom: 8px;
            line-height: 1.6;
        }}
        p {{
            margin-bottom: 15px;
            text-align: justify;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        th {{
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #ddd;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        strong {{
            color: #667eea;
        }}
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #667eea;
            color: #777;
        }}
        .back-button {{
            display: inline-block;
            margin-top: 20px;
            padding: 12px 30px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 25px;
            transition: all 0.3s;
        }}
        .back-button:hover {{
            background: #764ba2;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
                padding: 20px;
            }}
            .back-button {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✈️ KelanaAI Travel Itinerary</h1>
            <p style="color: #764ba2; font-size: 1.2em;">AI-Powered Travel Planning</p>
        </div>
        
        <div class="trip-info">
            <p><strong>📍 Destination:</strong> {trip.destination}</p>
            <p><strong>📅 Duration:</strong> {trip.days} days</p>
            <p><strong>💰 Budget:</strong> ${trip.budget:,.2f} USD (${trip.daily_budget:,.2f}/day)</p>
            <p><strong>🎯 Category:</strong> {trip.category}</p>
            <p><strong>🆔 Trip ID:</strong> #{trip.id}</p>
        </div>
        
        <div class="content">
            {html_content}
        </div>
        
        <div class="footer">
            <p>Generated by <strong>KelanaAI</strong> - Your AI Travel Assistant</p>
            <p style="font-size: 0.9em; color: #999;">Powered by AWS Bedrock</p>
            <a href="/docs" class="back-button">← Back to API Docs</a>
        </div>
    </div>
</body>
</html>
"""
        return HTMLResponse(content=full_html)
        
    finally:
        db.close()

@app.get("/api/v1/ai/preview-format", response_class=HTMLResponse)
def preview_markdown_format():
    """
    Preview the markdown format that AI recommendations will use
    """
    sample_markdown = bedrock_service.plan_trip_itinerary(
        destination="Sample Destination",
        days=3,
        budget=1000,
        travel_style="Family"
    )
    
    html_content = markdown.markdown(
        sample_markdown,
        extensions=['tables', 'fenced_code', 'nl2br']
    )
    
    full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AI Format Preview</title>
    <style>
        body {{ font-family: Arial; padding: 40px; max-width: 900px; margin: 0 auto; }}
        h1 {{ color: #667eea; }}
        h2 {{ color: #764ba2; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th {{ background: #667eea; color: white; padding: 10px; }}
        td {{ border: 1px solid #ddd; padding: 10px; }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>
"""
    return HTMLResponse(content=full_html)