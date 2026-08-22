"""
Script to run the KelanaAI FastAPI application
"""
import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("Starting KelanaAI API Server")
    print("=" * 60)
    print("\nSwagger UI akan tersedia di:")
    print("👉 http://127.0.0.1:8000/docs")
    print("\nReDoc akan tersedia di:")
    print("👉 http://127.0.0.1:8000/redoc")
    print("\nTekan CTRL+C untuk menghentikan server")
    print("=" * 60)
    print()
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
