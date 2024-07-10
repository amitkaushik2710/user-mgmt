from fastapi import FastAPI, Request
from core.config import settings
from starlette.middleware.cors import CORSMiddleware
from api.main import api_router
import structlog
from core.log import configure_logging
from core.db import connect_to_firestore

configure_logging()
logger = structlog.get_logger()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

async def start_db_client():
    await connect_to_firestore()
app.add_event_handler("startup", start_db_client)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("Request received", method=request.method, url=request.url.path)
    response = await call_next(request)
    logger.info("Response sent", status_code=response.status_code)
    return response

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)