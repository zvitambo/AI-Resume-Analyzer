from fastapi import FastAPI
from app.api.routes.analyze import router as analyze_router
from app.api.routes.health import router as health_router

app = FastAPI(title="AI Resume Analyzer")

app.include_router(health_router)
app.include_router(analyze_router, prefix="/api")