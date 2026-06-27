from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api.routes.analyze import router as analyze_router
from app.api.routes.health import router as health_router
from app.core.exceptions import BaseAppException
from app.core.logging import logger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Resume Analyzer")

# Global exception handler
@app.exception_handler(BaseAppException)
async def app_exception_handler(request, exc):
    logger.error("Application error: %s", exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message}
    )

app.include_router(health_router)
app.include_router(analyze_router, prefix="/api")

