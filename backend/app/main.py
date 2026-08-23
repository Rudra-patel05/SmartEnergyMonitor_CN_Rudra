from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import energy

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Energy Monitor API",
    description="Backend API for Smart Campus Energy Monitoring System",
    version="1.0.0"
)

# CORS configuration (allow all for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(energy.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Smart Energy Monitor API. Go to /docs for API documentation."}
