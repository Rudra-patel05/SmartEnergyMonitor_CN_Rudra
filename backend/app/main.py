from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import energy, prediction, anomaly  # Day 10: anomaly router added

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
# energy.py  — prefix /api/energy  (Day 8, untouched)
# prediction.py — prefix /api/prediction (Day 9, new)
app.include_router(energy.router)
app.include_router(prediction.router)  # registered ONCE
app.include_router(anomaly.router)     # Day 10: registered ONCE


@app.on_event("startup")
async def _print_routes():
    """Print all registered routes on startup for duplicate-route verification."""
    print("\n=== FastAPI Registered Routes ===")
    seen: set = set()
    duplicates_found = False
    for route in app.routes:
        path = getattr(route, "path", "?")
        methods = ",".join(sorted(getattr(route, "methods", set()) or set()))
        key = f"{methods}:{path}"
        flag = ""
        if key in seen:
            flag = "  [DUPLICATE!]"
            duplicates_found = True
        seen.add(key)
        print(f"  [{methods:8}] {path}{flag}")
    if duplicates_found:
        print("WARNING: Duplicate routes detected!")
    else:
        print("OK: No duplicate routes.")
    print("=================================\n")

@app.get("/")
def read_root():
    return {"message": "Welcome to Smart Energy Monitor API. Go to /docs for API documentation."}
