from fastapi import APIRouter, Request, HTTPException, Depends
import utils
from core.db import Database, get_database
from core.log import logger

router = APIRouter()

@router.patch("/update_users/{user_id}")
async def update_users(user_id: str, request: Request, database: Database = Depends(get_database)):
    """
    Update user details
    """
    try:
        body = await request.json()
        if not body:
            raise HTTPException(status_code=400, detail="Empty JSON body")

        doc_ref = database.collection.document(user_id)
        doc = doc_ref.get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail="User not found")

        db_data = doc.to_dict()
        for key, value in body.items():
            if key == "password":
                hash_password = utils.hash_password(value)
                db_data[key] = hash_password
            else:
                db_data[key] = value

        doc_ref.update(db_data)

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
    except Exception as e:
        logger.error(f"update_user: Failed to update user: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update user")
