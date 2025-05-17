from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def update_admin():
    return {"message": "admin privileges ACTIVATED!!!"}