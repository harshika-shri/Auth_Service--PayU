from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from src.api.rest.middleware.cors import add_cors_middleware
from src.api.rest.middleware.error_handler import add_error_handlers
from src.api.rest.routes.authentication import router as authentication_router
from src.api.rest.routes.health import router as health_router
from src.api.rest.routes.sse import router as sse_router
from src.api.rest.routes.user_management import router as user_management_router
from src.api.rest.routes.websocket import router as websocket_router
from src.data.clients.postgres_client import get_or_create_engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    engine = get_or_create_engine()

    # Startup
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))

        print("Database connected")

    except Exception as e:
        print("Database connection failed")
        print(e)

    yield

    # Shutdown
    await engine.dispose()

    print("Database connections closed")


app = FastAPI(
    title="PayU",
    lifespan=lifespan,
)

add_cors_middleware(app)
add_error_handlers(app)
app.include_router(router=authentication_router)
app.include_router(router=user_management_router)
app.include_router(router=health_router)
app.include_router(router=sse_router)
app.include_router(router=websocket_router)
