from fastapi import FastAPI
from backend.core.database import engine, Base
from backend.core.routes import router

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SmartReimburse AI",
    description="Core Backend System for SmartReimburse AI",
    version="1.0.0"
)

# Include the main router
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome to SmartReimburse AI API"}

# Note: to run the application, use:
# uvicorn backend.main:app --reload
