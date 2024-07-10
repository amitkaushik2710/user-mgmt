from fastapi import APIRouter

from api.routes import status, add_users, get_users, delete_users, update_users, send_invite


api_router = APIRouter()
api_router.include_router(status.router, prefix="/status", tags=["status"])
api_router.include_router(add_users.router, prefix="/add_users", tags=["users"])
api_router.include_router(get_users.router, prefix="/get_users", tags=["users"])
api_router.include_router(update_users.router, tags=["users"])
api_router.include_router(delete_users.router, tags=["users"])
api_router.include_router(send_invite.router, prefix="/send_invite", tags=["invitations"])
