from fastapi import APIRouter, HTTPException, Depends
from core.db import Database, get_database
from core.log import logger

router = APIRouter()

@router.get("/")
async def get_users(database: Database = Depends(get_database)):
    """
    Get All User Details
    """
    try:
        users = []
        documents_ref = database.collection.stream()
        documents = [doc.to_dict() for doc in documents_ref]
        logger.info(f"get_users: Retrieved {users} users from db")
        for user in documents:
            users.append(user)

        logger.info(f"get_users: Retrieved {len(users)} users from db")

        return {"users": users}
    
    except Exception as e:
        logger.error(f"get_users: Failed to fetch users from db: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch users from db")