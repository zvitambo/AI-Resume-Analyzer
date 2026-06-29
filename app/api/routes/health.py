from fastapi import APIRouter
router = APIRouter()




@router.post("/health")
async def health():
    
    return "ok"
   