from fastapi import APIRouter
from core.log import logger

router = APIRouter()

@router.get("/")
def status():
    """
    Status of the Service
    """
    logger.info("Status: API Called")
    return {"status" : "online", "version":"0.0.1"}