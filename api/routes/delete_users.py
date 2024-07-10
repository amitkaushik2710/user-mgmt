from fastapi import APIRouter, HTTPException, Depends
from core.db import Database, get_database
from core.log import logger

router = APIRouter()

@router.delete("/delete_users/{doc_id}")
async def delete_users(doc_id: str, database: Database = Depends(get_database)):
    """
    Delete a Document from Firestore Collection
    """
    try:
        doc_ref = database.collection.document(doc_id)
        doc = doc_ref.get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Document not found")
        
        doc_ref.delete()
        logger.info(f"delete_document: Deleted document with ID {doc_id}")

        return {"message": f"Document with ID {doc_id} deleted successfully"}
    
    except Exception as e:
        logger.error(f"delete_document: Failed to delete document from Firestore: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete document from Firestore")
