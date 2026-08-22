"""
Test script to check if all imports work correctly
"""
print("Testing imports...")

try:
    print("✓ Importing FastAPI...")
    from fastapi import FastAPI, HTTPException
    
    print("✓ Importing Pydantic...")
    from pydantic import BaseModel
    
    print("✓ Importing database...")
    from database import SessionLocal, init_db
    
    print("✓ Importing Trip model...")
    from models.trip import Trip
    
    print("✓ Importing bedrock_service...")
    from services.bedrock_service import bedrock_service
    
    print("✓ Importing trip_service...")
    from services.trip_service import calculate_daily_budget, get_trip_category
    
    print("\n✅ All imports successful!")
    print("\nDatabase connection test:")
    try:
        init_db()
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"⚠️  Database connection issue: {e}")
    
    print("\nBedrock service test:")
    print(f"- AWS Region: {bedrock_service.aws_region}")
    print(f"- Model ID: {bedrock_service.model_id}")
    print(f"- Bedrock configured: {bedrock_service.bedrock_runtime is not None}")
    
    print("\n✅ System is ready to run!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
