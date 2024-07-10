from fastapi import APIRouter, Request, HTTPException, Depends
import utils
import uuid
from core.db import Database, get_database
from core.log import logger

router = APIRouter()

@router.post("/")
async def add_users(request: Request, database: Database = Depends(get_database)):
    """
    Create new user
    """
    try:
        body = await request.json()
        if not body:
            raise HTTPException(status_code=400, detail="Empty JSON body")
        
        db_data = {}
        for key, value in body.items():
            
            if key == "password":
                hash_password = utils.hash_password(value)
                db_data[key] = hash_password
            else:
                db_data[key] = value

        user_id = str(uuid.uuid4())
        db_data["id"] = user_id

        database.collection.document(user_id).set(db_data)

        response_data = {}
        for key, value in db_data.items():
            if key == "password" or key == "_id":
                continue
            else:
                response_data[key] = value
        
        return {"data": response_data}
        
    except HTTPException as http_err:
        raise http_err
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")